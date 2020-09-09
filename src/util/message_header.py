# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import struct

import uuid
import numpy as np

from src.protobuf import defs_pb2
from src.protobuf import enums_pb2
from src.protobuf import register_viewer_pb2
from src.protobuf import open_file_pb2
from src.protobuf import region_histogram_pb2
from src.protobuf import region_requirements_pb2

# The ICD protocol version number
ICD_VERSION = 17

# struct EventHeader {
#     uint16_t type;
#     uint16_t icd_version;
#     uint32_t request_id;
# };
EVENT_HEADER = struct.Struct('HHI')

message_type_code_to_protobuf_obj = {
    enums_pb2.EventType.REGISTER_VIEWER: register_viewer_pb2.RegisterViewer,
    enums_pb2.EventType.REGISTER_VIEWER_ACK: register_viewer_pb2.RegisterViewerAck,
    enums_pb2.EventType.OPEN_FILE: open_file_pb2.OpenFile,
    enums_pb2.EventType.OPEN_FILE_ACK: open_file_pb2.OpenFileAck,
    enums_pb2.EventType.SET_HISTOGRAM_REQUIREMENTS: region_requirements_pb2.SetHistogramRequirements,
    enums_pb2.EventType.REGION_HISTOGRAM_DATA: region_histogram_pb2.RegionHistogramData
}

def add_message_header(msg, msg_type):
    """ Prefix a given protobuf message with its event header """
    header = EVENT_HEADER.pack(
        msg_type,
        ICD_VERSION,
        uuid.uuid4().int % np.iinfo(np.uint32()).max)
    payload = msg.SerializeToString()
    return header + payload

def strip_message_header(data):
    """ Remove event header from given message and parse protobuf object """
    message_type, icd_version, message_id = EVENT_HEADER.unpack(data[:8])
    message = message_type_code_to_protobuf_obj.get(message_type)()
    message.ParseFromString(data[8:])
    return (message_type, message_id, message)
