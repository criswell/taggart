#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Tag plugin for command-line tag manipulation

   :author: Sam Hart <sam@glencoesoftware.com>

   Copyright (C) 2013 Glencoe Software, Inc. All rights reserved.
   Use is subject to license terms supplied in LICENSE.txt

"""
from omero.cli import BaseControl, CLI, ExceptionHandler

HELP="""Manage OMERO user tags.

Foo

Examples:

    bar
    snaz

"""

def pagetext(text_lined, num_lines=25):
    for index,line in enumerate(text_lined):
        if index % num_lines == 0 and index:
            input=raw_input("Hit any key to continue press q to quit")
            if input.lower() == 'q':
                break
            else:
                print line

class TagControl(BaseControl):

    def _configure(self, parser):

        self.exc = ExceptionHandler()

        parser.add_login_arguments()
        sub = parser.sub()

        list_g = parser.add(sub, self.list_groups, help="List groups")
        list_g = parser.add(sub, self.list_groups_md, help="List groups_md")
        list_g.add_argument("--foo", action="store_true", default=False, \
            help="Placeholder for future option")
        list_g.add_login_arguments()

    def list_groups(self, args):
        client = self.ctx.conn(args)
        session = client.getSession()
        query = session.getQueryService()
        sql = """
            select aal.parent.id, aal.child.id
            from AnnotationAnnotationLink aal
            inner join aal.parent ann
            where ann.ns=:ns
        """


    def list_groups_md(self, args):
        #self.ctx.out("In list groups- whee!")
        c = self.ctx.conn(args)
        s = c.getSession()
        metadata = s.getMetadataService()
        for el in metadata.loadTagSets(None):
            print "%s : %s" % (el.getId().getValue(), el.getTextValue().getValue())


try:
    register("tag", TagControl, HELP)
except NameError:
    if __name__ == "__main__":
        cli = CLI()
        cli.register("user", TagControl, HELP)
        cli.invoke(sys.argv[1:])
