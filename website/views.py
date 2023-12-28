from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify 
from flask_login import login_required, current_user
from .models import Note, User
from . import db


from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) <= 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
        
        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

'''
@views.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == 'GET': 
        all_notes = Note.query.all()#Gets all the notes from the db 
        return render_template('feed.html', all_notes=all_notes, user=current_user)
'''

@views.route('/user', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html', user=current_user)
