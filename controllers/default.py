# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon.tools import Crud
crud = Crud(db)

def index():
    response.flash = T("Slug Hero")
    message='Welcome Slug Hero'
    return dict(message=T('Welcome to Slug Hero'))

def showDepartment():
    depts = db().select(db.department.ALL, orderby=db.department.name)
    return locals()

@auth.requires_login()
def departmentCreate():
    form = crud.create(db.department,next='showDepartment')
    return locals()

@auth.requires_login()
#@auth.requires_membership('admin')
def departmentEdit():
    department = db.department(request.args(0)) or redirect(URL('showDepartment'))
    form = crud.update(db.department,department,next='showDepartment')
    return locals()

def showCourse():
    dept = db.department(request.args(0)) or redirect(URL('showDepartment'))
    courses = db(db.course.department_id==dept.id).select(orderby=db.course.name,limitby=(0,25))
    return locals()

@auth.requires_login()
def courseCreate():
    db.course.department_id.default = request.args(0)
    redirect='showCourse/'+request.args(0)
    form = crud.create(db.course,next=redirect)
    return locals()

@auth.requires_login()
def courseEdit():
    course = db.course(request.args(0)) or redirect(URL('showCourse'))
    form = crud.update(db.course,course,next='showCourse')
    return locals()

def showProfessor():
    profs = db().select(db.professor.ALL, orderby=db.professor.first_name)
    return locals()

@auth.requires_login()
def professorCreate():
    #dept = db.department(request.args(0,cast=int)) or redirect(URL('index'))
    #db.course.department_id.default = dept.id
    form = SQLFORM(db.professor)
    if form.process().accepted:
        response.flash = 'Professor added'
        redirect(URL('showProfessor'))
    #info = db(db.course.course_id==dept.id).select()
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
