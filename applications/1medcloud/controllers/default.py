# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import gluon.utils as TT

def index():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

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

def mobile_patient_register():
    email = request.vars.email
    password = request.vars.password
    firstname = request.vars.firstname
    middlename = request.vars.middlename
    lastname = request.vars.lastname
    country = request.vars.country
    rows = db(db.patient.email==email).select()
    result = {}
    
    if len(rows) != 0:
        result['status'] = "exist"
        return response.json(result)
    
    return_result = TT.md5_hash(password)
    ret = db.patient.validate_and_insert(email=email, password=password, first_name=firstname, middle_name=middlename, last_name=lastname, md5=return_result, country=country)

    if ret.errors:
        result['status'] = "ERROR"
        return response.json(result)        
    else:
        result['status'] = "success"
        result['result'] = return_result   
        return response.json(result)

    
def mobile_prof_register():
    email = request.vars.email
    password = request.vars.password
    firstname = request.vars.firstname
    middlename = request.vars.middlename
    lastname = request.vars.lastname
    country = request.vars.country
    rows = db(db.prof.email==email).select()
    result = {}
    
    if len(rows) != 0:
        result['status'] = "exist"
        return response.json(result)
    
    return_result = TT.md5_hash(password)
    ret = db.prof.validate_and_insert(email=email, password=password, first_name=firstname, middle_name=middlename, last_name=lastname, md5=return_result, country=country)

    if ret.errors:
        result['status'] = "ERROR"
        return response.json(result)        
    else:
        result['status'] = "success"
        result['result'] = return_result   
        return response.json(result)
    
def mobile_patient_login():
    email=request.vars.email
    password=request.vars.password
    rows = db(db.patient.email==email).select()
    if len(rows) != 1:
        return response.json({'status': 'ERROR'})
    user = rows[0]
    return response.json({'status':'success', 'result': user.md5})

def mobile_prof_login():
    email=request.vars.email
    password=request.vars.password
    rows = db(db.prof.email==email).select()
    if len(rows) != 1:
        return response.json({'status': 'ERROR'})
    user = rows[0]
    return response.json({'status':'success', 'result': user.md5})

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
