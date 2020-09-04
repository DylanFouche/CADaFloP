# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging

from src.protobuf import register_viewer_pb2

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

        while True:
            clientSocket, clientAddress = serverSocket.accept()
            logging.info("\t[Server]\tConnection from %s has been established.", clientAddress)
