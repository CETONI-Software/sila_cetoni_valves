"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Valve Position Controller*

:details: ValvePositionController:
    Allows to specify a certain logical position for a valve. The Position property can be querried at any time to
    obtain the current valve position.

:file:    ValvePositionController_real.py
:authors: Florian Meinicke

:date: (creation)          2019-07-16T11:11:31.318610
:date: (last modification) 2021-07-10T09:27:04.756905

.. note:: Code generated by sila2codegenerator 0.3.6

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

# import general packages
import logging
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
# import SiLA errors
from impl.common.qmix_errors import DeviceError, QmixSDKSiLAError, \
    ValvePositionOutOfRangeError

# import gRPC modules for this feature
from .gRPC import ValvePositionController_pb2 as ValvePositionController_pb2
# from .gRPC import ValvePositionController_pb2_grpc as ValvePositionController_pb2_grpc

# import default arguments
from .ValvePositionController_default_arguments import default_dict

# import SiLA Defined Error factories
from .ValvePositionController_defined_errors import ValveNotToggleableError, ValvePositionNotAvailableError

# import valve gateway feature
from impl.de.cetoni.valves.ValveGatewayService.ValveGatewayService_servicer import ValveGatewayService

# import qmixsdk
from qmixsdk.qmixvalve import Valve


# noinspection PyPep8Naming,PyUnusedLocal
class ValvePositionControllerReal:
    """
    Implementation of the *Valve Position Controller* in *Real* mode
        Allows to control valve devices
    """

    def __init__(self, valve: Valve = None, valve_gateway: ValveGatewayService = None):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

        self.valve = valve
        self.valve_gateway: ValveGatewayService = valve_gateway

    def _get_valve(self, invocation_metadata, type: str) -> Valve:
        """
        Get the valve that the calling command/property should operate on.
        This returns either this Feature's specific valve or the valve that is identified
        by the ID in the given `invocation_metadata`.

        :param invocation_metadata: The metadata that contains a valve identifier which
                                    can be mapped to a qmixvalve.Valve object
        :param type: Either "Command" or "Property"

        :returns: A valve that the calling command/property can operate on
        :rtype: Valve
        """

        if self.valve is not None:
            return self.valve

        return self.valve_gateway.get_valve(invocation_metadata, type)

    def SwitchToPosition(self, request, context: grpc.ServicerContext) \
            -> ValvePositionController_pb2.SwitchToPosition_Responses:
        """
        Executes the unobservable command "Switch To Position"
            Switches the valve to the specified position. The given position has to be less than the NumberOfPositions or else a ValidationError is thrown.

        :param request: gRPC request containing the parameters passed:
            request.Position (Position): The target position that the valve should be switched to.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        valve = self._get_valve(context.invocation_metadata(), "Command")

        requested_valve_pos = request.Position.value
        num_of_valve_pos = valve.number_of_valve_positions()

        if requested_valve_pos < 0 or requested_valve_pos >= num_of_valve_pos:
            raise ValvePositionOutOfRangeError(
                f"The given position ({requested_valve_pos}) is not in the range "
                "for this valve. Adjust the valve position to fit in the range "
                f"between 0 and {num_of_valve_pos - 1}!"
            )

        valve.switch_valve_to_position(requested_valve_pos)
        return ValvePositionController_pb2.SwitchToPosition_Responses()

    def TogglePosition(self, request, context: grpc.ServicerContext) \
            -> ValvePositionController_pb2.TogglePosition_Responses:
        """
        Executes the unobservable command "Toggle Position"
            This command only applies for 2-way valves to toggle between its two different positions. If the command is called for any other valve type a ValveNotToggleable error is thrown.

        :param request: gRPC request containing the parameters passed:
            request.EmptyParameter (Empty Parameter): An empty parameter data type used if no parameter is required.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        valve = self._get_valve(context.invocation_metadata(), "Command")

        if valve.number_of_valve_positions() > 2:
            raise ValveNotToggleableError()

        try:
            curr_pos = valve.actual_valve_position()
            valve.switch_valve_to_position((curr_pos + 1) % 2)

            return ValvePositionController_pb2.TogglePosition_Responses()
        except DeviceError as err:
            if err.errorcode == -2:
                raise ValvePositionNotAvailableError()

    def Get_NumberOfPositions(self, request, context: grpc.ServicerContext) \
            -> ValvePositionController_pb2.Get_NumberOfPositions_Responses:
        """
        Requests the unobservable property Number Of Positions
            The number of the valve positions available.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            NumberOfPositions (Number Of Positions): The number of the valve positions available.
        """

        valve = self._get_valve(context.invocation_metadata(), "Property")

        return ValvePositionController_pb2.Get_NumberOfPositions_Responses(
            NumberOfPositions=silaFW_pb2.Integer(value=valve.number_of_valve_positions())
        )

    def Subscribe_Position(self, request, context: grpc.ServicerContext) \
            -> ValvePositionController_pb2.Subscribe_Position_Responses:
        """
        Requests the observable property Position
            The current logical valve position. This is a value between 0 and NumberOfPositions - 1.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            Position (Position): The current logical valve position. This is a value between 0 and NumberOfPositions - 1.
        """

        valve = self._get_valve(context.invocation_metadata(), "Property")

        while True:
            try:
                yield ValvePositionController_pb2.Subscribe_Position_Responses(
                    Position=silaFW_pb2.Integer(value=valve.actual_valve_position())
                )
            except DeviceError as err:
                if err.errorcode == -2:
                    raise ValvePositionNotAvailableError()

            # we add a small delay to give the client a chance to keep up.
            time.sleep(0.5)
