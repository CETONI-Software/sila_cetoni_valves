"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Valve Gateway Service*

:details: ValveGatewayService:
    Provides means to access individual valves of a valve terminal

:file:    ValveGatewayService_simulation.py
:authors: Florian Meinicke

:date: (creation)          2021-01-07T15:03:06.171562
:date: (last modification) 2021-07-09T13:25:42.690556

.. note:: Code generated by sila2codegenerator 0.2.0

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

# import gRPC modules for this feature
from .gRPC import ValveGatewayService_pb2 as ValveGatewayService_pb2
# from .gRPC import ValveGatewayService_pb2_grpc as ValveGatewayService_pb2_grpc

# import default arguments
from .ValveGatewayService_default_arguments import default_dict


# noinspection PyPep8Naming,PyUnusedLocal
class ValveGatewayServiceSimulation:
    """
    Implementation of the *Valve Gateway Service* in *Simulation* mode
        Allows to control valve devices
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Simulation'))

    def _get_command_state(self, command_uuid: str) -> silaFW_pb2.ExecutionInfo:
        """
        Method to fill an ExecutionInfo message from the SiLA server for observable commands

        :param command_uuid: The uuid of the command for which to return the current state

        :return: An execution info object with the current command state
        """

        #: Enumeration of silaFW_pb2.ExecutionInfo.CommandStatus
        command_status = silaFW_pb2.ExecutionInfo.CommandStatus.waiting
        #: Real silaFW_pb2.Real(0...1)
        command_progress = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_estimated_remaining = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_lifetime_of_execution = None

        # TODO: check the state of the command with the given uuid and return the correct information

        # just return a default in this example
        return silaFW_pb2.ExecutionInfo(
            commandStatus=command_status,
            progressInfo=(
                command_progress if command_progress is not None else None
            ),
            estimatedRemainingTime=(
                command_estimated_remaining if command_estimated_remaining is not None else None
            ),
            updatedLifetimeOfExecution=(
                command_lifetime_of_execution if command_lifetime_of_execution is not None else None
            )
        )

    def get_valve(self, metadata, type: str):
        """
        Get the valve that is identified by the valve index given in `metadata`
        This is just a dummy

        :param metdata: The metadata of the call. It should contain the requested valve index
        :param type: Either "Command" or "Property"
        :return: A valid valve object if the valve can be identified, otherwise a SiLAFrameworkError will be raised
        """

        return None


    def Get_NumberOfValves(self, request, context: grpc.ServicerContext) \
            -> ValveGatewayService_pb2.Get_NumberOfValves_Responses:
        """
        Requests the unobservable property Valve Identifiers
            The number of valves of a terminal

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            NumberOfValves (Valve Identifiers): The number of valves of a terminal
        """

        # initialise the return value
        return_value: ValveGatewayService_pb2.Get_NumberOfValves_Responses = None

        # TODO:
        #   Add implementation of Simulation for property NumberOfValves here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = ValveGatewayService_pb2.Get_NumberOfValves_Responses(
                **default_dict['Get_NumberOfValves_Responses']
            )

        return return_value

    def Get_FCPAffectedByMetadata_ValveIndex(self, request, context: grpc.ServicerContext) \
            -> ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIndex_Responses:
        """
        Requests the unobservable property FCPAffectedByMetadata Valve Identifier
            Specifies which Features/Commands/Properties of the SiLA server are affected by the Valve Identifier Metadata.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            AffectedCalls (AffectedCalls): A string containing a list of Fully Qualified Identifiers of Features, Commands and Properties for which the SiLA Client Metadata is expected as part of the respective RPCs.
        """

        # initialise the return value
        return_value: ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIndex_Responses = None

        # TODO:
        #   Add implementation of Simulation for property FCPAffectedByMetadata_ValveIndex here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIndex_Responses(
                **default_dict['Get_FCPAffectedByMetadata_ValveIndex_Responses']
            )

        return return_value
