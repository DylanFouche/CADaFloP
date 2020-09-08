# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import uuid
import numpy as np

from src.protobuf import enums_pb2
from src.protobuf import register_viewer_pb2
from src.protobuf import open_file_pb2

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

def construct_open_file(file, directory):
    """ Construct an OPEN_FILE message """
    message = open_file_pb2.OpenFile()
    message.file = file
    message.directory = directory
    message_type = enums_pb2.EventType.OPEN_FILE
    return (message, message_type)

def construct_open_file_ack():
    """ Construct an OPEN_FILE_ACK message """
    message = open_file_pb2.OpenFileAck()
    message.success = True
    message_type = enums_pb2.EventType.OPEN_FILE_ACK
    return (message, message_type)
