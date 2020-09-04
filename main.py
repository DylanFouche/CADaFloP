#!/usr/bin/python3

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import threading
import time
import sys

from src.frontend import client
from src.backend import server

def main():
    logging.info("\t[Main]\t\tStarting the server...")
    serverThread = threading.Thread(target=server.Server, daemon=True)
    serverThread.start()
    logging.info("\t[Main]\t\tCreated a server thread.")

    time.sleep(1)

    logging.info("\t[Main]\t\tStarting the client...")
    clientThread = threading.Thread(target=client.Client, daemon=True)
    clientThread.start()
    logging.info("\t[Main]\t\tCreated a client thread.")

    while True:
        pass

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    try:
        main()
    except KeyboardInterrupt:
        logging.warn("\t[Main]\t\tShutting down...")
        sys.exit(0)
