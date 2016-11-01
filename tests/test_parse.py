#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rpnparse.rpnparse import parse

__author__ = "Julian Gethmann"
__copyright__ = "Julian Gethmann"
__license__ = "new-bsd"


def test_parse():
    assert parse('1 2 + 3 * sin') == 0.4121184852417566
    assert parse('1 2 + 3 * cos') == -0.9111302618846769
    assert round(parse('10,3,1,2,/,*,-,tan', delimiter=","), 5) == -1.32636
    assert round(parse('0.2 10.24 pi * 180 / * 10.24 pi * 180 / sin /'), 9) == 0.201068696
    with pytest.raises(ValueError):
        parse('2 2 2')
