# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback

import asyncio
import websockets

from src.protobuf import register_viewer_pb2
from src.protobuf import enums_pb2

from src.util.message_provider import *
from src.util.message_header import *

class Client:

    def __init__(self, name, address, port):
        """ Create a client object with a connection to a server """
        self.name = name
        self.server = "ws://{}:{}/websocket".format(address, port)
        self.connect_to_server()

    def connect_to_server(self):
        """ Attempt to connect to server on given port and address """
        async def __connect_to_server(self):
            try:
                websocket = await websockets.connect(self.server, ping_interval=None)
                logging.info("\t[%s]\tConnected to server %s successfully.", self.name, self.server)
                return websocket
            except:
                logging.error("\t[%s]\tUnable to connect to server %s.", self.name, self.server)
                raise RuntimeError("Failed to connect to server.")

        self.ws = asyncio.get_event_loop().run_until_complete(__connect_to_server(self))

    def register_viewer(self):
        """ Send a REGISTER_VIEWER to server and wait for REGISTER_VIEWER_ACK response """
        async def __register_viewer(self):
            try:
                req, req_type = construct_register_viewer()
                await self.ws.send(add_message_header(req, req_type))
                logging.info("\t[%s]\tSent REGISTER_VIEWER with session id %s to server %s.", self.name, req.session_id, self.server)
                message = await self.ws.recv()
                ack_type, ack_id, ack = strip_message_header(message)
                if ack.success:
                    logging.info("\t[%s]\tGot a successful REGISTER_VIEWER_ACK with session id %s from server %s.", self.name, ack.session_id, self.server)
                else:
                    logging.warn("\t[%s]\tGot an unsuccessful REGISTER_VIEWER_ACK with session id %s from server %s. Message: %s", self.name, ack.session_id, self.server, ack.message)
            except:
                logging.error("\t[%s]\tUnable to register as a viewer with server %s.", self.name, self.server)
                traceback.print_exc()

        asyncio.get_event_loop().run_until_complete(__register_viewer(self))

    def open_file(self, file, directory):
        """ Send an OPEN_FILE to server and wait for OPEN_FILE_ACK response """
        async def __open_file(self):
            try:
                req, req_type = construct_open_file(file, directory)
                await self.ws.send(add_message_header(req, req_type))
                logging.info("\t[%s]\tSent OPEN_FILE for file %s to server %s.", self.name, req.directory + req.file, self.server)
                message = await self.ws.recv()
                ack_type, ack_id, ack = strip_message_header(message)
                if ack.success:
                    logging.info("\t[%s]\tGot a successful OPEN_FILE_ACK for file %s from server %s.", self.name, req.directory + req.file, self.server)
                else:
                    logging.warn("\t[%s]\tGot an unsuccessful OPEN_FILE_ACK for file %s from server %s. Message: %s", self.name, req.directory + req.file, self.server, ack.message)
            except:
                logging.error("\t[%s]\tUnable to open file %s on server %s.", self.name, req.directory + req.file, self.server)
                traceback.print_exc()

        asyncio.get_event_loop().run_until_complete(__open_file(self))
