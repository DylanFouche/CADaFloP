# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: set_image_channels.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import tiles_pb2 as tiles__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='set_image_channels.proto',
  package='CARTA',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18set_image_channels.proto\x12\x05\x43\x41RTA\x1a\x0btiles.proto\"u\n\x10SetImageChannels\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\x0f\x12\x0f\n\x07\x63hannel\x18\x02 \x01(\x0f\x12\x0e\n\x06stokes\x18\x03 \x01(\x0f\x12/\n\x0erequired_tiles\x18\x04 \x01(\x0b\x32\x17.CARTA.AddRequiredTilesb\x06proto3'
  ,
  dependencies=[tiles__pb2.DESCRIPTOR,])




_SETIMAGECHANNELS = _descriptor.Descriptor(
  name='SetImageChannels',
  full_name='CARTA.SetImageChannels',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_id', full_name='CARTA.SetImageChannels.file_id', index=0,
      number=1, type=15, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='channel', full_name='CARTA.SetImageChannels.channel', index=1,
      number=2, type=15, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stokes', full_name='CARTA.SetImageChannels.stokes', index=2,
      number=3, type=15, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='required_tiles', full_name='CARTA.SetImageChannels.required_tiles', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=48,
  serialized_end=165,
)

_SETIMAGECHANNELS.fields_by_name['required_tiles'].message_type = tiles__pb2._ADDREQUIREDTILES
DESCRIPTOR.message_types_by_name['SetImageChannels'] = _SETIMAGECHANNELS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SetImageChannels = _reflection.GeneratedProtocolMessageType('SetImageChannels', (_message.Message,), {
  'DESCRIPTOR' : _SETIMAGECHANNELS,
  '__module__' : 'set_image_channels_pb2'
  # @@protoc_insertion_point(class_scope:CARTA.SetImageChannels)
  })
_sym_db.RegisterMessage(SetImageChannels)


# @@protoc_insertion_point(module_scope)
