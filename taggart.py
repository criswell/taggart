# -*- coding: utf-8 -*-

"""
Foo
"""

from omero.gateway import BlitzGateway
from goatools.obo_parser import GODag


class Taggart(object):
    """
    Bar
    """

    def __init__(self, username=None, password=None, host='localhost'):
        """
        """
        self.username = username
        self.password = username
        self.host = host
        self._conn = None

    def _test_set(self):
        """
        """
        if self.username is None:
            raise Exception('Username is not set!')
        if self.password is None:
            raise Exception('Password is not set!')
        if self.host is None:
            raise Exception('Host is not set!')

    def _lazy_connect(self):
        """
        """
        _test_set()
        
        if self._conn is None:
            self._conn = BlitzGateway(self.username, self.password, \
                         host=self.host)

        return self._conn.connect()

    def import_from_obo(self, filename):
        """
        """
        g = GODag(obo_file=filename)
        # FIXME XXX - This is terrible. We can make something better
        # This is a first-stab inefficient hunk of crap
        tag_groups = {}
        tag_group_descriptions = ()
        tags_wo_groups = []
        if _lazy_connect():
            for term in g:
                if term.namespace and len(term.namespace) > 0:
                    if not tag_groups.has_key(term.namespace):
                        tag_groups[term.namespace] = []
                        tag_group_descriptions[term.namespace] = term.definition
                    

        else:
            raise Exception('Could not connect, and had no internal exception!')


