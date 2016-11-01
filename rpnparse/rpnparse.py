#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides one function :func:`parse` that parses and calculates
reverse polish notation (RPN) strings or lists with RPN items in it.

Other functions are just for the command line interface and the interactive
RPN shell.
"""
from __future__ import division
from collections import deque
from operator import add, sub, mul, abs, mod
from operator import truediv as div
from operator import floordiv as idiv
from math import sqrt, pi, exp, sin, cos, tan, asin, acos, atan

__author__ = "Julian Gethmann"
__copyright__ = "Julian Gethmann"
__license__ = "new-bsd"


def parse(code, delimiter=' '):
    """Return the result of the RPN calculation of the `code` string or list.

    Supported operatorations are
        * +, -, *, mult, /, div, //, idiv, pow, %, mod
        * sin, cos, tan, asin, acos, atan, sqrt, sqr, abs, exp

    Args:
        code (str|list):
            string of the RPN calculation to be carried out or a list with each
            number or operator as one element of the list.
        delimiter (str): optional
            delimiter of the RPN expression. e. g. "," if your `code` looks like
            "2,2,+" and not like "2 2 +".

    Returns:
        float or int: Result of the RPN calculation

    Raises:
        ValueError: if the code is neither a list of numbers and strings of
            operator names or a string with these.
            And if the code does not compute and there are items left on the stack.

    .. note::
        Though this might be used with Python 2 the division is a Python 3 div.

    Examples:
        >>> parse(code="2 2 +")
        4
        >>> parse(code="3 3 2 * + sqrt")
        3.0
        >>> parse("2,2,+", delimiter=",")
        4
    """
    def sqr(a):
        return a * a

    operators1 = {
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "asin": asin,
        "acos": acos,
        "atan": atan,
        "sqrt": sqrt,
        "sqr": sqr,
        "abs": abs,
        "exp": exp,
    }
    operators2 = {
        "+": add,
        "-": sub,
        "*": mul,
        "mult": mul,
        "/": div,
        "//": idiv,
        "idiv": idiv,
        "pow": pow,
        "mod": mod,
        "%": mod,
    }

    if isinstance(code, list):
        code_list = deque(code)
    elif isinstance(code, str):
        code_list = deque(filter(None, code.lower().replace(
            'pi', str(pi)).split(delimiter)))
    else:
        raise ValueError("Code must be either a list of numbers and operators "
                         "or a string thereof.")
    stack = list()
    for tok in code_list:
        if tok in operators1:
            stack.append(operators1[tok](stack.pop()))
        elif tok in operators2:
            b = stack.pop()
            a = stack.pop()
            stack.append(operators2[tok](a, b))
        else:
            try:
                stack.append(int(tok))
            except ValueError:
                stack.append(float(tok))
    if len(stack) > 1:
        raise ValueError("The code must be a valid RPN code. "
                         "The calculation stopped with these elements: "
                         "{}".format(" ".join([str(s) for s in stack])))
    return stack[0]


def console():
    """Main entry point for console_scripts.

    Cares about the arument parsing, interactive shell.
    """
    import argparse
    import sys
    if sys.version_info.major == 2:
        PY2 = True
    parser = argparse.ArgumentParser(
        prog='Command line reverse polish notation calculator')
    parser.add_argument("--delimiter", "-d", dest='d', nargs='?', default=" ",
                        help='Delimiter for the RPN string (default is space)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("code", nargs='*', default=[],
                       help="put the calculation in quotation marks as an argument")
    group.add_argument("--interactive", "-i", action='store_true', dest='i',
                       help='If one wants an interactive RPN shell')
    args = parser.parse_args()
    delimiter = args.d
    if args.i:
        while True:
            try:
                if PY2:
                    print(parse(raw_input('>>> '), delimiter))  # noqa
                else:
                    print(parse(input('>>> '), delimiter))  # noqa
            except:
                print('Bye')
                sys.exit(0)
    else:
        print(parse(" ".join(args.code), delimiter))


if __name__ == "__main__":
    console()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
