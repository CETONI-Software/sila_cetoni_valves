# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ValveGatewayService.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import sila2lib.framework.SiLAFramework_pb2 as SiLAFramework__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ValveGatewayService.proto',
  package='sila2.de.cetoni.valves.valvegatewayservice.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19ValveGatewayService.proto\x12-sila2.de.cetoni.valves.valvegatewayservice.v1\x1a\x13SiLAFramework.proto\"6\n4Get_FCPAffectedByMetadata_ValveIdentifier_Parameters\"l\n3Get_FCPAffectedByMetadata_ValveIdentifier_Responses\x12\x35\n\rAffectedCalls\x18\x01 \x03(\x0b\x32\x1e.sila2.org.silastandard.String\"S\n\x18Metadata_ValveIdentifier\x12\x37\n\x0fValveIdentifier\x18\x01 \x01(\x0b\x32\x1e.sila2.org.silastandard.String2\x8e\x02\n\x13ValveGatewayService\x12\xf6\x01\n)Get_FCPAffectedByMetadata_ValveIdentifier\x12\x63.sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Parameters\x1a\x62.sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Responses\"\x00\x62\x06proto3'
  ,
  dependencies=[SiLAFramework__pb2.DESCRIPTOR,])




_GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_PARAMETERS = _descriptor.Descriptor(
  name='Get_FCPAffectedByMetadata_ValveIdentifier_Parameters',
  full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Parameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=151,
)


_GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_RESPONSES = _descriptor.Descriptor(
  name='Get_FCPAffectedByMetadata_ValveIdentifier_Responses',
  full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Responses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='AffectedCalls', full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Responses.AffectedCalls', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=153,
  serialized_end=261,
)


_METADATA_VALVEIDENTIFIER = _descriptor.Descriptor(
  name='Metadata_ValveIdentifier',
  full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.Metadata_ValveIdentifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ValveIdentifier', full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.Metadata_ValveIdentifier.ValveIdentifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=263,
  serialized_end=346,
)

_GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_RESPONSES.fields_by_name['AffectedCalls'].message_type = SiLAFramework__pb2._STRING
_METADATA_VALVEIDENTIFIER.fields_by_name['ValveIdentifier'].message_type = SiLAFramework__pb2._STRING
DESCRIPTOR.message_types_by_name['Get_FCPAffectedByMetadata_ValveIdentifier_Parameters'] = _GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_PARAMETERS
DESCRIPTOR.message_types_by_name['Get_FCPAffectedByMetadata_ValveIdentifier_Responses'] = _GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_RESPONSES
DESCRIPTOR.message_types_by_name['Metadata_ValveIdentifier'] = _METADATA_VALVEIDENTIFIER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Get_FCPAffectedByMetadata_ValveIdentifier_Parameters = _reflection.GeneratedProtocolMessageType('Get_FCPAffectedByMetadata_ValveIdentifier_Parameters', (_message.Message,), {
  'DESCRIPTOR' : _GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_PARAMETERS,
  '__module__' : 'ValveGatewayService_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Parameters)
  })
_sym_db.RegisterMessage(Get_FCPAffectedByMetadata_ValveIdentifier_Parameters)

Get_FCPAffectedByMetadata_ValveIdentifier_Responses = _reflection.GeneratedProtocolMessageType('Get_FCPAffectedByMetadata_ValveIdentifier_Responses', (_message.Message,), {
  'DESCRIPTOR' : _GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_RESPONSES,
  '__module__' : 'ValveGatewayService_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.valves.valvegatewayservice.v1.Get_FCPAffectedByMetadata_ValveIdentifier_Responses)
  })
_sym_db.RegisterMessage(Get_FCPAffectedByMetadata_ValveIdentifier_Responses)

Metadata_ValveIdentifier = _reflection.GeneratedProtocolMessageType('Metadata_ValveIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _METADATA_VALVEIDENTIFIER,
  '__module__' : 'ValveGatewayService_pb2'
  # @@protoc_insertion_point(class_scope:sila2.de.cetoni.valves.valvegatewayservice.v1.Metadata_ValveIdentifier)
  })
_sym_db.RegisterMessage(Metadata_ValveIdentifier)



_VALVEGATEWAYSERVICE = _descriptor.ServiceDescriptor(
  name='ValveGatewayService',
  full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.ValveGatewayService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=349,
  serialized_end=619,
  methods=[
  _descriptor.MethodDescriptor(
    name='Get_FCPAffectedByMetadata_ValveIdentifier',
    full_name='sila2.de.cetoni.valves.valvegatewayservice.v1.ValveGatewayService.Get_FCPAffectedByMetadata_ValveIdentifier',
    index=0,
    containing_service=None,
    input_type=_GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_PARAMETERS,
    output_type=_GET_FCPAFFECTEDBYMETADATA_VALVEIDENTIFIER_RESPONSES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_VALVEGATEWAYSERVICE)

DESCRIPTOR.services_by_name['ValveGatewayService'] = _VALVEGATEWAYSERVICE

# @@protoc_insertion_point(module_scope)