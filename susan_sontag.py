#!/usr/bin/env python

import omero

from omero.gateway import BlitzGateway

user = 'taggart'
password = 'taggart'
host = 'localhost'

conn = BlitzGateway(user, password, host)
