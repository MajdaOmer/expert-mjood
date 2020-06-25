#!/usr/bin/env python3
import socket
import sys
import threading
import logging
import threading
from RTSPMediaServer import My_RTSP_Server

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

# videos and Audioes in my Store
Video1path = "MajdaPhdStoreTestingMediaData/AnaSV1.MP4"
Video2path = "MajdaPhdStoreTestingMediaData/caminandes-2-gran-dillama-x65-aacV2.mp4"
Video3path = "MajdaPhdStoreTestingMediaData/caminandes-3-llamigos-x265-aacV3.mp4"
Video4path = "MajdaPhdStoreTestingMediaData/big_buck_bunnyV4.mp4"
Audio1path = "MajdaPhdStoreTestingMediaData/BonnieTylerEclipseHeartA.mp3"
#this used when a request come to RTSP Server from a foreign clints like Vlc player from windowes or linux rather than My Client App
defultpath= Video1path

#Media Variables  ************************************************************
MediaPath = ""
Mediatype = ""

# Server Address Information *************************************************
HOST = '10.0.20.4'  # Standard loopback interface address (localhost)
PORT = 9090 # Port to listen on (non-privileged ports are > 1023)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
class Server:
    """Data (Video)sender server"""
    oldmsg = "None"
    rtspServer = My_RTSP_Server(HOST,"2000")

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the port
        logger.info("Server started on %s port %s", host, port)
        self.sock.bind((host, port))
        # Listen for incoming connections
        self.sock.listen(5)
        logger.info("Now listening for clients")
        while True:
            client,address = self.sock.accept()
            logger.info("Accepted Connection from: %s", client.getsockname())
            client_handler = threading.Thread(target=self.handle_client_connection, args=(client,))
            client_handler.start()

        self.sock.close()

    def handle_client_connection(self,client_socket):
        request="None"
        responseMedia_URL="None"
        # receive the response data (4096 is recommended buffer size)
        print(" handle_client_connection ..........................")

        request = client_socket.recv(4096)
        msg = request.decode()
        if msg != self.oldmsg:
            if msg == "video1":
                MediaPath = Video1path
                Mediatype = "H.264"
            elif msg == "video2":
                MediaPath = Video2path
                Mediatype = "H.265"
            elif msg == "video3":
                MediaPath = Video3path
                Mediatype = "H.265"
            elif msg == "video4":
                MediaPath = Video4path
                Mediatype = "H.264"
            elif msg == "audio1":
                MediaPath = Audio1path
                Mediatype = "MPEG-1_mp3"
            self.oldmsg = msg
            # Starting RTSP Server
            self.rtspServer.start_factory(MediaPath,Mediatype)
            responseMedia_URL=  self.rtspServer.getMedia_URL
            client_socket.send(responseMedia_URL.encode())

            client_socket.close()
            self.rtspServer.start()
        else:
            resMedia_URL = self.rtspServer.getMedia_URL
            client_socket.send(resMedia_URL.encode())
            client_socket.close()
           # self.rtspServer.start()

def MyMainServer():
    server = Server(HOST,PORT)
def MainRTSPServer():
    # for  requests come to RTSP Server from a foreign Vlc player or other foreign clints rather than my client App
    rtspServ = My_RTSP_Server(HOST, "2020")
    rtspServ.start_factory(defultpath, "H.264")
    rtspServ.start()

if __name__ == '__main__':
    t1 = threading.Thread(target=MyMainServer)
    t2 = threading.Thread(target=MainRTSPServer)
    t1.start()
    t2.start()


