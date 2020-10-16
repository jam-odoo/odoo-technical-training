from xmlrpc import client

url = 'https://odoo-online-online-technical-training-13-0-dev-acade-1364739.dev.odoo.com'
db = 'odoo-online-online-technical-training-13-0-dev-acade-1364739'
username = 'admin'
password = 'admin'

common = client.ServerProxy("{}/xmlrpc/2/common".format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})
print(uid)

models = client.ServerProxy("{}/xmlrpc/2/object".format(url))

model_access = models.execute_kw(db, uid, password,
                                'academy.session', 'check_access_rights',
                                ['write'], {'raise_exception': False})
print(model_access)

courses = models.execute_kw(db, uid, password,
                           'academy.course', 'search_read',
                           [[['level', 'in', ['intermediate', 'beginner']]]])
print(courses)

course = models.execute_kw(db, uid, password,
                          'academy.course', 'search',
                          [[['name', '=', 'Accounting 200']]])
print(course)

session_fields = models.execute_kw(db, uid, password,
                                  'academy.session', 'fields_get',
                                  [], {'attributes': ['string', 'type', 'required']})
print(session_fields)

# Was a small typo with 'execute' instead of 'execute_kw' in video
new_session = models.execute_kw(db, uid, password,
                            'academy.session', 'create',
                            [
                                {
                                    'course_id': course[0],
                                    'state': 'open', 
                                    'duration': 5,
                                }
                            ]
                            )

print(new_session)