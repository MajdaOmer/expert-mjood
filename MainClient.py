
#!/usr/bin/env python3
import queue
import socket
import threading
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

HOST = '10.0.20.4'  # Standard loopback interface address (localhost)
PORT = 9090  # Port to listen on (non-privileged ports are > 1023)
data_queue = ""
class Client:
     """Data receiver client"""

     def __init__(self, address, port, data_queue):
         self.data_queue = data_queue
         # Create a TCP/IP socket
         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         # Connect the socket to the port where the server is listening
         logger.info("Connecting to %s port %s", address, port)
         self.sock.connect((address, port))
         """Handles receiving, parsing, and queueing data"""
         logger.info("New data receivering started.")
         # send some data (in this case is My Name)
         self.sock.send(self.data_queue.encode())
         self.data = self.sock.recv(4096)
         print(self.data.decode())
         self.sock.close()

if __name__ == '__main__':
    data_queue="video2"
    client = Client(HOST,PORT,data_queue)

