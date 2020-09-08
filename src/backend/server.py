# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import threading
import traceback

import numpy as np

import asyncio
import websockets

from src.protobuf import enums_pb2
from src.protobuf import register_viewer_pb2
from src.protobuf import open_file_pb2


from src.backend.image import Image

from src.util.comms import *

class Server:

    async def __on_register_viewer(self, ws, msg):
        """ Handle the REGISTER_VIEWER message """
        logging.info("\t[Server]\tGot REGISTER_VIEWER with session id %s.", msg.session_id)
        ack, ack_type = construct_register_viewer_ack(msg.session_id)
        await ws.send(pack_message(ack, ack_type))
        logging.info("\t[Server]\tSent REGISTER_VIEWER_ACK with session id %s.", ack.session_id)

    async def __on_open_file(self, ws, msg):
        """ Handle the OPEN_FILE message """
        logging.info("\t[Server]\tGot OPEN_FILE with file %s and directory %s.", msg.file, msg.directory)
        ack, ack_type = construct_open_file_ack()
        try:
            self.image = Image(self.base + msg.directory + msg.file)
            logging.info("\t[Server]\tOpened file %s successfully.", msg.directory + msg.file)
        except:
            ack.success = False
            logging.error("\t[Server]\tUnable to open file %s.", msg.directory + msg.file)
            traceback.print_exc()
        await ws.send(pack_message(ack, ack_type))
        logging.info("\t[Server]\tSent OPEN_FILE_ACK.")

    MESSAGE_TYPE_CODE_TO_EVENT_HANDLER = {
        enums_pb2.EventType.REGISTER_VIEWER: __on_register_viewer,
        enums_pb2.EventType.OPEN_FILE: __on_open_file
    }

    async def __serve(self, websocket, path):
        """ Serve a new client connection """
        logging.info("\t[Server]\tClient connection opened.")
        try:
            async for message in websocket:
                try:
                    message_type, message_id, message_payload = unpack_message(message)
                    handler = self.MESSAGE_TYPE_CODE_TO_EVENT_HANDLER.get(message_type)
                    await handler(self, websocket, message_payload)
                except:
                    logging.error("\t[Server]\tUnable to process message from client.")
                    traceback.print_exc()
        except:
            logging.warn("\t[Server]\tClient connection closed.")

    def __init__(self, address, port, base):
        """ Start a server on given address:port and run forever """
        self.image = None
        self.base = base

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        server = websockets.serve(self.__serve, address, port, loop=event_loop, ping_interval=None)

        logging.info("\t[Server]\tStarting a server on ws://%s:%s", address, port)

        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
