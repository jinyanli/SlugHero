# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    dept = db().select(db.department.ALL, orderby=db.department.name)
    form = SQLFORM(db.department)
    if form.process().accepted:
        response.flash = 'Department added'
    return dict(dept=dept, form=form)

def show():
    dept = db.department(request.args(0,cast=int)) or redirect(URL('index'))
    #db.course.department_id.default = dept.id
    info = db(db.course.department_id==dept.id).select()
    return dict(dept=dept, info=info)

def addCourse():
    dept = db.department(request.args(0,cast=int)) or redirect(URL('index'))
    db.course.department_id.default = dept.id
    form = SQLFORM(db.course)
    form.add_button('Back', URL('show', args=dept.id))
    if form.process().accepted:
        response.flash = 'Course added'
        redirect(URL('show', args=dept.id))
    info = db(db.course.course_id==dept.id).select()
    return dict(dept=dept, info=info, form=form)

def showClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.UCSCclass.course_id==ucscClass.id).select(orderby=db.UCSCclass.year | db.UCSCclass.quarter)
    return dict(ucscClass=ucscClass, info=info)

def check_term(form):
    q = form.vars.quarter
    y = form.vars.year
    query = db((db.UCSCclass.quarter == q) & (db.UCSCclass.year == y)).select()
    if query:
        form.errors.query = 'Term already exists'
        response.flash = 'Term already exists'

def addProf():
    uclass = db.UCSCclass(request.args(0, cast=int)) or redirect(URL('index'))
    form = FORM('Professor\'s name',
               INPUT(_name='name'),
               INPUT(_type='Submit'))
    if form.process().accepted:
        q = db(db.professor.name==form.vars.name).select(db.professor.ALL)
        print q
        if q:
            row = q[0]
            db(db.UCSCclass.id==uclass.id).update(professor_id=row.id)
        else:
            response.flash = form.vars.name
            db.professor.insert(name=form.vars.name)
            q = db(db.professor.name==form.vars.name).select()
            response.flash = q
            db(db.UCSCclass.id==uclass.id).update(professor_id=q[0].id)
        response.flash = 'Professor added'
        redirect(URL('term', args=uclass.id))
    return dict(form=form)

def addClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    db.UCSCclass.course_id.default = ucscClass.id
    fields = ['description', 'quarter', 'year', 'difficulty']
    #labels = {'name':'Professor Name'}
    form = SQLFORM(db.UCSCclass, fields=fields)
    form.add_button('Back', URL('showClass', args=ucscClass.id))
    if form.process().accepted:
        response.flash = 'Class added'
        redirect(URL('showClass', args=ucscClass.id))
    info = db(db.UCSCclass.course_id==ucscClass.id).select()
    return dict(ucscClass=ucscClass, info=info, form=form)

def term():
    uclass = db.UCSCclass(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.UCSCclass.course_id==uclass.id).select()
    classReview = db(db.classReview.class_id==uclass.id).select()
    return dict(uclass=uclass, info=info, classReview=classReview)



def showProf():
    prof = db.professor(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.professorReview.professor_id==prof.id).select()
    return dict(prof=prof, info=info)

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
