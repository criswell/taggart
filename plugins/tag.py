#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Tag plugin for command-line tag manipulation

   :author: Sam Hart <sam@glencoesoftware.com>

   Copyright (C) 2013 Glencoe Software, Inc. All rights reserved.
   Use is subject to license terms supplied in LICENSE.txt

"""

import platform
import subprocess
import sys

import omero
from omero.cli import BaseControl, CLI, ExceptionHandler

HELP="""Manage OMERO user tags.

Foo

Examples:

    bar
    snaz

"""

def exec_command(cmd):
    """
    given a command, will execute it in the parent environment
    Returns a list containing the output
    """
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.stdout.readlines()
    p.stdout.close()
    return output

def clip(s, width):
    """
    Given a string, s, and a width, will clip the string to that width or
    fill it with spaces up to that width.

    Returns modified string
    """
    mod_s = s
    if len(s) > width:
        mod_s = s[:width]
    elif len(s) < width:
        mod_s = s + " " * (width - len(s))
    return mod_s

class TagControl(BaseControl):

    def _configure(self, parser):

        self.exc = ExceptionHandler()

        parser.add_login_arguments()
        sub = parser.sub()

        list_g = parser.add(sub, self.list, help="List tags")

        self.add_standard_params(list_g)

        list_g.add_login_arguments()

    def add_standard_params(self, parser):
        parser.add_argument("--admin", action="store_true", default=False, \
            help="Perform action as an administrator")
        parser.add_argument("--nopage", action="store_true", default=False, \
            help="Disable pagination")

    def pagetext(self, format, elements, num_lines=None):
        for index, line in enumerate(elements):
            if num_lines is None:
                #self.ctx.out(format % line)
                self.ctx.out(format.format(*line))
            elif index % num_lines == 0 and index:
                input=raw_input("[Enter] or [q]uit: ")
                if input.lower() == 'q':
                    break
            else:
                self.ctx.out(format.format(*line))

    def determine_console_size(self):
        """
        Will attempt to determine console size based upon the current platform.

        Returns tuple of width and length.
        """
        # The defaults if we can't figure it out
        lines = 25
        width = 80

        this_system = platform.system().lower()

        try:
            if this_system in ['linux', 'darwin', 'macosx', 'cygwin']:
                output = exec_command(['tput', 'lines'])
                if len(output) > 0:
                    lines = int(output[0].rstrip())
                output = exec_command(['tput', 'cols'])
                if len(output) > 0:
                    width = int(output[0].rstrip()) 
            elif this_system in ['windows', 'win32']:
                # http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
                from ctypes import windll, create_string_buffer
                # stdin handle is -10
                # stdout handle is -11
                # stderr handle is -12
                h = windll.kernel32.GetStdHandle(-12)
                csbi = create_string_buffer(22)
                res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
                if res:
                    (bufx, bufy, curx, cury, wattr,
                     left, top, right, bottom,
                     maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                    lines = bottom - top + 1
                    width = bottom - top + 1
        except:
            raise
            # Possible evil to ignore what the error was, but, truthfully,
            # the reason we do so is because it means it's a platform we
            # don't have support for, or a platform we should have support
            # for but which has some non-standard witch-craftery going on
            self.ctx.out("Could not determine the console length.")

        return width, lines

    def list(self, args):
        """
        """
        # The max width of the ID field. We need something here unless
        # we want to pre-search to determine the max size. Our assumption
        # here is that we wont have more than 10,000,000 tags.
        max_id_width = 8

        params = omero.sys.ParametersI()
        params.addString('ns', omero.constants.metadata.NSINSIGHTTAGSET)
        ice_map = dict()
        #import pdb; pdb.set_trace()
        if args.admin:
            ice_map["omero.group"]="-1"

        if args.nopage:
            console_length = None
            width = 80
        else:
            width, console_length = self.determine_console_size()

        client = self.ctx.conn(args)
        session = client.getSession()
        query = session.getQueryService()

        sql = """
            select ann.id, ann.textValue, ann.description
            from TagAnnotation ann
            """

        tags = []

        max_field_width = int(((width - max_id_width) / 2.0) - 2)

        for element in query.projection(sql, params, ice_map):
            tag_id, text, description, = \
                [str(None) if x is None else str(x.getValue()) for x in element]

            if args.nopage:
                tags.append((
                    tag_id,
                    text,
                    description,
                ))
            else:
                tags.append((
                    clip(tag_id, max_id_width),
                    clip(text, max_field_width),
                    clip(description, max_field_width),
                ))

        self.pagetext("{0}|{1}|{2}", tags, console_length)

try:
    register("tag", TagControl, HELP)
except NameError:
    if __name__ == "__main__":
        cli = CLI()
        cli.register("user", TagControl, HELP)
        cli.invoke(sys.argv[1:])
