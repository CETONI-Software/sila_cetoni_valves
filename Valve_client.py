#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Valve client*

:details: Valve:
    Allows to control valve devices

:file:    Valve_client.py
:authors: Florian Meinicke

:date: (creation)          2021-01-07T11:31:48.192429
:date: (last modification) 2021-01-07T11:31:48.192429

.. note:: Code generated by sila2codegenerator 0.2.0

_______________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

# import general packages
import logging
import argparse
import grpc
import time

# import meta packages
from typing import Union, Optional

# import SiLA2 library modules
from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2
from sila2lib.sila_client import SiLA2Client
from sila2lib.framework.std_features import SiLAService_pb2 as SiLAService_feature_pb2
from sila2lib.error_handling import client_err
#   Usually not needed, but - feel free to modify
# from sila2lib.framework.std_features import SimulationController_pb2 as SimController_feature_pb2

# import feature gRPC modules
# Import gRPC libraries of features
from impl.de.cetoni.valves.ValvePositionController.gRPC import ValvePositionController_pb2
from impl.de.cetoni.valves.ValvePositionController.gRPC import ValvePositionController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.valves.ValvePositionController.ValvePositionController_default_arguments import default_dict as ValvePositionController_default_dict
from impl.de.cetoni.valves.ValveGatewayService.gRPC import ValveGatewayService_pb2
from impl.de.cetoni.valves.ValveGatewayService.gRPC import ValveGatewayService_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.valves.ValveGatewayService.ValveGatewayService_default_arguments import default_dict as ValveGatewayService_default_dict


# noinspection PyPep8Naming, PyUnusedLocal
class ValveClient(SiLA2Client):
    """
        Allows to control valve devices

    .. note:: For an example on how to construct the parameter or read the response(s) for command calls and properties,
              compare the default dictionary that is stored in the directory of the corresponding feature.
    """
    # The following variables will be filled when run() is executed
    #: Storage for the connected servers version
    server_version: str = ''
    #: Storage for the display name of the connected server
    server_display_name: str = ''
    #: Storage for the description of the connected server
    server_description: str = ''

    def __init__(self,
                 name: str = "ValveClient", description: str = "Allows to control valve devices",
                 server_name: Optional[str] = None,
                 client_uuid: Optional[str] = None,
                 version: str = __version__,
                 vendor_url: str = "cetoni.de",
                 server_hostname: str = "localhost", server_ip: str = "127.0.0.1", server_port: int = 50052,
                 cert_file: Optional[str] = None):
        """Class initialiser"""
        super().__init__(
            name=name, description=description,
            server_name=server_name,
            client_uuid=client_uuid,
            version=version,
            vendor_url=vendor_url,
            server_hostname=server_hostname, server_ip=server_ip, server_port=server_port,
            cert_file=cert_file
        )

        logging.info(
            "Starting SiLA2 service client for service Valve with service name: {server_name}".format(
                server_name=name
            )
        )

        # Create stub objects used to communicate with the server
        self.ValvePositionController_stub = \
            ValvePositionController_pb2_grpc.ValvePositionControllerStub(self.channel)

        # initialise class variables for server information storage
        self.server_version = ''
        self.server_display_name = ''
        self.server_description = ''

    def Get_ImplementedFeatures(self):
        """Get a list of all implemented features."""
        # type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Retrieving the list of implemented features of the server:")
        try:
            response = self.SiLAService_stub.Get_ImplementedFeatures(
                SiLAService_feature_pb2.Get_ImplementedFeatures_Parameters()
            )
            for feature_id in response.ImplementedFeatures:
                logging.debug("Implemented feature: {feature_id}".format(
                    feature_id=feature_id.value)
                    )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.ImplementedFeatures

    def Get_FeatureDefinition(self, feature_identifier: str) -> Union[str, None]:
        """
        Returns the FDL/XML feature definition of the given feature.

        :param feature_identifier: The name of the feature for which the definition should be returned.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Requesting feature definitions of feature {feature_identifier}:".format(
            feature_identifier=feature_identifier)
        )
        try:
            response = self.SiLAService_stub.GetFeatureDefinition(
                SiLAService_feature_pb2.GetFeatureDefinition_Parameters(
                    QualifiedFeatureIdentifier=silaFW_pb2.String(value=feature_identifier)
                    )
                )
            logging.debug("Response of GetFeatureDefinition for {feature_identifier} feature: {response}".format(
                response=response,
                feature_identifier=feature_identifier)
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

    def run(self) -> bool:
        """
        Starts the actual client and retrieves the meta-information from the server.

        :returns: True or False whether the connection to the server is established.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        try:
            # Retrieve the basic server information and store it in internal class variables
            #   Display name
            response = self.SiLAService_stub.Get_ServerName(SiLAService_feature_pb2.Get_ServerName_Parameters())
            self.server_display_name = response.ServerName.value
            logging.debug("Display name: {name}".format(name=response.ServerName.value))
            # Server description
            response = self.SiLAService_stub.Get_ServerDescription(
                SiLAService_feature_pb2.Get_ServerDescription_Parameters()
            )
            self.server_description = response.ServerDescription.value
            logging.debug("Description: {description}".format(description=response.ServerDescription.value))
            # Server version
            response = self.SiLAService_stub.Get_ServerVersion(SiLAService_feature_pb2.Get_ServerVersion_Parameters())
            self.server_version = response.ServerVersion.value
            logging.debug("Version: {version}".format(version=response.ServerVersion.value))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return False

        return True

    def stop(self, force: bool = False) -> bool:
        """
        Stop SiLA client routine

        :param force: If set True, the client is supposed to disconnect and stop immediately. Otherwise it can first try
                      to finish what it is doing.

        :returns: Whether the client could be stopped successfully or not.
        """
        # TODO: Implement all routines that have to be executed when the client is stopped.
        #   Feel free to use the "force" parameter to abort any running processes. Or crash your machine. Your call!
        return True

    def SwitchToPosition(self,
                      parameter: ValvePositionController_pb2.SwitchToPosition_Parameters = None) \
            -> ValvePositionController_pb2.SwitchToPosition_Responses:
        """
        Wrapper to call the unobservable command SwitchToPosition on the server.

        :param parameter: The parameter gRPC construct required for this command.

        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Calling SwitchToPosition:")
        try:
            # resolve to default if no value given
            #   TODO: Implement a more reasonable default value
            if parameter is None:
                parameter = ValvePositionController_pb2.SwitchToPosition_Parameters(
                    **ValvePositionController_default_dict['SwitchToPosition_Parameters']
                )

            response = self.ValvePositionController_stub.SwitchToPosition(parameter)

            logging.debug('SwitchToPosition response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response

    def TogglePosition(self,
                      parameter: ValvePositionController_pb2.TogglePosition_Parameters = None) \
            -> ValvePositionController_pb2.TogglePosition_Responses:
        """
        Wrapper to call the unobservable command TogglePosition on the server.

        :param parameter: The parameter gRPC construct required for this command.

        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Calling TogglePosition:")
        try:
            # resolve to default if no value given
            #   TODO: Implement a more reasonable default value
            if parameter is None:
                parameter = ValvePositionController_pb2.TogglePosition_Parameters(
                    **ValvePositionController_default_dict['TogglePosition_Parameters']
                )

            response = self.ValvePositionController_stub.TogglePosition(parameter)

            logging.debug('TogglePosition response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response


    def Get_NumberOfPositions(self) \
            -> ValvePositionController_pb2.Get_NumberOfPositions_Responses:
        """Wrapper to get property NumberOfPositions from the server."""
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Reading unobservable property NumberOfPositions:")
        try:
            response = self.ValvePositionController_stub.Get_NumberOfPositions(
                ValvePositionController_pb2.Get_NumberOfPositions_Parameters()
            )
            logging.debug(
                'Get_NumberOfPositions response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response
    def Subscribe_Position(self) \
            -> ValvePositionController_pb2.Subscribe_Position_Responses:
        """Wrapper to get property Position from the server."""
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Reading observable property Position:")
        try:
            response = self.ValvePositionController_stub.Subscribe_Position(
                ValvePositionController_pb2.Subscribe_Position_Parameters()
            )
            logging.debug(
                'Subscribe_Position response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response


    def Get_FCPAffectedByMetadata_ValveIdentifier(self) \
            -> ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIdentifier_Responses:
        """Wrapper to get property FCPAffectedByMetadata_ValveIdentifier from the server."""
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Reading unobservable property FCPAffectedByMetadata_ValveIdentifier:")
        try:
            response = self.ValveGatewayService_stub.Get_FCPAffectedByMetadata_ValveIdentifier(
                ValveGatewayService_pb2.Get_FCPAffectedByMetadata_ValveIdentifier_Parameters()
            )
            logging.debug(
                'Get_FCPAffectedByMetadata_ValveIdentifier response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response

    @staticmethod
    def grpc_error_handling(error_object: grpc.Call) -> None:
        """Handles exceptions of type grpc.RpcError"""
        # pass to the default error handling
        grpc_error =  client_err.grpc_error_handling(error_object=error_object)

        # Access more details using the return value fields
        # grpc_error.message
        # grpc_error.error_type


def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 client: Valve")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    return parser.parse_args()


if __name__ == '__main__':
    # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    parsed_args = parse_command_line()

    # start the server
    sila_client = ValveClient(server_ip='127.0.0.1', server_port=50052)
    sila_client.run()

    # Log connection info
    logging.info(
        (
            'Connected to SiLA Server {display_name} running in version {version}.' '\n'
            'Service description: {service_description}'
        ).format(
            display_name=sila_client.server_display_name,
            version=sila_client.server_version,
            service_description=sila_client.server_description
        )
    )

    # TODO:
    #   Write your further function calls here to run the client as a standalone application.
