#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Valve*

:details: Valve:
    Allows to control valve devices

:file:    Valve_server.py
:authors: Florian Meinicke

:date: (creation)          2021-01-07T11:31:48.185578
:date: (last modification) 2021-01-07T11:31:48.185578

.. note:: Code generated by sila2codegenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

import os
import logging
import argparse

# Import the main SiLA library
from sila2lib.sila_server import SiLA2Server

# Import gRPC libraries of features
from impl.de.cetoni.valves.ValveGatewayService.gRPC import ValveGatewayService_pb2
from impl.de.cetoni.valves.ValveGatewayService.gRPC import ValveGatewayService_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.valves.ValveGatewayService.ValveGatewayService_default_arguments import default_dict as ValveGatewayService_default_dict
from impl.de.cetoni.valves.ValvePositionController.gRPC import ValvePositionController_pb2
from impl.de.cetoni.valves.ValvePositionController.gRPC import ValvePositionController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.valves.ValvePositionController.ValvePositionController_default_arguments import default_dict as ValvePositionController_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.valves.ValveGatewayService.ValveGatewayService_servicer import ValveGatewayService
from impl.de.cetoni.valves.ValvePositionController.ValvePositionController_servicer import ValvePositionController

from ..local_ip import LOCAL_IP

class ValveServer(SiLA2Server):
    """
    Allows to control valve devices
    """

    def __init__(self, cmd_args, valves, simulation_mode: bool = True):
        """Class initialiser"""
        super().__init__(
            name=cmd_args.server_name, description=cmd_args.description,
            server_type=cmd_args.server_type, server_uuid=None,
            version=__version__,
            vendor_url="cetoni.de",
            ip=LOCAL_IP, port=int(cmd_args.port),
            key_file=cmd_args.encryption_key, cert_file=cmd_args.encryption_cert,
            simulation_mode=simulation_mode
        )

        logging.info(
            "Starting SiLA2 server with server name: {server_name}".format(
                server_name=cmd_args.server_name
            )
        )

        data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..',
                                                 'features', 'de', 'cetoni', 'valves'))

        # registering features
        #  Register de.cetoni.valve.ValveGatewayService
        self.ValveGatewayService_servicer = ValveGatewayService(
            valves=valves,
            simulation_mode=self.simulation_mode
        )
        ValveGatewayService_pb2_grpc.add_ValveGatewayServiceServicer_to_server(
            self.ValveGatewayService_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='de.cetoni/valves/ValveGatewayService/v1',
                         servicer=self.ValveGatewayService_servicer,
                         data_path=data_path)
        #  Register de.cetoni.valves.ValvePositionController
        self.ValvePositionController_servicer = ValvePositionController(
            valve_gateway=self.ValveGatewayService_servicer,
            simulation_mode=self.simulation_mode
        )
        ValvePositionController_pb2_grpc.add_ValvePositionControllerServicer_to_server(
            self.ValvePositionController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='de.cetoni/valves/ValvePositionController/v1',
                         servicer=self.ValvePositionController_servicer,
                         data_path=data_path)

        self.simulation_mode = simulation_mode


def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: Valve")

    # Simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="Valve", help='start SiLA server with [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="Allows to control valve devices", help='SiLA server description')

    # Encryption
    parser.add_argument('-X', '--encryption', action='store', default=None,
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parsed_args = parser.parse_args()

    # validate/update some settings
    #   encryption
    if parsed_args.encryption is not None:
        # only overwrite the separate keys if not given manually
        if parsed_args.encryption_key is None:
            parsed_args.encryption_key = parsed_args.encryption + '.key'
        if parsed_args.encryption_cert is None:
            parsed_args.encryption_cert = parsed_args.encryption + '.cert'

    return parsed_args


if __name__ == '__main__':
    # or use logging.ERROR for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    args = parse_command_line()

    # generate SiLA2Server
    sila_server = ValveServer(cmd_args=args, simulation_mode=True)
