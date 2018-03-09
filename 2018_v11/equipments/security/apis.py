# -*- coding: utf-8 -*-

import xmlrpclib

url = "http://127.0.0.1:8069"
db = "test"
user = "admin"
pwd = "admin"


common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()