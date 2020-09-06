# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

# Reference: https://krpc.github.io/krpc/communication-protocols/tcpip.html

import logging
import traceback
import time
import uuid

import numpy as np

from src.protobuf import register_viewer_pb2
from src.protobuf import enums_pb2

import bitstruct

message_type_code_to_protobuf_obj = {
    enums_pb2.EventType.REGISTER_VIEWER: register_viewer_pb2.RegisterViewer,
    enums_pb2.EventType.REGISTER_VIEWER_ACK: register_viewer_pb2.RegisterViewerAck
}

header_format = bitstruct.compile('u16u16u32')

def recv_message(conn):
    """ Receive a message with header from a TCP/IP socket """
    data = b''
    # Recieve the message header
    while True:
        try:
            data += conn.recv(8)
            if len(data) > 0:
                message_type, icd_version, message_id = header_format.unpack(data)
                break
        except IndexError:
            pass
    # Recieve and decode payload
    data = conn.recv(1024)
    message = message_type_code_to_protobuf_obj.get(message_type)()
    message.ParseFromString(data)
    # Return message type, message id, and protobuf message object
    return (message_type, message_id, message)

def __send_message(conn, msg_type, msg):
    """ Send a message with header to a TPC/IP socket """
    header = header_format.pack(msg_type, 14, uuid.uuid4().int % np.iinfo(np.uint32()).max)
    payload = msg.SerializeToString()
    conn.send(header + payload)

def send_register_viewer(conn):
    """ Construct and send a REGISTER_VIEWER message """
    message = register_viewer_pb2.RegisterViewer()
    message.session_id = np.uint32(uuid.uuid4().int % np.iinfo(np.uint32()).max)
    __send_message(conn, enums_pb2.EventType.REGISTER_VIEWER, message)
    return message

def send_register_viewer_ack(conn, client_session_id):
    """ Construct and send a REGISTER_VIEWER_ACK message """
    message = register_viewer_pb2.RegisterViewerAck()
    message.session_id = client_session_id
    message.success = True
    __send_message(conn, enums_pb2.EventType.REGISTER_VIEWER_ACK, message)
    return message
