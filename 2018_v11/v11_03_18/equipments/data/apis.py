# -*- coding: utf-8 -*-

import xmlrpclib
import pprint
pp = pprint.PrettyPrinter(indent=4)
url = "http://127.0.0.1:8069"
db = "test"
user = "admin"
pwd = "admin"

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
print common.version()

uid = common.authenticate(db, user, pwd, {})
print uid


models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))


eids =  models.execute_kw(db, uid, pwd, 'equipment.equipment', 'search',[[]])

x = models.execute_kw(db, uid, pwd, 'equipment.equipment', 'read', [eids, ["name"]])
pp.pprint(x)

x = models.execute_kw(db, uid, pwd, 'equipment.equipment', 'action_out', [eids])
