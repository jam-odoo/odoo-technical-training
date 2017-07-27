import xmlrpclib

url = "http://127.0.0.1:8069"
dbname = "test9"
user = "admin"
pwd = "admin"


common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(dbname, user, pwd, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))


session_ids = models.execute_kw(dbname, uid, pwd, "openacademy.session", "search", [[]])

print session_ids

sessions = models.execute_kw(dbname, uid, pwd, "openacademy.session", "read", [session_ids],  {'fields': ['name', 'course_id']})

print sessions

sessions = models.execute_kw(dbname, uid, pwd, "openacademy.session", "reset_session", [session_ids])
