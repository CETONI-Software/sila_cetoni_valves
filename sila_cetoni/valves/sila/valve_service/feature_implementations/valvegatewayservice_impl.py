from __future__ import annotations

import logging
from typing import List, Union, cast

from qmixsdk.qmixvalve import Valve
from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Metadata, Property
from sila2.server import MetadataDict, SilaServer

from ..generated.valvegatewayservice import InvalidValveIndex, ValveGatewayServiceBase, ValveGatewayServiceFeature
from ..generated.valvepositioncontroller import ValvePositionControllerFeature

logger = logging.getLogger(__name__)


class ValveGatewayServiceImpl(ValveGatewayServiceBase):
    __valves: List[Valve]
    __valve_index_metadata: Metadata[int]

    def __init__(self, server: SilaServer, valves: List[Valve]) -> None:
        super().__init__(server)
        self.__valves = valves
        self.__valve_index_metadata = cast(Metadata[int], ValveGatewayServiceFeature["ValveIndex"])

    def get_NumberOfValves(self, *, metadata: MetadataDict) -> int:
        return len(self.__valves)

    def get_calls_affected_by_ValveIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [ValvePositionControllerFeature]

    def get_valve(self, metadata: MetadataDict) -> Valve:
        """
        Get the valve that is identified by the valve index given in `metadata`

        Parameters
        ----------
        metadata : MetadataDict
            The metadata of the call. It should contain the requested valve index

        Returns
        -------
        Valve
            A valid `Valve` object if the valve can be identified

        Raises
        ------
        FrameworkError
            If the valve index is invalid
        """

        valve_index: int = metadata[self.__valve_index_metadata]
        logger.debug(f"Requested valve: {valve_index}")

        try:
            if valve_index < 0:
                raise IndexError
            return self.__valves[valve_index]
        except IndexError:
            raise InvalidValveIndex(
                message=(
                    f"The sent Valve Index ({valve_index}) is invalid! The index has to be between 0 and "
                    f"{len(self.__valves) - 1}."
                )
            )

    @property
    def valves(self) -> List[Valve]:
        return self.__valves

    @property
    def valve_index_metadata(self) -> Metadata:
        return self.__valve_index_metadata
