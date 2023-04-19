from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
import requests
from flask_login import login_required, current_user
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import lxml
from . import db
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


@views.route('/novaSolicitacao', methods=['GET'])
@login_required
def novaSolicitacao():
    return render_template("novaSolicitacao.html", user=current_user)


@views.route('/formulario', methods=['GET'])
@login_required
def formulario():
    return render_template('formulario.html', user=current_user)


@views.route('/riscos', methods=['GET'])
@login_required
def riscos():
    return render_template("riscos.html", user=current_user)


@views.route('/closing', methods=['GET'])
@login_required
def closing():
    return render_template("closing.html", user=current_user)
