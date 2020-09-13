# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback

import asyncio
import websockets

import os

from src.util.message_provider import *
from src.util.message_header import *

class Client:

    def __init__(self, name, address, port, is_carta_client=False):
        """ Create a client object with a connection to a server """
        self.name = name
        self.server = "ws://{}:{}/websocket".format(address, port)
        self.carta = is_carta_client
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
                if self.carta:
                    # ignore default histogram sent after OPEN_FILE
                    discard = await self.ws.recv()
            except:
                logging.error("\t[%s]\tUnable to open file %s on server %s.", self.name, req.directory + req.file, self.server)
                traceback.print_exc()

        asyncio.get_event_loop().run_until_complete(__open_file(self))

    def get_region_histogram(self, num_bins=-1):
        """ Send a SET_HISTOGRAM_REQUIREMENTS and wait to recieve a REGION_HISTOGRAM_DATA. """
        async def __get_region_histogram(self):
            try:
                req, req_type = construct_set_histogram_requirements(num_bins)
                await self.ws.send(add_message_header(req, req_type))
                logging.info("\t[%s]\tSent SET_HISTOGRAM_REQUIREMENTS to server %s.", self.name, self.server)
                message = await self.ws.recv()
                histo_type, histo_id, histo = strip_message_header(message)
                logging.info("\t[%s]\tGot REGION_HISTOGRAM_DATA back from server %s.", self.name, self.server)
                return (histo.histograms[0].bins, histo.histograms[0].mean, histo.histograms[0].std_dev)

            except:
                logging.error("\t[%s]\tUnable to get region histogram from server %s.", self.name, self.server)
                traceback.print_exc()

        return asyncio.get_event_loop().run_until_complete(__get_region_histogram(self))

    def get_region_statistics(self):
        """ Send a SET_STATS_REQUIREMETNS and wait to recieve a REGION_STATS_DATA. """
        async def __get_region_statistics(self):
            try:
                req, req_type = construct_set_stats_requirements()
                await self.ws.send(add_message_header(req, req_type))
                logging.info("\t[%s]\tSent SET_STATS_REQUIREMETNS to server %s.", self.name, self.server)
                message = await self.ws.recv()
                stats_type, stats_id, stats = strip_message_header(message)
                logging.info("\t[%s]\tGot REGION_STATS_DATA back from server %s.", self.name, self.server)
                stat_list = []
                for stat in stats.statistics:
                    stat_list.append(stat.value)
                return stat_list

            except:
                logging.error("\t[%s]\tUnable to get region statistics from server %s.", self.name, self.server)
                traceback.print_exc()

        return asyncio.get_event_loop().run_until_complete(__get_region_statistics(self))

    def clear_cache_and_open_file_and_get_region_histogram(self, file, directory, num_bins=-1):
        """ Clear cache, open file and get histogram. Used in performance testing """
        os.system('echo "sync && echo 3 > /proc/sys/vm/drop_caches" | sudo bash')
        self.open_file(file, directory)
        return self.get_region_histogram(num_bins)
