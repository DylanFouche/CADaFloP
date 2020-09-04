# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging

import numpy as np

from src.protobuf import register_viewer_pb2
from src.util.comms import *

class Server:
    def __init__(self, port=3003):
        logging.info("\t[Server]\tStarting a server on port %s.", port)

        try:
            serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            serverSocket.bind(('localhost', port))
            serverSocket.listen(1)
            logging.info("\t[Server]\tListening on port %s.", port)
        except:
            logging.error("\t[Server]\tUnable to listen on port %s.", port)

        clientSocket, clientAddress = serverSocket.accept()
        logging.info("\t[Server]\tConnection from %s has been established.", clientAddress)

        while True:
            try:
                msg = recv_message(clientSocket, register_viewer_pb2.RegisterViewer)
                logging.info("\t[Server]\tClient %s registered as a viewer with id %s.", clientAddress, msg.session_id)

                ack = register_viewer_pb2.RegisterViewerAck()
                ack.session_id = msg.session_id
                send_message(clientSocket, ack)
                logging.info("\t[Server]\tSent REGISTER_VIEWER_ACK for id %s to client %s.", ack.session_id, clientAddress)
            except:
                logging.error("\t[Server]\tUnable to process incoming message from client %s.", clientAddress)
