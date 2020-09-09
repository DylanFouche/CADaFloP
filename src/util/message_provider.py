# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import uuid
import numpy as np

from src.protobuf import defs_pb2
from src.protobuf import enums_pb2
from src.protobuf import register_viewer_pb2
from src.protobuf import open_file_pb2
from src.protobuf import region_histogram_pb2
from src.protobuf import region_requirements_pb2

from src.util.message_header import *

def construct_register_viewer():
    """ Construct a REGISTER_VIEWER message """
    message_type = enums_pb2.EventType.REGISTER_VIEWER
    message = register_viewer_pb2.RegisterViewer()
    message.session_id = np.uint32(uuid.uuid4().int % np.iinfo(np.uint32()).max)
    return (message, message_type)

def construct_register_viewer_ack(client_session_id):
    """ Construct a REGISTER_VIEWER_ACK message """
    message_type = enums_pb2.EventType.REGISTER_VIEWER_ACK
    message = register_viewer_pb2.RegisterViewerAck()
    message.session_id = client_session_id
    message.success = True
    return (message, message_type)

def construct_open_file(file, directory):
    """ Construct an OPEN_FILE message """
    message_type = enums_pb2.EventType.OPEN_FILE
    message = open_file_pb2.OpenFile()
    message.file = file
    message.directory = directory
    message.file_id = 1
    return (message, message_type)

def construct_open_file_ack():
    """ Construct an OPEN_FILE_ACK message """
    message_type = enums_pb2.EventType.OPEN_FILE_ACK
    message = open_file_pb2.OpenFileAck()
    message.success = True
    return (message, message_type)

def construct_set_histogram_requirements(num_bins):
    """ Construct a SET_HISTOGRAM_REQUIREMENTS message """
    message_type = enums_pb2.EventType.SET_HISTOGRAM_REQUIREMENTS
    message = region_requirements_pb2.SetHistogramRequirements()
    message.file_id = 1
    message.region_id = -1
    histogram_config = region_requirements_pb2.SetHistogramRequirements.HistogramConfig()
    histogram_config.channel = -1
    histogram_config.num_bins = num_bins
    message.histograms.append(histogram_config)
    return (message, message_type)

def construct_region_histogram_data(num_bins, bins, mean, std_dev):
    """ Construct a REGION_HISTOGRAM_DATA message """
    message_type = enums_pb2.EventType.REGION_HISTOGRAM_DATA
    message = region_histogram_pb2.RegionHistogramData()
    message.file_id = 1
    message.region_id = -1
    message.progress = 1
    histogram = defs_pb2.Histogram()
    histogram.num_bins = num_bins
    histogram.bins.extend(bins)
    histogram.mean = mean
    histogram.std_dev = std_dev
    message.histograms.append(histogram)
    return (message, message_type)
