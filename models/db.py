# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# -*- coding: utf-8 -*-
db = DAL("sqlite://storage.sqlite")

db.define_table('department',
   Field('name', 'string', unique=True),
   Field('short_name','string', unique=True)
   )

db.define_table('course',
   Field('course_id', writable=False, readable=False),
   Field('department_id', 'reference department', writable=False, readable=False),
   Field('course_num','integer',unique=True),
   Field('name', 'string', unique=True),
   Field('description', 'text'))

db.define_table('professor',
   Field('professor_id', writable=False, readable=False),
   Field('name','string',unique=True, default=None),
   #Field('image', 'upload', update=True, authorize=True),
   Field('saltiness', 'double'))

db.define_table('UCSCclass', # 'class' is a python reserved word
   Field('UCSCclass_id', writable=False, readable=False),
   Field('course_id', 'reference course', writable=False, readable=False),
   Field('description', 'text'),
   Field('quarter', requires=IS_IN_SET(['Fall', 'Winter', 'Spring', 'Summer'])),
   Field('year', requires=IS_INT_IN_RANGE(2000, 2051)),
   Field('difficulty','double'),
   Field('textbook_id', 'list:reference textbook', writable=False, readable=False),
   Field('professor_id', 'reference professor', writable=False, readable=False))

db.define_table('student',
   Field('student_id', writable=False, readable=False),
   Field('first_name', 'string'),
   Field('last_name', 'string'))

db.define_table('classReview',
   Field('class_id', writable=False, readable=False),
   Field('student_id', 'reference student', writable=False, readable=False),
   Field('content','text',update=True),
   Field('term'),
   Field('rating', 'double'))

db.define_table('post',
   Field('post_id', writable=False, readable=False),
   Field('UCSCclass_id', 'reference UCSCclass', writable=False, readable=False),
   Field('student_id', 'reference student', writable=False, readable=False),
   Field('title','string'),
   Field('body','text'),
   Field('datetime', 'datetime'))

db.define_table('salePost',
   Field('salePost_id', writable=False, readable=False),
   Field('student_id', 'reference student', writable=False, readable=False),
   Field('title','string'),
   Field('body','text'),
   Field('price', 'double'),
   Field('image', 'upload'),
   Field('datetime', 'datetime'))

db.define_table('comment',
   Field('comment_id', writable=False, readable=False),
   Field('student_id', 'reference student', writable=False, readable=False),
   Field('post_id', 'reference post', writable=False, readable=False),
   Field('body','text'),
   Field('datetime', 'datetime'))


db.define_table('user',
   Field('user_id', writable=False, readable=False),
   Field('student_id', 'reference student', writable=False, readable=False),
   Field('image', 'upload', update=True),
   Field('email'),
   Field('password', 'string', length=10),
   Field('year'),
   Field('is_admin','boolean'))
db.user.email.requires = IS_EMAIL()

db.define_table('studentGrade',
   Field('studentGrade_id', writable=False, readable=False),
   Field('student_id', 'reference student', writable=False, readable=False),
   Field('grade', 'double'),
   Field('UCSCclass_id', 'reference UCSCclass', writable=False, readable=False))

db.define_table('professorReview',
   Field('professorReview_id', writable=False, readable=False),
   Field('professor_id', 'reference professor', writable=False, readable=False),
   Field('user_id', 'reference user', writable=False, readable=False),
   Field('course_id','reference course', writable=False, readable=False),
   Field('term'),
   Field('review','text',update=True),
   Field('rating', 'double'),
   Field('datetime','datetime'))

db.define_table('note',
   Field('note_id', writable=False, readable=False),
   Field('title','string'),
   Field('file','upload'),
   Field('user_id', 'reference user', writable=False, readable=False),
   Field('course_id','reference course', writable=False, readable=False),
   Field('professor_id', 'reference professor', writable=False, readable=False),
   Field('notetype', 'string'),
   Field('datetime','datetime'))

db.define_table('textbook',
   Field('textbook_id', writable=False, readable=False),
   Field('title','string',ondelete='CASCADE'),
   Field('author','list:string'),
   Field('publication_year','integer'),
   Field('isbn', 'integer',unique=True))


## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)
