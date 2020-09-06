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
    def __init__(self, carta_port=3002, local_port=3003):

        # Connect to our backend server
        try:
            local_client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            local_client_socket.connect(('localhost', local_port))
            logging.info("\t[Client]\tConnected to Python server on %s successfully.", local_port)
        except:
            logging.error("\t[Client]\tUnable to connect to Python server on %s.", local_port)

        # Register as a viewer with our backend server
        try:
            msg = send_register_viewer(local_client_socket)
            logging.info("\t[Client]\tSent REGISTER_VIEWER with session id %s to Python server on %s.", msg.session_id, local_port)
            ack_type, ack_id, ack = recv_message(local_client_socket)
            logging.info("\t[Client]\tGot REGISTER_VIEWER_ACK with session id %s from Python server on %s.", ack.session_id, local_port)
        except:
            logging.error("\t[Client]\tUnable to register as a viewer with Python server on %s.", local_port)
            logging.error(traceback.print_exc())

            """
        # Connect to CARTA server
        try:
            carta_client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            carta_client_socket.connect(('localhost', carta_port))
            logging.info("\t[Client]\tConnected to CARTA server on %s successfully.", carta_port)
        except:
            logging.error("\t[Client]\tUnable to connect to CARTA server on %s.", carta_port)

        # Register as a viewer with CARTA server
        try:
            msg = send_register_viewer(carta_client_socket)
            logging.info("\t[Client]\tSent REGISTER_VIEWER with session id %s to CARTA server on %s.", msg.session_id, carta_port)
            ack_type, ack_id, ack = recv_message(carta_client_socket)
            logging.info("\t[Client]\tGot REGISTER_VIEWER_ACK with session id %s from CARTA server on %s.", ack.session_id, carta_port)
        except:
            logging.error("\t[Client]\tUnable to register as a viewer with CARTA server on %s.", carta_port)
            logging.error(traceback.print_exc())
            """
        while True:
            #Keep the ports open for now
            pass
