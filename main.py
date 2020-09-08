#!/usr/bin/python3

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import argparse
import logging
import threading
import time
import sys

from src.frontend.client import *
from src.backend.server import *

option_string = """
What would you like to do?
0: REGISTER_VIEWER
1: OPEN_FILE
q: Quit the program
"""

def main(args):

    # Start a Dask server
    logging.info("\t[Main]\t\tStarting the server...")
    serverThread = threading.Thread(target=Server, args=(args.dask_address, args.dask_port, args.base), daemon=True)
    serverThread.start()
    logging.info("\t[Main]\t\tCreated a server thread successfully.")

    time.sleep(1)

    clients = set()

    # Create a Dask client
    logging.info("\t[Main]\t\tCreating a DASK client...")
    dask_client = Client("DaskClient", args.dask_address, args.dask_port)
    logging.info("\t[Main]\t\tCreated a DASK client object successfully.")
    clients.add(dask_client)

    if args.connect_to_carta:

        # Create a CARTA client
        logging.info("\t[Main]\t\tCreating a CARTA client...")
        carta_client = Client("CartaClient", args.carta_address, args.carta_port)
        logging.info("\t[Main]\t\tCreated a CARTA client object successfully.")
        clients.add(carta_client)

    time.sleep(1)

    while True:
        option = input(option_string)

        # Process user input
        if (option == '0'):
            for client in clients:
                client.register_viewer()

        elif (option == '1'):
            directory = input("Enter file directory (default ''): ")
            if not directory:
                directory = ''
            file = input("Enter file name (default 'h_m51_b_s05_drz_sci.fits'):")
            if not file:
                file = "h_m51_b_s05_drz_sci.fits"
            for client in clients:
                client.open_file(file, directory)

        elif (option == 'q'):
            sys.exit(0)

        else:
            print("Invalid option!")

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description='Interface with our Dask server and the CARTA server.')
    argparser.add_argument('-c', '--connect_to_carta', help="Establish a connection with CARTA back-end", default=False)
    argparser.add_argument('--dask_address', help="Host address for our Dask python server", default='localhost')
    argparser.add_argument('--carta_address', help="Host address for the CARTA back-end server", default='localhost')
    argparser.add_argument('--dask_port', help="Port for our Dask python server", default=3003)
    argparser.add_argument('--carta_port', help="Port for the CARTA back-end server", default=3002)
    argparser.add_argument('-b', '--base', help="Root directory of image data", default="/data/cadaflop/Data/")
    argparser.add_argument('-v', '--verbose', help="Enable verbose info logging to console", default=False)

    args = argparser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    try:
        main(args)
    except KeyboardInterrupt:
        logging.warn("\t[Main]\t\tShutting down...")
        sys.exit(0)
