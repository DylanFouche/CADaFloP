# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: error.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from src.protobuf import enums_pb2 as enums__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='error.proto',
  package='CARTA',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0b\x65rror.proto\x12\x05\x43\x41RTA\x1a\x0b\x65nums.proto\"`\n\tErrorData\x12&\n\x08severity\x18\x01 \x01(\x0e\x32\x14.CARTA.ErrorSeverity\x12\x0c\n\x04tags\x18\x02 \x03(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\tb\x06proto3'
  ,
  dependencies=[enums__pb2.DESCRIPTOR,])




_ERRORDATA = _descriptor.Descriptor(
  name='ErrorData',
  full_name='CARTA.ErrorData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='severity', full_name='CARTA.ErrorData.severity', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='CARTA.ErrorData.tags', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='CARTA.ErrorData.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='CARTA.ErrorData.data', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=35,
  serialized_end=131,
)

_ERRORDATA.fields_by_name['severity'].enum_type = enums__pb2._ERRORSEVERITY
DESCRIPTOR.message_types_by_name['ErrorData'] = _ERRORDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorData = _reflection.GeneratedProtocolMessageType('ErrorData', (_message.Message,), {
  'DESCRIPTOR' : _ERRORDATA,
  '__module__' : 'error_pb2'
  # @@protoc_insertion_point(class_scope:CARTA.ErrorData)
  })
_sym_db.RegisterMessage(ErrorData)


# @@protoc_insertion_point(module_scope)