from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
import requests
from flask_login import login_required, current_user
import psycopg2
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import lxml
from . import db
from .creds import *
from .models import convertData, findValue, findCustomValue, convertText
import unicodedata
import json
import uuid

views = Blueprint('views', __name__)
views.secret_key = 'blablabla'

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

"""
Este código é a base do backend, tudo roda a partir daqui. As views criam a lógica que vai rodar
por trás do formulário. Cada uma delas aponta para um arquivo .html diferente e cada um desses
arquivos é construído na pasta templates.

É importante também usar os métodos corretos para cada formulário (GET, POST) para não crashar.

Caso sejam necessários scripts em Javascript, estes ficam na pasta static, junto com os arquivos
CSS.

Temos também o models.py, o auth.py, o __init__.py e o app.py, cada um com suas funcionalidades.
"""


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/novaSolicitacao', methods=['GET', 'POST'])
@login_required
def novaSolicitacao():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário
        session['ansList'] = [request.form.get('treino'), request.form.get(
            'equipBloq'), request.form.get('possuiEPI'), request.form.get('condFerramenta')]
        session['codart'] = uuid.uuid4()

        return redirect(url_for('views.formulario'))

    return render_template("novaSolicitacao.html", user=current_user)


@views.route('/formulario', methods=['GET', 'POST'])
@login_required
def formulario():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário
        ansList = session.get('ansList')
        codart = session.get('codart')
        print(ansList, codart)
        # session['ansList'].append(request.form.get('ferrManual'), request.form.get('ferrPneumatica'), request.form.get(
        #     'escada'), request.form.get('furadeira'), request.form.get('lixadeira'), request.form.get('solda'), request.form.get('corte'))
        # session['codRecursos'] = uuid.uuid4()
        return redirect(url_for('views.riscos'))

    return render_template('formulario.html', user=current_user)


@views.route('/riscos', methods=['GET', 'POST'])
@login_required
def riscos():
    if request.method == 'POST':
        session['codRiscos']
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário
        return redirect(url_for('views.closing'))

    return render_template("riscos.html", user=current_user)


@views.route('/closing', methods=['GET'])
@login_required
def closing():
    print(session['ansList'])
    print(session['codart'])
    # conn = psycopg2.connect(host = dbHost, database=dbName, user=dbUser, password=dbPass)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO recursosmateriais (column1, column2) VALUES (%s, %s)", (data['value1'], data['value2']))
    return render_template("closing.html", user=current_user)
