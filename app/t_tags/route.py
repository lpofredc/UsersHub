from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_tags import forms as t_tagsforms
from app.models import TTags,BibTagTypes, TApplications, CorRoleTag, TRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db

route =  Blueprint('tags',__name__)

@route.route('tags/list', methods=['GET','POST'])
def tags():
    fLine =['ID','ID_type', 'CODE', 'Nom', 'Label', 'Description']
    columns = ['id_tag','id_tag_type','tag_code','tag_name','tag_label','tag_desc']
    contents = TTags.get_all(columns)
    return render_template('table_database.html' ,fLine = fLine ,line = columns,  table = contents,  key = 'id_tag', pathU = '/tag/update/', pathD = '/tags/delete/', pathA = '/tag/add/new',pathP = "/tag/users/",name = "un tag", name_list = "Liste des Tags", Members= "Utilisateurs", otherCol = 'True')


@route.route('tags/delete/<id_tag>',methods=['GET','POST'])
def delete(id_tag):
    TTags.delete(id_tag)
    return redirect(url_for('tags.tags'))


@route.route('tag/add/new',defaults={'id_tag': None}, methods=['GET','POST'])
@route.route('tag/update/<id_tag>',methods=['GET','POST'])
def addorupdate(id_tag):
    form = t_tagsforms.Tag()
    form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if id_tag == None:
        if request.method =='POST':
            if form.validate() and form.validate_on_submit():
                form_tag = pops(form.data)
                form_tag.pop('id_tag')
                TTags.post(form_tag)
                return redirect(url_for('tags.tags'))
            else:
                flash(form.errors)
        return render_template('tag.html', form = form)
    else:
        tag = TTags.get_one(id_tag)
        if request.method == 'GET':
            form = process(form,tag)
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit():
                form_tag = pops(form.data)
                form_tag['id_tag'] = tag['id_tag']
                TTags.update(form_tag)
                return redirect(url_for('tags.tags'))
            else:
                flash(form.errors)
        return render_template('tag.html',form = form)

@route.route('tag/users/<id_tag>', methods=['GET','POST'])
def tag_users(id_tag):
    fLine = [ 'ID', 'nom']
    user_list =  TRoles.concat()
    user_list = TRoles.test_group(user_list)
    user_tag = TRoles.get_user_in_tag(id_tag)
    tab2= TRoles.test_group(TRoles.concat(user_tag))    
    return render_template("tobelong.html",fLine = fLine, table = user_list, group = 'groupe', table2 =tab2  )

    # # affichage des utlisateurs
    # fLine = [ 'id role', 'nom role']
    # columns = [ 'id_role', 'prenom_role', 'nom_role']
    # filters = [{'col': 'groupe', 'filter': 'False'}]
    
    # contents = TRoles.get_all(columns,filters, False)
    # filters2 = [{'col': 'groupe', 'filter': 'True'}]
    # contents2 = TRoles.get_all(columns,filters2)
    # col = [ 'id_role', 'nom_role']
    # tab =[]
    # tab2 = []
    # tab3 = []
    # for d in contents:
    #     t = dict()
    #     t['id_role'] = d['id_role']
    #     t['nom_role'] = d['prenom_role']+ ' '+d['nom_role']
    #     tab.append(t)
    # for d in contents2:
    #     t = dict()
    #     t['id_role'] = d['id_role']
    #     if d['prenom_role'] == None:
    #         t['nom_role'] =d['nom_role']
    #     else :
    #         t['nom_role'] = d['prenom_role']+ ' '+d['nom_role']        
    #     tab2.append(t)
    
    # affichage des utilisateurs du tag
    

    


def pops(form):
    form.pop('csrf_token')
    form.pop('submit')
    return form

def process(form,tag):
    form.id_tag_type.process_data(tag['id_tag_type'])
    form.tag_name.process_data(tag['tag_name'])
    form.tag_label.process_data(tag['tag_label'])
    form.tag_code.process_data(tag['tag_code'])
    form.tag_desc.process_data(tag['tag_desc'])
    return form



# NON UTILISE
# @route.route('/tag', methods=['GET','POST'])
# def tag():
#     form = t_tagsforms.Tag()
#     form.id_tag_type.choices =BibTagTypes.choixSelect('id_tag_type','tag_type_name')
#     if request.method =='POST':
#         if form.validate() and form.validate_on_submit():
#             form_tag = form.data
#             form_tag.pop('csrf_token')
#             form_tag.pop('submit')
#             form_tag.pop('id_tag')
#             TTags.post(form_tag)
#             return redirect(url_for('tags.tags'))
#         else:
#             flash(form.errors)
#     return render_template('tag.html', form = form)


# @route.route('tags/update/<id_tag>',methods=['GET','POST'])
# def update(id_tag):
#     entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
#     colonne = ['id_tag','id_tag_type','tag_code','tag_name','tag_label','tag_desc']
#     contenu = TTags.get_all(colonne)
#     # test
#     tag = TTags.get_one(id_tag)
#     form = t_tagsforms.Tag()
#     form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
#     if request.method == 'GET':
#         form.id_tag_type.process_data(tag['id_tag_type'])
#     if request.method == 'POST':
#         if form.validate() and form.validate_on_submit():
#             form_tag = form.data
#             form_tag.pop('csrf_token')
#             form_tag.pop('submit')
#             form_tag['id_tag'] = tag['id_tag']
#             TTags.update(form_tag)
#             return redirect(url_for('tags.tags'))
#         else:
#             flash(form.errors)
#     return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/tags/update/', cheminS = '/tags/delete/', test ='tag.html', form = form, code = tag['tag_code'], name = tag['tag_name'], label = tag['tag_label'], desc = tag['tag_desc'])