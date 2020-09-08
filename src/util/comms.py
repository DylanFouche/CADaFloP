# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback
import time
import uuid
import struct

import asyncio
import websockets

import numpy as np

from src.protobuf import register_viewer_pb2
from src.protobuf import enums_pb2

message_type_code_to_protobuf_obj = {
    enums_pb2.EventType.REGISTER_VIEWER: register_viewer_pb2.RegisterViewer,
    enums_pb2.EventType.REGISTER_VIEWER_ACK: register_viewer_pb2.RegisterViewerAck
}

ICD_VERSION = 17

EVENT_HEADER = struct.Struct('HHI')

def pack_message(msg, msg_type):
    """ Prefix a given protobuf message with a header """
    header = EVENT_HEADER.pack(msg_type, 14, uuid.uuid4().int % np.iinfo(np.uint32()).max)
    payload = msg.SerializeToString()
    return header + payload

def unpack_message(data):
    """ Remove header from given message and parse protobuf """
    message_type, icd_version, message_id = EVENT_HEADER.unpack(data[:8])
    message = message_type_code_to_protobuf_obj.get(message_type)()
    message.ParseFromString(data[8:])
    return (message_type, message_id, message)

def construct_register_viewer():
    """ Construct a REGISTER_VIEWER message """
    message = register_viewer_pb2.RegisterViewer()
    message.session_id = np.uint32(uuid.uuid4().int % np.iinfo(np.uint32()).max)
    message_type = enums_pb2.EventType.REGISTER_VIEWER
    return (message, message_type)

def construct_register_viewer_ack(client_session_id):
    """ Construct a REGISTER_VIEWER_ACK message """
    message = register_viewer_pb2.RegisterViewerAck()
    message.session_id = client_session_id
    message.success = True
    message_type = enums_pb2.EventType.REGISTER_VIEWER_ACK
    return (message, message_type)
