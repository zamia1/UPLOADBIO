import pandas as pd
import numpy as np
import os
import glob
import json
 
import pprint
from json2html import *
from pymongo import MongoClient
from pathlib import Path
from flask import jsonify, Flask, render_template, request, send_file
from flask import Flask
import pdb
import ast
import os,subprocess
from bson.objectid import ObjectId
from itertools import chain
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import pdb
import base64
import gridfs
from io import BytesIO
import pymongo as pym
import gridfs
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)

# Configure a secret key for Flask-Login
app.secret_key =os.urandom(50)

url="http://127.0.0.1:5000"
# # Initialize Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'  # Specify the login route
FILE_SYSTEM_ROOT =os.getcwd()


client = MongoClient("mongodb+srv://mongodb:mongodb@cluster0.ps5mh8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Get and Post Route
bflag=True
db = client.dataghotkali
#allghotkali = db.dataghotkalicol
ghotkali_collection = db['ghotali']
users_collection = db['users']


def connectToDb(namesp):
    fs = gridfs.GridFS(db,namesp)
    return db, ghotkali_collection, fs

@app.route('/register', methods=['GET', 'POST'])
def register():
    pdb.set_trace()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/',methods=['GET', 'POST'])
def login():
    pdb.set_trace()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            #flash('Login successful.', 'success')
            return render_template('home.html',url=url)
            # Add any additional logic, such as session management
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')
@app.route('/get_file/<name>/<gender>')
@app.route('/get_file', methods=['GET','POST'])
def get_file(name=None,gender=None):
    pdb.set_trace()
    
    if request.method=="POST":
        
    #fs = gridfs.GridFS(MongoClient().CINEfs_example)

        if name is not None:
            f = fs.get_last_version(name)
            r = app.response_class(f, direct_passthrough=True, mimetype='application/octet-stream')
            r.headers.set('Content-Disposition', 'attachment', filename=name)
            return r
        else:
            gender=request.form['gender']
            age=request.form['age']
            db, collectn, fs = connectToDb(gender+age)
            return render_template('get_file.html', names=fs.list())
    return render_template('filter.html')




@app.route('/upload', methods=['GET','POST'])
def upload_file():
    pdb.set_trace()
    if request.method == "POST":
        names=request.form['names']
        age=request.form['age']
        db, collectn, fs = connectToDb(names+age)
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and file.filename.endswith('.pdf'):
            file_id = fs.put(file, filename=file.filename)
           # return jsonify({'file_id': str(file_id)}), 201
            return jsonify({'file is uploaded'}), 201
        else:
            return jsonify({'error': 'Only PDF files are allowed'}), 400
    else:
        return render_template('index.html')



# # Create a User model (you'll need to implement this with your database)
# class User(UserMixin):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def get_id(self):
#         return str(self.id)

# # Load a user from the database
# @login_manager.user_loader
# def load_user(user_id):
#     # Replace this with your database logic
#     if user_id == '1':
#         return User(1, 'admin', 'password')
#     return None

# Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # Replace this with your database logic
#         if username == 'admin' and password == 'password':
#             user = load_user('1')
#             login_user(user)
#             return redirect(url_for('index'))
#         else:
#             return 'Invalid username or password'
#     return render_template('login.html')

# # Protected route
# @app.route('/')
# @login_required
# def index():
#     return 'Hello, authenticated user!'

# # Logout route
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


