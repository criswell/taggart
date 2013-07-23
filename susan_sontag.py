#!/usr/bin/env python

import omero

from omero.gateway import BlitzGateway

user = 'taggart'
password = 'taggart'
host = 'localhost'

conn = BlitzGateway(user, password, host)


class TagHandler(object):
    """
    """
    def __init__(self, conn):
        """
        """
        self._conn = conn

    def list_tags(self):
        """
        """
        
