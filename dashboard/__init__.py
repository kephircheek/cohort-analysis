"""
General file for flask app.
Routes will add here.
"""

import os
import json
import shutil
from uuid import uuid4
from flask import Flask, render_template, redirect, url_for, request, session

from dashboard.skin import DASHBOARD, STATUS_LINE
from dashboard.tools import load, write, createfigure
from analytics.core import CohortAnalyser

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


# App routes


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
    logging.debug(f"Posted plot form: {request.form}")
    # [('cohort_types', 'Дата первого посещения'), ('cohort_sizes', 'по
    # месяцам'), ('targets', 'Пользователей'), ('date_range', 'За год')]
    token = session['token']
    data = {
        "token": token,
        "filename": request.form['file']
    }

    ch = CohortAnalyser(
        target=DASHBOARD['controls']['target']['options'][request.form['target']],
        cohort_type=DASHBOARD['controls']['cohort_type']['options'][request.form['cohort_type']],
        cohort_range=DASHBOARD['controls']['cohort_range']['options'][request.form['cohort_range']],
        date_range=DASHBOARD['controls']['date_range']['options'][request.form['date_range']]
    )

    for result in ch.analyse(data):
        write(result, token, 'figures')

    logging.debug(f"Make figures for user with token: {token}")
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    token = session['token']
    figures = [createfigure(json.loads(fig)) for fig in load(token, 'figures')]
    logging.debug(f'Loaded {len(figures)} figures.')
    logging.debug("Render dashboard page.")
    return render_template(
        'dashboard.html',
        dashboard=DASHBOARD,
        status_line=STATUS_LINE,
        files=os.listdir(f"storage/{token}/data"),
        figures=figures)

