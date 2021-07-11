"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Valve Gateway Service*

:details: ValveGatewayService:
    Provides means to access individual valves of a valve terminal

:file:    ValveGatewayService_real.py
:authors: Florian Meinicke

:date: (creation)          2021-01-07T13:40:21.899119
:date: (last modification) 2021-07-10T09:27:04.770908

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
from typing import List, Tuple

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import SiLA errors
from impl.common.qmix_errors import SiLAFrameworkError, SiLAFrameworkErrorType

# import gRPC modules for this feature
from .gRPC import ValveGatewayService_pb2 as ValveGatewayService_pb2
# from .gRPC import ValveGatewayService_pb2_grpc as ValveGatewayService_pb2_grpc

# import default arguments
from .ValveGatewayService_default_arguments import default_dict

from qmixsdk.qmixvalve import Valve

from . import METADATA_VALVE_INDEX

# noinspection PyPep8Naming,PyUnusedLocal
class ValveGatewayServiceReal:
    """
    Implementation of the *Valve Gateway Service* in *Real* mode
        Allows to control valve devices
    """

    def __init__(self, valves: List[Valve]):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

        self.valves = valves
        self.num_valves = len(self.valves)

    def _get_valve_index(self, metadata: Tuple[Tuple[str, str]], type: str) -> int:
        """
        Get the requested valve index from the given `metadata`

        :param metdata: The metadata of the call. It should contain the requested valve index
        :param type: Either "Command" or "Property"
        :return: The valve index if it can be obtained, otherwise a SiLAFrameworkError will be raised
        """

        invocation_metadata = {key: value for key, value in metadata}
        logging.debug(f"Received invocation metadata: {invocation_metadata}")
        try:
            message = ValveGatewayService_pb2.Metadata_ValveIndex()
            message.ParseFromString(invocation_metadata[METADATA_VALVE_INDEX])
            return message.ValveIndex.value
        except KeyError:
            raise SiLAFrameworkError(SiLAFrameworkErrorType.INVALID_METADATA,
                                     f'This {type} requires the ValveIndex metadata!')

    def get_valve(self, metadata: Tuple[Tuple[str, str]], type: str) -> Valve:
        """
        Get the valve that is identified by the valve index given in `metadata`

        :param metdata: The metadata of the call. It should contain the requested valve index
        :param type: Either "Command" or "Property"
        :return: A valid valve object if the valve can be identified, otherwise a SiLAFrameworkError will be raised
        """

        valve_id = self._get_valve_index(metadata, type)

        logging.debug(f"Requested valve: {valve_id}")

        try:
            return self.valves[valve_id]
        except KeyError:
            raise SiLAFrameworkError(
                SiLAFrameworkErrorType.INVALID_METADATA,
                f"The sent valve index ({valve_id}) is invalid! "
                f"The index has to be between 0 and {self.num_valves - 1}."
            )

    def Get_NumberOfValves(self, request, context: grpc.ServicerContext) \
            -> ValveGatewayService_pb2.Get_NumberOfValves_Responses:
        """
        Requests the unobservable property Number Of Valves
            The number of valves of a terminal

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            NumberOfValves (Number Of Valves): The number of valves of a terminal
        """

        return ValveGatewayService_pb2.Get_NumberOfValves_Responses(
                NumberOfValves=silaFW_pb2.Integer(value=self.num_valves)
            )

    def Get_FCPAffectedByMetadata_ValveIndex(self, request, context: grpc.ServicerContext) \
            -> ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIndex_Responses:
        """
        Requests the unobservable property FCPAffectedByMetadata Valve Index
            Specifies which Features/Commands/Properties of the SiLA server are affected by the Valve Index Metadata.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            AffectedCalls (AffectedCalls): A string containing a list of Fully Qualified Identifiers of Features, Commands and Properties for which the SiLA Client Metadata is expected as part of the respective RPCs.
        """

        return ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIndex_Responses(
            AffectedCalls=[
                silaFW_pb2.String(value="de.cetoni/valves/ValvePositionController/v1")
            ]
        )
