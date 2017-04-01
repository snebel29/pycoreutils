#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# https://github.com/karelzak/util-linux/blob/master/text-utils/tailf.c
# http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
# http://stackoverflow.com/questions/32901504/reading-lines-backwards-relative-to-a-line-in-python
# https://github.com/kasun/python-tail/blob/master/tail.py
# http://www.manugarg.com/2007/04/real-tailing-in-python.html


# TODO: Watch file using inotify
# TODO: Apply callback function to every line as improvement
# TODO: What happens with callback function if lines are huge?
# TODO: Handle unlink, rename and truncate
# TODO: Handle signals
# TODO: Watch for multiple files
# TODO: Add Tests, create mocks when necessary
# TODO: Python 2 and 3 compatible
# TODO: Publish to pypi providing bin and modules using generator
# TODO: docstring Documentation?
# TODO: Settup CI pipeline with travis

import os
import io
import sys

from time import sleep

BLOCK_SIZE = io.DEFAULT_BUFFER_SIZE

def poll_file(fd):
    fd.seek(0, os.SEEK_END)
    while True:
        new_line = fd.readline()
        if not new_line:
            sleep(0.1)
        else:
            sys.stdout.write(new_line)


def tailf(file, lines=10, callback=print):
    with open(file) as fd:
        fd.seek(0, os.SEEK_END)
        file_size = fd.tell()
        buff = ''

        if file_size < BLOCK_SIZE:
            fd.seek(0, os.SEEK_SET)
            buff = fd.read()

        else:
            counter = 1
            while buff.count(os.linesep) < lines +1:
                pointer = (-1 * counter) * BLOCK_SIZE

                if abs(pointer) > file_size:
                    fd.seek(0, os.SEEK_SET)
                    buff = fd.read(file_size - (BLOCK_SIZE * (counter - 1))) + buff
                    break

                else:
                    fd.seek(pointer, os.SEEK_END)
                    buff = fd.read(BLOCK_SIZE) + buff

                counter += 1

        if buff[-1:] == os.linesep:
            buff = buff.rstrip()

        tail_lines = buff.split(os.linesep)[-1*lines:]
        for line in tail_lines:
            callback(line)

        poll_file(fd)


tailf('test.txt')


