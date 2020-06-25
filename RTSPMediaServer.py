#! /usr/bin/python

# Media RTSP Server based on Gestreamer
# Copyright (C) 2020  Majda Omer Elbasheer <majda.omer@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
import logging
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GObject, Gst, GstRtspServer

logger = logging.getLogger('logic.gstreamer.RTSPServer')
main_loop = GObject.MainLoop()  # define G main loop
GObject.threads_init()
Gst.init(None)


class MyMediaFactory(GstRtspServer.RTSPMediaFactory):
    # make a media factory for a media stream. The default media factory can use gst-launch syntax to
    # create pipelines.
    # #any launch line works as long as it contains elements named pay%d.
    # Each element with pay%d names will be a stream
    def __init__(self, mediaPath, mediatype):
        GstRtspServer.RTSPMediaFactory.__init__(self)
        if mediatype == "H.264":
            self.create_MediaPipelineH264(mediaPath)
        elif mediatype == "H.265":
            self.create_MediaPipelineH265(mediaPath)
        elif mediatype == "MPEG-1_mp3":
            self.create_MediaPipelineMPEG_mp3(mediaPath)
        self.set_launch(self.launshStr)

    def create_MediaPipelineH264(self, url):
        self.launshStr = "( filesrc location=" + url + " ! qtdemux name=d " \
                                                       "d. ! queue ! rtph264pay pt=96 name=pay0 d. ! queue ! rtpmp4apay pt=97 name=pay1 )"

    def create_MediaPipelineH265(self, url):
        self.launshStr = "( filesrc location=" + url + " ! qtdemux name=d " \
                                                       "d. ! queue ! " \
                                                       "rtph265pay pt=96 name=pay0 d. ! queue ! rtpmp4apay pt=97 name=pay1 )"

    def create_MediaPipelineMPEG_mp3(self, url):
        self.launshStr = "(  filesrc location=" + url + " ! mpegaudioparse  ! rtpmpapay name = pay0 pt = 97 )"
class My_RTSP_Server:
    Media_URL = "None"
    DefultAddress="10.0.0.4"
    DefultPort = "2020"
    def __init__(self,Address,Port):
        self.Address=Address
        self.Port=Port
        self.server = GstRtspServer.RTSPServer()
        logger.info('Creating Majda RTSP server')
    def start_factory(self, MediaPath, mediatype):
        logger.warning('Starting Majda RTSP server')
        # Setting Server Address and service
        self.server.set_address(self.Address)
        self.server.set_service(self.Port)
        self.create_factory(MediaPath, mediatype)
        self.server.connect("client-connected", self.do_client_connected)
    def start(self):
        # start serving
        # attach the server to the default maincontext
        self.server.attach(None)
        main_loop.run()

    @property
    def getMedia_URL(self):
        return self.Media_URL

    def close(self):
        GObject.source_remove(self.server_id)
        logger.warning('Stop RTSP server')

    def create_factory(self, uri, mediatype):
        logger.warning('Creating RTSP Factory for Majda Video')
        factory = MyMediaFactory(uri, mediatype)
        # the line Below  Make all clients share the playing media simultaneously
        # factory.set_shared(True)
        # get the mount points for this server, every server has a default object that be used to
        # map uri mount points to media factories
        mounts = self.server.get_mount_points()
        # attach the media factory to the /media url
        mounts.add_factory("/media", factory)
        self.Media_URL = 'rtsp://{0}:{1}/media'.format(self.server.get_address(), self.server.get_service())
        logger.warning(
            'stream ready at rtsp://{0}:{1}/media'.format(self.server.get_address(), self.server.get_service()))


    def remove_factory(self, uri):
        logger.warning('Remove RTSP Factory: ', uri)
        mounts = self.server.get_mount_points()
        mounts.remove_factory('/' + uri)

    def do_client_connected(self, arg1, arg2):
        logger.warning('Rtsp client connected.')


