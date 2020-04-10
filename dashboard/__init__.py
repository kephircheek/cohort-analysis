"""
General file for flask app.
Routes will add here.
"""

import os
from uuid import uuid4
from flask import Flask, render_template, redirect, url_for, request, session
import logging
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.DEBUG
)

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# app routes
@app.route('/')
@app.route('/welcome', methods=['GET'])
def welcome():
    if ('token' not in session
         or 'storage' not in os.listdir('.')
         or session['token'] not in os.listdir("storage")):
        session['token'] = str(uuid4())
        os.makedirs(f"storage/{session['token']}")
        logging.debug(f"Token was created: {session['token']}")

    logging.debug(f"Render welcome page.")
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'token' not in session:
        logging.debug(f"Not token in session: redirect to welcome.")
        return redirect(url_for('welcome'))

    token = session['token']
    logging.debug(f"Upload file with token: {session['token']}")
    f = request.files['data']
    logging.debug(f"Uploaded file {f.filename}")
    _, extention = os.path.splitext(os.path.basename(f.filename))
    f.save(f'storage/{token}/{f.filename}')
    logging.debug(f"Saved file {f.filename} to storage/{token}/{f.filename}")
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    logging.debug(f"Render dashboard page.")
    return (
        "Uploaded files:\n" +
        '\n'.join(os.listdir(f"storage/{session['token']}"))
    )
