"""
General file for flask app.
Routes will add here.
"""

import os
import shutil
from uuid import uuid4
from flask import Flask, render_template, redirect, url_for, request, session

from dashboard.skin import DASHBOARD, STATUS_LINE
from dashboard.tools import load

import logging
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.DEBUG
)

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

if 'storage' not in os.listdir('.'):
    os.makedirs('storage')

# app routes

@app.route('/')
@app.route('/welcome', methods=['GET'])
def welcome():
    if 'token' in session and session['token'] not in os.listdir("storage"):
       shutil.rmtree(f'storage/{session["token"]}', ignore_errors=True)

    session['token'] = str(uuid4())
    token = session['token']
    os.makedirs(f"storage/{token}")
    os.makedirs(f"storage/{token}/data")
    os.makedirs(f"storage/{token}/figures")
    logging.debug(f"Token was created: {session['token']}")

    logging.debug(f"Render welcome page.")
    return render_template('welcome.html', status_line=STATUS_LINE)


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
    f.save(f'storage/{token}/data/{f.filename}')
    logging.debug(f"Saved file {f.filename} to storage/{token}/data/{f.filename}")
    return redirect(url_for('dashboard'))


@app.route('/plot', methods=['POST'])
def plot():
    if 'token' not in session:
        logging.debug(f"Not token in session: redirect to welcome.")
        return redirect(url_for('welcome'))
    logging.debug(f"Posted plot form:\n"
                  f"args: {request.args}\n"
                  f"form: {request.form}\n"
                  f"valus: {request.values}"
    )
    token = session['token']
    logging.debug(f"Make figures for user with token: {token}")
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    token = session['token']
    figures = [load(fig) for fig in os.listdir(f"storage/{token}/figures")]
    logging.debug(f'Loaded {len(figures)} figures.')
    logging.debug(f"Render dashboard page.")
    return render_template(
        'dashboard.html',
        dashboard=DASHBOARD,
        status_line=STATUS_LINE,
        figures=figures)

