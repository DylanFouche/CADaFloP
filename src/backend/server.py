# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import socket
import logging
import traceback

import numpy as np

from src.protobuf import register_viewer_pb2
from src.util.comms import *

def __on_register_viewer(conn, addr, msg_id, msg):
    """ Handle the REGISTER_VIEWER message """
    logging.info("\t[Server]\tGot REGISTER_VIEWER with session id %s from client %s.", msg.session_id, addr)
    ack = send_register_viewer_ack(conn, msg.session_id)
    logging.info("\t[Server]\tSent REGISTER_VIEWER_ACK with session id %s to client %s.", ack.session_id, addr)

message_type_code_to_event_handler = {
    enums_pb2.EventType.REGISTER_VIEWER: __on_register_viewer
}

def handle_message(conn, addr, msg_type, msg_id, msg):
    """ Decide which handler to invoke for the given message type """
    handler = message_type_code_to_event_handler.get(msg_type)
    handler(conn, addr, msg_id, msg)


class Server:

    def __init__(self, port, address):
        """ Open a socket on the given port and address, listen forever """

        logging.info("\t[Server]\tStarting a server on port %s.", port)

        # Open a TCP socket to listen on
        try:
            server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            server_socket.bind((address, port))
            server_socket.listen(1)
            logging.info("\t[Server]\tListening on port %s.", port)
        except:
            logging.error("\t[Server]\tUnable to listen on port %s.", port)

        # Wait for a client to connect
        client_socket, client_address = server_socket.accept()
        logging.info("\t[Server]\tConnection from %s has been established.", client_address)

        # Handle incoming messages
        while True:
            try:
                msg_type, msg_id, msg = recv_message(client_socket)
                handle_message(client_socket, client_address, msg_type, msg_id, msg)
            except:
                logging.error("\t[Server]\tUnable to process incoming message from client %s.", client_address)
                traceback.print_exc()


if __name__ == "__main__":
    server = Server()
