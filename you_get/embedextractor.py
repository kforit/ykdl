#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import import_module
from .common import alias

class EmbedExtractor():
    """
    this class is to help video embed site to handle
    video from other site.
    we just need to know the source site name, and video ID
    that's enough.
    with site name and VID, develop can easily to find out the real URL

    because embed site don't have video info, so they don't need stream_info.
    """

    def __init__(self):
        self.video_info = []
        self.title = None

    def prepare(self):
        """
        this API is to do real job to get site and VID
        sometimes title
        MUST override!!
        """
        pass

    def prepare_playlist(self):
        """
        this API is to do real job to get site and VID
        sometimes title
        MUST override!!
        """
        pass

    def download(self, url, param):
        self.param = param
        if isinstance(url, str) and url.startswith('http'):
            self.url = url
        self.video_info = []
        self.prepare()

        if not self.video_info:
            raise NotImplementedError(self.url + " is not supported")

        if self.video_info:
            n = 0
            for v in self.video_info:
                site, vid = v
                if site in alias.keys():
                    site = alias[site]
                s = import_module('.'.join(['you_get','extractors',site])).site
                s.title = self.title + " %02d" % n
                s.download(vid, self.param)
                n += 1

    def download_playlist(self, url, param):
        self.param = param
        if isinstance(url, str) and url.startswith('http'):
            self.url = url
        self.video_info = []
        self.prepare_playlist()

        if not self.video_info:
            raise NotImplementedError('Playlist is not supported for ' + self.name)

        if self.video_info:
            for v in self.video_info:
                site, vid = v
                if site in alias.keys():
                    site = alias[site]
                s = import_module('.'.join(['you_get','extractors',site])).site
                s.download_playlist(vid, self.param)
