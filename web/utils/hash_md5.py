#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

import hashlib

def gen_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    if origin:
        ha = hashlib.md5()
        ha.update(origin.encode('utf-8'))
        return ha.hexdigest()