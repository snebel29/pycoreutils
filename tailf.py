#! /usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/karelzak/util-linux/blob/master/text-utils/tailf.c
# http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
# http://stackoverflow.com/questions/32901504/reading-lines-backwards-relative-to-a-line-in-python
# https://github.com/kasun/python-tail/blob/master/tail.py
# http://www.manugarg.com/2007/04/real-tailing-in-python.html

# Read last n lines
# Watch for changes on the file and print them (inotify vs rollfile)
# Apply callback function to every line as improvement
# What happens with callback function if lines are huge?
# Handle unlink, rename and truncate
# Handle signals
# Handle unicode codifications
# Watch for multiple files
# Tests
# Python 2 and 3 compatible
# Publish to pypi
# docstring Documentation?

import os
import io
import sys

from time import sleep

BLOCK_SIZE = io.DEFAULT_BUFFER_SIZE

def tailf1(file, lines=10):
    with open(file, 'r') as fd:
        print([l for l in fd.read().splitlines() if l != ''][-1*lines:])
        while True:
            line = fd.readline()
            if not line:
                sleep(1)
            else:
                sys.stdout.write(line)

def tailf2(file, lines=10):
    with open(file) as fd:
        fd.seek(0, os.SEEK_END)
        file_size = fd.tell()
        print(file_size)
        buffer = ''

        if file_size < BLOCK_SIZE:
            fd.seek(0, os.SEEK_SET)
            buffer = fd.read()

        else:
            counter = 1
            while buffer.count(os.linesep) < lines +1:
                pointer = (-1 * counter) * BLOCK_SIZE
                print('pointer: {0}'.format(pointer))

                if abs(pointer) > file_size:
                    fd.seek(0, os.SEEK_SET)
                    buffer = fd.read(file_size - (BLOCK_SIZE * (counter - 1))) + buffer
                    break

                else:
                    fd.seek(pointer, os.SEEK_END)
                    buffer = fd.read(BLOCK_SIZE) + buffer

                counter += 1

        if buffer[-1:] == os.linesep:
            buffer = buffer.rstrip()

        tail_lines = buffer.split(os.linesep)[-1*lines:]
        for line in tail_lines: print(line)



tailf = tailf2
tailf('test3.txt')

"""
import os
from abc import abstractmethod

class Command(object):
    def __init__(self, ops):
        self.ops = ops

    @abstractmethod
    def run(self):
        pass

class Tail(Command):

    nlines = 4
    block_size = 2

    def __init__(self, ops):
        super(Tail, self).__init__(ops)
        self.pointer = None
        self.read_buffer = ""
        self.lines_backward = []

    def _move_pointer_backwards(self):
        self.pointer = self.pointer - self.block_size
        if not self.pointer > 0: self.pointer = 0
        self.fd.seek(self.pointer)

    def read_chunk(self):
        self._move_pointer_backwards()
        self.read_buffer += self.fd.read(self.block_size)
        self._move_pointer_backwards() ## Because read move it forward by exactly block_size

    def run(self):
        with open('test.txt', 'r') as self.fd:
            self.fd.seek(0, os.SEEK_END)
            self.file_size = self.fd.tell()
            self.pointer = self.fd.tell()

            while self.fd.tell() > 0:
                self.read_chunk()
                chunk_lines = self.read_buffer.split("\n")
                if chunk_lines > 2:
                    self.lines_backward += chunk_lines[1:]
                    self.pointer = self.pointer + len(chunk_lines[0])
                    self.read_buffer = ""

        print(self.lines_backward)

Tail({}).run()
"""


