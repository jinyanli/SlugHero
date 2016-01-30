# -*- coding: utf-8 -*-
db.define_table('department',
    Field('name', 'string', unique=True, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('short_name', 'string', unique=True, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    format = '%(name)s')

db.define_table('course',
    Field('department_id', 'reference department', readable=False, writable=False),
    Field('course_num', 'string', requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('name', 'string', unique=True, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('description', 'text'))

db.define_table('professor',
    Field('first_name', 'string', default=None, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('last_name', 'string', default=None, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('image', 'upload'),
    Field('department_id', 'reference department'),
    Field('saltiness', 'double'))
db.professor.department_id.requires = IS_IN_DB(db, db.department.id, '%(name)s')

quarter=['fall', 'winter', 'spring', 'summer']
db.define_table('ucscClass', # 'class' is a python reserved word
    Field('course_id', 'reference course', readable=False, writable=False),
    Field('syllabus', 'text'),
    Field('quarter', 'string', requires=IS_IN_SET(quarter)),
    Field('yr', ' integer', requires = IS_FLOAT_IN_RANGE(2000, 2100)),#year is a key word in SQL
    Field('term', 'string'),
    Field('difficulty', 'double'),
    Field('textbook_ids', 'list:reference textbook'),
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('datetime', 'datetime'))

db.define_table('classReview',
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('ucscClass_id', 'reference  ucscClass', readable=False, writable=False),
    Field('body', 'text', update=True),
    Field('term'),
    Field('rating', 'double'),
    Field('datetime', 'datetime'))

db.define_table('post',
    Field('ucscClass_id', 'reference ucscClass', readable=False, writable=False),
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('title', 'string', notnull=True),
    Field('body', 'text', notnull=True),
    Field('price', 'integer'), # price is in cents (eg 4000 -> $40)
    Field('image', 'upload'),
    Field('datetime', 'datetime'))

#comment is a resevered key word. Can't be used
db.define_table('comm',
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('post_id', 'reference post', readable=False , writable=False),
    Field('body', 'text'),
    Field('datetime', 'datetime'))


db.define_table('studentGrade',
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('grade', 'list:string'),
    Field('ucscClass_id', 'reference ucscClass', readable=False, writable=False))

gradeRange=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', 'P', 'NP']
db.studentGrade.grade.requires = IS_IN_SET(gradeRange)


db.define_table('professorReview',
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('course_id', 'reference course', readable=False, writable=False),
    Field('term'),
    Field('review', 'text', update=True),
    Field('rating', 'double'),
    Field('datetime', 'datetime'))
db.professorReview.rating.requires = IS_FLOAT_IN_RANGE(0, 5)

db.define_table('note',
    Field('title', 'string'),
    Field('notefile', 'upload'),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('course_id', 'reference course', readable=False, writable=False),
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('notetype', 'string'),
    Field('datetime', 'datetime'))

noteType = ['exam', 'homework', 'class note', 'course material', 'solution', 'other']
db.note.notetype.requires = IS_IN_SET(noteType)

db.define_table('textbook',
    Field('title', 'string', ondelete='CASCADE'),
    Field('author', 'list:string'),
    Field('publication_year', 'integer'),
    Field('isbn', 'integer', unique=True))
