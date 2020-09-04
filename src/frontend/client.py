# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging

from src.protobuf import register_viewer_pb2

class Client:
    def __init__(self,port=3003):
        logging.info("[Client]\tStarting a client on port %s", port)
        while True:
            pass
