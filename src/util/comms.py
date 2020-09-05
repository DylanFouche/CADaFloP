# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

# Reference: https://krpc.github.io/krpc/communication-protocols/tcpip.html

import logging
import traceback
import time
import uuid

import numpy as np

from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint

from src.protobuf import register_viewer_pb2
from src.protobuf import enums_pb2

import bitstruct

message_type_code_to_protobuf_obj = {
    enums_pb2.EventType.REGISTER_VIEWER: register_viewer_pb2.RegisterViewer,
    enums_pb2.EventType.REGISTER_VIEWER_ACK: register_viewer_pb2.RegisterViewerAck
}

header_format = bitstruct.compile('u16u16u32')

def encode_varint(value):
    """ Encode an int as a protobuf varint """
    data = []
    _VarintEncoder()(data.append, value, False)
    return b''.join(data)

def decode_varint(data):
    """ Decode a protobuf varint to an int """
    return _DecodeVarint(data, 0)[0]

def send_message(conn, msg_type, msg, prependSize=True):
    """ Send a message, prefixed with its message type and (optionally) size, to a TPC/IP socket """
    header = header_format.pack(msg_type, 14, uuid.uuid4().int % np.iinfo(np.uint32()).max)
    payload = msg.SerializeToString()
    if prependSize:
        size = encode_varint(len(payload))
        payload = size + payload
    conn.send(header + payload)

def recv_message(conn):
    """ Receive a message, prefixed with its message type and size, from a TCP/IP socket """
    data = b''
    # Recieve the message header
    while True:
        try:
            data += conn.recv(8)
            break
        except IndexError:
            pass
    # Get message type
    message_type, icd_version, message_id = header_format.unpack(data)
    # Recieve payload size
    data = conn.recv(1)
    size = decode_varint(data)
    # Recieve and decode payload
    data = conn.recv(size)
    message = message_type_code_to_protobuf_obj.get(message_type)()
    message.ParseFromString(data)
    # Return message type, message id, and protobuf message object
    return (message_type, message_id, message)

def send_register_viewer(conn):
    """ Construct and send a REGISTER_VIEWER message """
    message = register_viewer_pb2.RegisterViewer()
    message.session_id = np.uint32(uuid.uuid4().int % np.iinfo(np.uint32()).max)
    send_message(conn, enums_pb2.EventType.REGISTER_VIEWER, message)
    return message

def send_register_viewer_ack(conn, client_session_id):
    """ Construct and send a REGISTER_VIEWER_ACK message """
    message = register_viewer_pb2.RegisterViewerAck()
    message.session_id = client_session_id
    message.success = True
    send_message(conn, enums_pb2.EventType.REGISTER_VIEWER_ACK, message)
    return message
