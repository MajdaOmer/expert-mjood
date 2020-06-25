# expert-mjood
 
This project is a simple example of how to use Python and Gstreamer and Gst Rtsp Server.
It contains three python file:
1.	RTSP server is launch Gstreamer pipeline for video or audio and prepare a rtsp url
2.	Main Server create an object from RTSP server, and serve the clients request specific media file
3.	Main client request and specific media file and gets the rtsp url  for it.
4.	Also VLC player can be used as client, in vlc click on media then click on open network stream  then enter the url of rtsp servr

System requirement:
•	Ubuntu 18
•	GStreamer 1.14.1
•	Python 3.6
•	Python pycairo package	
•	Python PyGObject  package
•	gst-rtsp-server-1.0_1.14.0-1_
This websites can be useful:
http://lifestyletransfer.com/how-to-install-gstreamer-on-ubuntu/
http://lifestyletransfer.com/how-to-install-gstreamer-python-bindings/
https://ubuntu.pkgs.org/18.04/ubuntu-universe-amd64/gir1.2-gst-rtsp-server-1.0_1.14.0-_amd64.deb.html


 
