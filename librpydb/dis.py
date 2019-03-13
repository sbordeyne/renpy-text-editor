# py23 compatible
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import sys
import traceback
import types
import traceback

from opcode import *

# disassembler - sane one

class DisElement(object):
    """
    holds disassembler instruction information
    """

    def __init__(self):
        self.py_line = None
        self.bytecode_offset = None
        self.instruction = None
        self.arg = None
        self.readable_arg = None
        self.current = False

    # resulted object is (current, python_lineno, bytecode_offset, instruction, arg, constant)
    def to_tuple(self):
        """
        returns information as tuple
        """

        return (self.current, self.py_line, self.bytecode_offset, self.instruction, self.arg, self.readable_arg)


def dis(co, lasti=-1):
    """
    disassembles a code object into tuples
    """

    result = []

    code = co.co_code
    labels = findlabels(code)
    linestarts = dict(findlinestarts(co))
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    while i < n:
        c = code[i]
        op = ord(c)
        de = DisElement()
        result.append(de)

        if i in linestarts:
            de.python_lineno = linestarts[i]

        de.current = i == lasti
        de.bytecode_offset = i
        de.instruction = opname[op]
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256 + extended_arg
            extended_arg = 0
            i = i + 2
            if op == EXTENDED_ARG:
                extended_arg = oparg * 65536L
            de.arg = oparg

            if op in hasconst:
                de.readable_arg = co.co_consts[oparg]
            elif op in hasname:
                de.readable_arg = co.co_names[oparg]
            elif op in hasjrel:
                de.readable_arg = i + oparg
            elif op in haslocal:
                de.readable_arg = co.co_varnames[oparg]
            elif op in hascompare:
                de.readable_arg = cmp_op[oparg]
            elif op in hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                de.readable_arg = free[oparg]

    r = [d.to_tuple() for d in result]
    return r


def findlabels(code):
    """
    detect all offsets in a byte code which are jump targets

    return the list of offsets
    """

    labels = []
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = ord(c)
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256
            i = i + 2
            label = -1
            if op in hasjrel:
                label = i + oparg
            elif op in hasjabs:
                label = oparg
            if label >= 0:
                if label not in labels:
                    labels.append(label)
    return labels


def findlinestarts(code):
    """
    find the offsets in a byte code which are start of lines in the source

    generate pairs (offset, lineno) as described in Python/compile.c
    """

    byte_increments = [ord(c) for c in code.co_lnotab[0::2]]
    line_increments = [ord(c) for c in code.co_lnotab[1::2]]

    lastlineno = None
    lineno = code.co_firstlineno
    addr = 0
    for byte_incr, line_incr in zip(byte_increments, line_increments):
        if byte_incr:
            if lineno != lastlineno:
                yield (addr, lineno)
                lastlineno = lineno
            addr += byte_incr
        lineno += line_incr
    if lineno != lastlineno:
        yield (addr, lineno)
