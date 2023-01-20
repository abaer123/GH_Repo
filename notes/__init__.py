import os

from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash

note = Flask(__name__)
note.config.from_object(Config)
bootstrap = Bootstrap(note)
auth = HTTPBasicAuth()
db_backend = os.environ.get("NOTES_DB_BACKEND", "local")

users = {
    "admin": generate_password_hash("yeet")
}

from notes import db, routes

sql_create_notes_table = """CREATE TABLE IF NOT EXISTS notes (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            data TEXT);"""

if db_backend == 'mariadb':
    sql_create_notes_table = """CREATE TABLE IF NOT EXISTS notes (
                                id INTEGER NOT NULL AUTO_INCREMENT,
                                data TEXT,
                                PRIMARY KEY (id));"""

conn = db.create_connection()

if conn is not None:
    db.create_table(conn, sql_create_notes_table)
else:
    note.logger.error("Error! cannot create the database connection.")

# SAST Vulnerability
compute_user_input = input('\nType something here to compute: ')
if not compute_user_input:
	print ("No input")
else:
	print ("Result: ", eval(compute_user_input))

# Another Vulnerability

# var to assert 
var_to_assert = "foo"

# if condition returns True, then nothing happens:
assert var_to_assert == "foo"

# if condition returns False, AssertionError is raised (comment out to test the next one):
assert var_to_assert == "bar"

# if condition returns False, custom AssertionError is raised: 
assert var_to_assert == "bar", f"Variable var_to_assert should be '{var_to_assert}'"

# run like this to disable assert statements: python3 -O py_vuln03.py
print("When you run code with -O, assert statements are skipped...")

#Vulernable code
def update_details(request, acc_id):  
  user = Account.objects.get(acc=acc_id)  
  if request.user.id == user.id:  
    # ALLOW ACTION  
    # VALIDATE REQUEST DATA  
    form = AccountForm(instance=user,request=request)  
    ...  
  else:  
    # DENY ACTION
    raise Exception("User ID of request does not match DB")
