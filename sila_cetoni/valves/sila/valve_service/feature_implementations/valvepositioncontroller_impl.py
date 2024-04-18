from __future__ import annotations

import logging
from functools import partial
from queue import Queue
from typing import List, Optional, cast

from qmixsdk.qmixbus import DeviceError
from qmixsdk.qmixvalve import Valve
from sila2.framework import Command
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem
from sila_cetoni.utils import PropertyUpdater, not_equal

from ..generated.valvegatewayservice import InvalidValveIndex
from ..generated.valvepositioncontroller import (
    SwitchToPosition_Responses,
    TogglePosition_Responses,
    ValveNotToggleable,
    ValvePositionControllerBase,
    ValvePositionControllerFeature,
    ValvePositionNotAvailable,
)
from .valvegatewayservice_impl import ValveGatewayServiceImpl

logger = logging.getLogger(__name__)


@CetoniApplicationSystem.monitor_traffic
class ValvePositionControllerImpl(ValvePositionControllerBase):
    __valve: Optional[Valve]
    __valve_gateway: Optional[ValveGatewayServiceImpl]
    __position_queues: List[Queue[int]]  # same number of items and order as `__valve_gateway.valves`
    __system: ApplicationSystem

    def __init__(
        self,
        server: SilaServer,
        valve: Optional[Valve] = None,
        gateway: Optional[ValveGatewayServiceImpl] = None,
    ):
        super().__init__(server)
        self.__valve = valve
        self.__valve_gateway = gateway
        self.__system = ApplicationSystem()  # type: ignore

        if self.__valve is not None:
            try:
                self.__valve.actual_valve_position()
                self.run_periodically(
                    PropertyUpdater(
                        self.__valve.actual_valve_position,
                        not_equal,
                        self.update_Position,
                        when=self.__system.state.is_operational,
                    )
                )
            except DeviceError as err:
                logger.error(f"Error reading valve position for valve {self.__valve.get_device_name()}: {err}")
        elif self.__valve_gateway is not None:
            self.__position_queues = []
            for i in range(len(self.__valve_gateway.valves)):
                queue = Queue()
                self.__position_queues += [queue]

                self.run_periodically(
                    PropertyUpdater(
                        lambda: self.__valve_gateway.valves[i].actual_valve_position(),  # type: ignore
                        not_equal,
                        partial(self.update_Position, queue=queue),
                        when=self.__system.state.is_operational,
                    )
                )

    def __get_valve(self, metadata: MetadataDict) -> Valve:
        if self.__valve is not None:
            return self.__valve

        if self.__valve_gateway is not None:
            return self.__valve_gateway.get_valve(metadata)

        raise ValueError("No valve or valve gateway is set. Cannot determine the valve.")

    def get_NumberOfPositions(self, *, metadata: MetadataDict) -> int:
        return self.__get_valve(metadata).number_of_valve_positions()

    def Position_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[int]]:
        if self.__valve_gateway is None:
            return super().Position_on_subscription(metadata=metadata)

        valve_index: int = metadata[self.__valve_gateway.valve_index_metadata]
        try:
            return self.__position_queues[valve_index]
        except IndexError:
            raise InvalidValveIndex(
                message=f"The sent Valve Index {valve_index} is invalid. The index must be between 0 and {len(self.__valve_gateway.valves) - 1}.",
            )

    @staticmethod
    def _try_switch_valve_to_position(valve: Valve, position: int):
        try:
            valve.switch_valve_to_position(position)
        except DeviceError as err:
            if err.errorcode == 2:
                raise ValvePositionNotAvailable()
            raise err

    @ApplicationSystem.ensure_operational(ValvePositionControllerFeature)
    def SwitchToPosition(self, Position: int, *, metadata: MetadataDict) -> SwitchToPosition_Responses:
        valve = self.__get_valve(metadata)
        if 0 > Position or Position >= valve.number_of_valve_positions():
            err = ValidationError(
                f"The given position ({Position}) is not in the range for this valve. "
                f"Adjust the valve position to fit in the range between 0 and {valve.number_of_valve_positions() - 1}!"
            )
            err.parameter_fully_qualified_identifier = (
                cast(Command, ValvePositionControllerFeature["SwitchToPosition"])
                .parameters.fields[0]
                .fully_qualified_identifier
            )
            raise err

        self._try_switch_valve_to_position(valve, Position)
        return SwitchToPosition_Responses()

    @ApplicationSystem.ensure_operational(ValvePositionControllerFeature)
    def TogglePosition(self, *, metadata: MetadataDict) -> TogglePosition_Responses:
        valve = self.__get_valve(metadata)
        if valve.number_of_valve_positions() > 2:
            raise ValveNotToggleable()

        self._try_switch_valve_to_position(valve, (valve.actual_valve_position() + 1) % 2)
        return TogglePosition_Responses()
