# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
@auth.requires_membership('manager')
def manage():
    grid = SQLFORM.smartgrid(db.image)
    return dict(grid=grid)
likes=0
@auth.requires_login()
def delete():
    a=db.image(request.args(0)) or redirect(URL('index'))
    form=crud.delete(db.image,a.id)
    return dict(form=form)
@auth.requires_login()        
def upload(): 
    db.image.author.default = auth.user.first_name + ' '+ auth.user.last_name
    form=crud.create(db.image,message='Upload Successful!')
    return dict(form=form)
def fade():
    return dict()
@auth.requires_login()
def show():
    image = db.image(request.args(0)) or redirect(URL('index'))
    db.comment.image_id.default = image.id
    form = crud.create(db.comment,
                message='your comment is posted',next=URL(args=image.id))
    db.like.image_id.default = image.id
    form1 = SQLFORM (db.like,submit_button= T('LIKE ME :)'))
   
    if form1.process().accepted:
       response.flash='Thanks for liking me'
    likey = db(db.like.image_id==image.id).select()
    comments = db(db.comment.image_id==image.id).select()
    return dict(image=image, comments=comments,form=form,form1=form1,likey=likey)

def download():
    return response.download(request, db)

def index():
        images = db().select(db.image.ALL, orderby=db.image.title)
        if not session.counter:
            session.counter = 1
        else:
            session.counter += 1
       
        return dict(images=images,message="Hello from Cyclone", counter=session.counter)

def first():
    form = SQLFORM.factory(Field('visitor_name',requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        session.visitor_name = form.vars.visitor_name
        redirect(URL('second'))
    return dict(form=form)
def second():
    if not request.function=='first' and not session.visitor_name:
        redirect(URL('first'))
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
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


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
