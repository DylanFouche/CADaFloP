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

    def __init__(self, name, port, address):
        """ Create a client object with a connection to a server """
        self.name = name
        self.server_port = port
        self.server_address = address
        self.conn = self.__connect_to_server(port, address)

    def __connect_to_server(self, port, address):
        """ Attempt to connect to server on given port and address """
        try:
            conn = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            conn.connect((address, port))
            logging.info("\t[%s]\tConnected to server on %s successfully.", self.name, self.server_port)
        except:
            logging.error("\t[%s]\tUnable to connect to server on %s.", self.name, self.server_port)
            raise RuntimeError("Failed to connect to server.")
        return conn

    def register_viewer(self):
        """ Send a REGISTER_VIEWER to server and wait for REGISTER_VIEWER_ACK response """
        try:
            req = send_register_viewer(self.conn)
            logging.info("\t[%s]\tSent REGISTER_VIEWER with session id %s to server on %s.", self.name, req.session_id, self.server_port)
            ack_type, ack_id, ack = recv_message(self.conn)
            logging.info("\t[%s]\tGot REGISTER_VIEWER_ACK with session id %s from server on %s.", self.name, ack.session_id, self.server_port)
        except:
            logging.error("\t[%s]\tUnable to register as a viewer with server on %s.", self.name, self.server_port)
            traceback.print_exc()
