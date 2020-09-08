# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import threading
import traceback

import numpy as np

import asyncio
import websockets

from src.protobuf import register_viewer_pb2
from src.protobuf import enums_pb2

from src.util.comms import *

async def __on_register_viewer(ws, msg):
    """ Handle the REGISTER_VIEWER message """
    logging.info("\t[Server]\tGot REGISTER_VIEWER with session id %s.", msg.session_id)
    ack, ack_type = construct_register_viewer_ack(msg.session_id)
    await ws.send(pack_message(ack, ack_type))
    logging.info("\t[Server]\tSent REGISTER_VIEWER_ACK with session id %s.", ack.session_id)

MESSAGE_TYPE_CODE_TO_EVENT_HANDLER = {
    enums_pb2.EventType.REGISTER_VIEWER: __on_register_viewer
}

class Server:

    async def __handle(self, websocket, path):

        logging.info("\t[Server]\tClient connection opened.")

        try:
            async for message in websocket:
                try:
                    message_type, message_id, message_payload = unpack_message(message)
                    handler = MESSAGE_TYPE_CODE_TO_EVENT_HANDLER.get(message_type)
                    await handler(websocket, message_payload)
                except:
                    logging.error("\t[Server]\tUnable to process message from client.")
                    traceback.print_exc()
        except:
            logging.warn("\t[Server]\tClient connection closed.")

    def __init__(self, address, port):

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        server = websockets.serve(self.__handle, address, port, loop=event_loop, ping_interval=None)

        logging.info("\t[Server]\tStarting a server on ws://%s:%s", address, port)

        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
