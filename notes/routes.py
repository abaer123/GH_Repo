import os

from notes import db, note, auth, users
from notes.forms import AddForm, AdminForm, ResetForm, DeleteForm
from flask import render_template, request, flash, redirect, jsonify
from werkzeug.security import check_password_hash


@note.route('/', methods=['GET', 'POST'])
@note.route('/index', methods=['GET', 'POST'])
def index():
    items = []

    id = request.args.get('id')
    conn = db.create_connection()

    try:
        items = db.select_note_by_id(conn, id)
    except Exception as e:
        note.logger.error("Error Creating UI: %s" % e)

    arr = [
        {
          'name': 'Shoe', id: '1', 'time': '1:35'
        },
        {
          'name': 'Thorn', id: '2', 'time': '1:36'
        },
        {
          'name': 'BrightCow', id: '3', 'time': '1:39'
        },
        {
          'name': 'FireFlower', id: '4', 'time': '1:41'
        },
        {
          'name': 'RTZ', id: '5', 'time': '1:47'
        },
        {
          'name': 'Krit', id: '6', 'time': '1:50'
        },
        {
          'name': 'DuBu', id: '7', 'time': '2:11'
        },
        {
          'name': 'DinnerZoltar', id: '8', 'time': '2:12'
        },
        {
          'name': 'DM', id: '9', 'time': '2:22'
        },
        {
          'name': 'Zoo', id: '10', 'time': '2:30'
        },
        {
          'name': 'Nova', id: '11', 'time': '2:57'
        },
        {
          'name': 'Light', id: '12', 'time': '3:07'
        },
        {
          'name': 'Beam', id: '13', 'time': '3:08'
        },
        {
          'name': 'Solo', id: '14', 'time': '3:22'
        },
        {
          'name': 'Ghost', id: '15', 'time': '3:50'
        }
      ]


    add_form = AddForm()
    delete_form = DeleteForm()
    admin_form = AdminForm()

    if add_form.validate_on_submit():
        add_note(add_form.note_field.data)
        flash('Note "{}" has been added!'.format(
            add_form.note_field.data))

        return redirect('/')

    if delete_form.validate_on_submit():
        try:
            delete_note(delete_form.id_field.data)
            flash('Note "{}" has been Deleted!'.format(
            delete_form.id_field.data))
        except Exception as e:
            flash('Failed to delete Note "{}": %s'.format(
            delete_form.id_field.data, e))

        return redirect('/')

    if admin_form.validate_on_submit():
        return redirect('/admin')
    
    return render_template('index.html', notes=arr, add_form=add_form, delete_form=delete_form, admin_form=admin_form)


@note.route('/admin', methods=['GET', 'POST'])
@auth.login_required
def admin():
    reset_form = ResetForm()
    if reset_form.validate_on_submit():
        try:
            reset()
            flash('Database Table "{}" has been reset!'.format(
            "notes"))
            return redirect('/')
        except Exception as e:
            note.logger.error(e)
    
    return render_template('admin.html', reset_form=reset_form)


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@note.route('/add', methods=['POST'])
def add_note(msg=""):

    if not msg:
        data = request.get_json(force=True)
        msg = data.get('message')

    if not msg:
         return jsonify({"Error": "No message in Request"}), 400

    if len(msg) > 1024:
        return jsonify({"Error": "Message tooooo long!"}), 400

    if (msg == "\""):
        response = jsonify({"Success": "Maybe a Security Issue!"})
        response.headers.set('Content-Type', 'text/html')
        return response, 200

    conn = db.create_connection()
    try:
        db.create_note(conn, (str(msg),))
        return jsonify({"Sucess": "Note added!"})
    except Exception as e:
        err = "%s" % e
        return jsonify({"Error": err}), 500


@note.route('/delete', methods=['DELETE'])
def delete_note(id=None):
    if not id:
        id = request.args.get('id')

    if not id:
        return "No Id sent in request."

    conn = db.create_connection()
    try:
        db.delete_note(conn, id)
        return "Note deleted successfully!"
    except Exception as e:
        return "Failed to delete Note: %s" % e

def reset():
    conn = db.create_connection()
    sql_drop_notes_table = """ DROP TABLE notes;"""
    try:
        db.drop_table(conn, sql_drop_notes_table)
    except Exception as e:
        note.logger.error("Failed to reset database table 'notes': %s" % e)

    # TODO: Refactor this as well as
    # always check for db and table and
    # recreate if missing
    conn = db.create_connection()
    sql_create_notes_table = """ CREATE TABLE IF NOT EXISTS notes (
                                        id integer NOT NULL AUTO_INCREMENT,
                                        data text,
                                        PRIMARY KEY (id)
                                    ); """
    try:
        db.create_table(conn, sql_create_notes_table)
    except Exception as e:
        note.logger.error("Failed to re-create database table 'notes': %s" % e)

@note.route('/get', methods=['GET'])
def get_note():
    id = request.args.get('id')
    conn = db.create_connection()

    try:
        return str(db.select_note_by_id(conn, id))
    except Exception as e:
        note.logger.error("Error Getting Notes: %s" % e)
        return str([])


@note.route('/get-with-vuln', methods=['GET'])
def get_note_with_vulnerability():
    id = request.args.get('id')
    conn = db.create_connection()

    f = open("danger_zone.txt", "w")
    f.write("Add some text")
    f.close()

    os.chmod("danger_zone.txt", 777)

    with conn:
        try:
            return str(db.select_note_by_id(conn, id))
        except Exception as e:
            return "Failed to delete Note: %s" % e