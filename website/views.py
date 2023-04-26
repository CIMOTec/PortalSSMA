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

views = Blueprint('views', __name__)

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
        print(request.form.get('treino'))
        print(request.form.get('equipBloq'))
        print(request.form.get('possuiEPI'))
        print(request.form.get('condFerramenta'))
        return redirect(url_for('views.formulario'))

    return render_template("novaSolicitacao.html", user=current_user)


@views.route('/formulario', methods=['GET', 'POST'])
@login_required
def formulario():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário
        print(request.form.get('ferrManual'))
        print(request.form.get('ferrPneumatica'))
        print(request.form.get('escada'))
        print(request.form.get('furadeira'))
        print(request.form.get('lixadeira'))
        print(request.form.get('solda'))
        print(request.form.get('corte'))
        return redirect(url_for('views.riscos'))
    
    return render_template('formulario.html', user=current_user)


@views.route('/riscos', methods=['GET', 'POST'])
@login_required
def riscos():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário
        print(request.form.get('aprisionamento'))
        print(request.form.get('projecao'))
        print(request.form.get('sistema'))
        print(request.form.get('aclive'))
        print(request.form.get('falta'))
        print(request.form.get('inundacao'))
        print(request.form.get('trabalhoQuente'))
        print(request.form.get('ferramenta'))
        print(request.form.get('superficie'))
        print(request.form.get('atropelamento'))
        print(request.form.get('bater'))
        print(request.form.get('vibração'))
        print(request.form.get('umidade'))
        print(request.form.get('iluminacao'))
        print(request.form.get('transportePessoas'))
        print(request.form.get('calor'))
        print(request.form.get('incendio'))
        print(request.form.get('animais'))
        print(request.form.get('carga'))
        print(request.form.get('instalacao'))
        print(request.form.get('trabalho'))
        print(request.form.get('cilindros'))
        print(request.form.get('subst'))
        print(request.form.get('transporteMaterial'))
        print(request.form.get('tubulacao'))
        print(request.form.get('maVisibilidade'))
        print(request.form.get('tombamento'))
        print(request.form.get('pressao'))
        print(request.form.get('materiais'))
        print(request.form.get('transporte'))
        print(request.form.get('gasesEtc'))
        print(request.form.get('falhas'))
        print(request.form.get('ventilacao'))
        print(request.form.get('perfurocortante'))
        print(request.form.get('choque'))
        print(request.form.get('espaçoLimitado'))
        print(request.form.get('pisoRotativo'))
        print(request.form.get('pisoIrregular'))
        print(request.form.get('postura'))
        print(request.form.get('deslocamento'))
        print(request.form.get('espaçoConfinado'))
        print(request.form.get('desmoronamento'))
        print(request.form.get('explosao'))
        print(request.form.get('equipIcamento'))
        print(request.form.get('escada'))
        print(request.form.get('queda'))
        print(request.form.get('rompimento'))
        print(request.form.get('riscosTerceiros'))
        print(request.form.get('ruido'))
        print(request.form.get('outros'))
        return redirect(url_for('views.closing'))
    
    return render_template("riscos.html", user=current_user)


@views.route('/closing', methods=['GET'])
@login_required
def closing():
    # conn = psycopg2.connect(host = dbHost, database=dbName, user=dbUser, password=dbPass)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (data['value1'], data['value2']))
    return render_template("closing.html", user=current_user)
