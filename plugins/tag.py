#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Tag plugin for command-line tag manipulation

   :author: Sam Hart <sam@glencoesoftware.com>

   Copyright (C) 2013 Glencoe Software, Inc. All rights reserved.
   Use is subject to license terms supplied in LICENSE.txt

"""

import platform

import omero
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

def determine_pagination():
    """
    Will attempt to determine console length based upon the current platform.

    Returns the pagination length.
    """
    lines = 25 # The default if we can't figure it out

    this_system = platform.system().lower()

    try:
        if this_system in ['linux', 'darwin', 'macosx', 'cygwin']:
            #
        elif this_system in ['windows', 'win32']:
            #
    except:
        # Possible evil to ignore what the error was, but, truthfully,
        # the reason we do so is because it means it's a platform we
        # don't have support for, or a platform we should have support
        # for but which has some non-standard witch-craftery going on
        sys.ctx.out("Could not determine the console length.")

    return lines



class TagControl(BaseControl):

    def _configure(self, parser):

        self.exc = ExceptionHandler()

        parser.add_login_arguments()
        sub = parser.sub()

        list_g = parser.add(sub, self.list_groups, help="List groups")
        list_gd = parser.add(sub, self.list_groups_md, help="List groups_md")

        sefl.add_standard_params(list_g. list_gd)

        list_g.add_login_arguments()

    def add_standard_params(self, parser):
        parser.add_argument("--admin", action="store_true", default=False, \
            help="Perform action as an administrator")
        parser.add_argument("--nopage", action="store_true", default=False, \
            help="Disable pagination")

    def list_groups(self, args):
        params = omero.sys.ParametersI()
        params.addString('ns', omero.constants.metadata.NSINSIGHTTAGSET)
        ice_map = dict()
        #import pdb; pdb.set_trace()
        if args.admin:
            ice_map["omero.group"]="-1"

        client = self.ctx.conn(args)
        session = client.getSession()
        query = session.getQueryService()
        sql = """
            select aal.parent.id, aal.child.id
            from AnnotationAnnotationLink aal
            inner join aal.parent ann
            where ann.ns=:ns
        """

        children = set()
        mapping = dict()
        for element in query.projection(sql, params, ice_map):
            parent = element[0].getValue()
            child = element[1].getValue()
            children.add(child)
            mapping.setdefault(parent, []).append(child)

        sql = """
            select ann.id, ann.description, ann.textValue, ann.details.owner.id,
            ann.details.owner.firstName, ann.details.owner.lastName
            from TagAnnotation ann
            """

        tags = []
        owners = dict()
        for element in query.projection(sql, params, ice_map):
            tag_id, description, text, owner, first, last = \
                [None if x is None else x.getValue() for x in element]
            tags.append([
                tag_id,
                description,
                text,
                owner,
                mapping.get(tag_id) or 0,
            ])
            owners[owner] = "%s %s" % (first, last)

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
