# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging
import time
import uuid

import numpy as np

from src.protobuf import register_viewer_pb2
from src.util.comms import *

class Client:
    def __init__(self, port=3003):
        logging.info("\t[Client]\tStarting a client on port %s.", port)

        try:
            clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            clientSocket.connect(('localhost', port))
            logging.info("\t[Client]\tConnected to server on %s successfully.", port)
        except:
            logging.error("\t[Client]\tUnable to connect to server on %s.", port)

        while True:
            msg = register_viewer_pb2.RegisterViewer()
            msg.session_id = np.uint32(uuid.uuid4().int % np.iinfo(np.uint32()).max)

            try:
                send_message(clientSocket, msg)
                logging.info("\t[Client]\tSent REGISTER_VIEWER with id %s to server on %s.", msg.session_id, port)
                ack = recv_message(clientSocket, register_viewer_pb2.RegisterViewerAck)
                logging.info("\t[Client]\tGot REGISTER_VIEWER_ACK with id %s from server on %s.", ack.session_id, port)
            except:
                logging.error("\t[Client]\tUnable to register as a viewer with server on %s.", port)

            time.sleep(5)
