#!/usr/bin/python3

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import threading
import time

from src.frontend import client
from src.backend import server

def main():
    logging.info("[Main]\tStarting the server...")
    serverThread = threading.Thread(target=server.Server, daemon=True)
    serverThread.start()
    logging.info("[Main]\tCreated a server thread.")

    logging.info("[Main]\tStarting the client...")
    clientThread = threading.Thread(target=client.Client, daemon=True)
    clientThread.start()
    logging.info("[Main]\tCreated a client thread.")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
