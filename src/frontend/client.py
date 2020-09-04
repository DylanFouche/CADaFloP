# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging

from src.protobuf import register_viewer_pb2

class Client:
    def __init__(self, port=3003):
        logging.info("\t[Client]\tStarting a client on port %s.", port)

        try:
            clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            clientSocket.connect(('localhost', port))
            logging.info("\t[Client]\tConnected to server on %s successfully.", port)
        except:
            logging.error("\t[Client]\tUnable to connect to server on %s.", port)
