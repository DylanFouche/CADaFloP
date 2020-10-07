# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback

import asyncio
import websockets

import dask.distributed

from src.protobuf import enums_pb2

from src.util.message_provider import *
from src.util.message_header import *

from src.backend.image import Image


class Server:
    """A server object that runs forever to accept and serve incoming websocket connections from clients."""

    async def __on_register_viewer(self, ws, msg):
        """Handle the REGISTER_VIEWER message.

        :param ws: the client websocket object
        :param msg: the client message recieved

        """
        logging.info(
            "\t[Server]\tGot REGISTER_VIEWER with session id %s.", msg.session_id)
        ack, ack_type = construct_register_viewer_ack(msg.session_id)
        await ws.send(add_message_header(ack, ack_type))
        logging.info(
            "\t[Server]\tSent REGISTER_VIEWER_ACK with session id %s.", ack.session_id)

    async def __on_open_file(self, ws, msg):
        """Handle the OPEN_FILE message.

        :param ws: the client websocket object
        :param msg: the client message recieved

        """
        logging.info(
            "\t[Server]\tGot OPEN_FILE with file %s and directory %s.", msg.file, msg.directory)
        ack, ack_type = construct_open_file_ack()
        try:
            if self.image is None or not (msg.directory + msg.file == self.image.filename and self.cache):
                self.image = Image(msg.directory + msg.file)
                if self.client is not None:
                    self.image.data = self.client.persist(self.image.data)
                logging.info(
                    "\t[Server]\tOpened file %s successfully.", msg.directory + msg.file)
        except:
            ack.success = False
            logging.error("\t[Server]\tUnable to open file %s.",
                          msg.directory + msg.file)
            traceback.print_exc()
        await ws.send(add_message_header(ack, ack_type))
        logging.info("\t[Server]\tSent OPEN_FILE_ACK.")

    async def __on_set_histogram_requirements(self, ws, msg):
        """Handle the SET_HISTOGRAM_REQUIREMENTS message.

        :param ws: the client websocket object
        :param msg: the client message recieved

        """
        logging.info("\t[Server]\tGot SET_HISTOGRAM_REQUIREMENTS.")
        try:
            histo_num_bins = msg.histograms[0].num_bins if msg.histograms[0].num_bins > 0 else None
            raw_histogram = self.image.get_region_histogram(
                bins=histo_num_bins)
            mean = self.image.get_mean()
            std_dev = self.image.get_std_dev()
            histo, histo_type = construct_region_histogram_data(
                histo_num_bins, raw_histogram, mean, std_dev)
            await ws.send(add_message_header(histo, histo_type))
            logging.info("\t[Server]\tSent REGION_HISTOGRAM_DATA.")
        except:
            logging.error("\t[Server]\tUnable to compute region histogram")
            traceback.print_exc()

    async def __on_set_statistics_requirements(self, ws, msg):
        """Handle the SET_STATS_REQUIREMENTS message.

        :param ws: the client websocket object
        :param msg: the client message recieved

        """
        logging.info("\t[Server]\tGot SET_STATS_REQUIREMENTS.")
        try:
            raw_stats = self.image.get_region_statistics()
            stats, stats_type = construct_region_stats_data(raw_stats)
            await ws.send(add_message_header(stats, stats_type))
            logging.info("\t[Server]\tSent REGION_STATS_DATA.")
        except:
            logging.error("\t[Server]\tUnable to compute region statistics")
            traceback.print_exc()

    MESSAGE_TYPE_CODE_TO_EVENT_HANDLER = {
        enums_pb2.EventType.REGISTER_VIEWER:
            __on_register_viewer,
        enums_pb2.EventType.OPEN_FILE:
            __on_open_file,
        enums_pb2.EventType.SET_HISTOGRAM_REQUIREMENTS:
            __on_set_histogram_requirements,
        enums_pb2.EventType.SET_STATS_REQUIREMENTS:
            __on_set_statistics_requirements
    }

    async def __serve(self, websocket, path):
        """Serve a new client connection.

        :param websocket: the client websocket object
        :param path: the path to the new client

        """
        logging.info("\t[Server]\tClient connection opened.")
        try:
            async for message in websocket:
                try:
                    message_type, message_id, message_payload = strip_message_header(message)
                    handler = self.MESSAGE_TYPE_CODE_TO_EVENT_HANDLER.get(message_type)
                    await handler(self, websocket, message_payload)
                except:
                    logging.error(
                        "\t[Server]\tUnable to process message from client.")
                    traceback.print_exc()
        except:
            logging.warn("\t[Server]\tClient connection closed.")

    def __init__(self, address, port, cluster=False, cache=True):
        """Start a server on given address:port and run forever.

        :param address: the address of the server
        :param port: the port number of the server
        :param cluster: start the dask.distributed scheduler using a cluster of machines (Default value = False)
        :param cache: don't read in the same image from disk more than once (Default value = True)

        """
        self.image = None
        self.cache = cache

        if cluster:
            # Instantiate an unmanaged cluster for Dask
            self.cluster = dask.distributed.SSHCluster(
                ['localhost',       # scheduler
                 '192.168.80.12',   # worker 0
                 '192.168.80.13',   # worker 1
                 '192.168.80.14'])  # worker 2
            self.client = dask.distributed.Client(self.cluster)
        else:
            # Use the default Dask local client
            self.client = None

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        server = websockets.serve(
            self.__serve, address, port, loop=event_loop, ping_interval=None)

        logging.info(
            "\t[Server]\tStarting a server on ws://%s:%s", address, port)

        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
