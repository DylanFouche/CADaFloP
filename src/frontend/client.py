# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging
import traceback
import time

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

            time.sleep(5)

            try:
                msg = send_register_viewer(clientSocket)
                logging.info("\t[Client]\tSent REGISTER_VIEWER with session id %s to server on %s.", msg.session_id, port)
                ack_type, ack_id, ack = recv_message(clientSocket)
                logging.info("\t[Client]\tGot REGISTER_VIEWER_ACK with session id %s from server on %s.", ack.session_id, port)
            except:
                logging.error("\t[Client]\tUnable to register as a viewer with server on %s.", port)
                logging.error(traceback.print_exc())
