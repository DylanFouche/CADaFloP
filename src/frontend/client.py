# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback

import asyncio
import websockets

from src.protobuf import register_viewer_pb2
from src.protobuf import enums_pb2

from src.util.comms import *


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
                await self.ws.send(pack_message(req, req_type))
                logging.info("\t[%s]\tSent REGISTER_VIEWER with session id %s to server %s.", self.name, req.session_id, self.server)
                message = await self.ws.recv()
                ack_type, ack_id, ack = unpack_message(message)
                logging.info("\t[%s]\tGot REGISTER_VIEWER_ACK with session id %s from server %s.", self.name, ack.session_id, self.server)
            except:
                logging.error("\t[%s]\tUnable to register as a viewer with server %s.", self.name, self.server)
                traceback.print_exc()

        asyncio.get_event_loop().run_until_complete(__register_viewer(self))
