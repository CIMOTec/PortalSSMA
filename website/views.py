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
        session['ansList1'] = dict(
            treinado=request.form.get('treinado'),
            equipbloqueado=request.form.get('equipbloqueado'),
            possuiepi=request.form.get('possuiepi'),
            condferramenta=request.form.get('condferramenta'))

        session['codart'] = uuid.uuid4()

        return redirect(url_for('views.formulario'))

    return render_template("novaSolicitacao.html", user=current_user)


@views.route('/formulario', methods=['GET', 'POST'])
@login_required
def formulario():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário

        session['ansList2'] = dict(
            ferrManual=request.form.get('ferrManual'),
            ferrPneumatica=request.form.get('ferrPneumatica'),
            escada=request.form.get('escada'),
            furadeira=request.form.get('furadeira'),
            lixadeira=request.form.get('lixadeira'),
            solda=request.form.get('solda'),
            corte=request.form.get('corte'))

        session['codrecursos'] = uuid.uuid4()
        return redirect(url_for('views.riscos'))

    return render_template('formulario.html', user=current_user)


@views.route('/riscos', methods=['GET', 'POST'])
@login_required
def riscos():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário

        session['codriscos'] = uuid.uuid4()
        session['ansList3'] = dict(
            aprisionamento=request.form.get('aprisionamento'),
            projecao=request.form.get('projecao'),
            sistema=request.form.get('sistema'),
            aclive=request.form.get('aclive'),
            falta=request.form.get('falta'),
            inundacao=request.form.get('inundacao'),
            trabalhoQuente=request.form.get('trabalhoQuente'),
            ferramenta=request.form.get('ferramenta'),
            superficie=request.form.get('superficie'),
            atropelamento=request.form.get('atropelamento'),
            bater=request.form.get('bater'),
            vibração=request.form.get('vibração'),
            umidade=request.form.get('umidade'),
            iluminacao=request.form.get('iluminacao'),
            transportePessoas=request.form.get('transportePessoas'),
            calor=request.form.get('calor'),
            incendio=request.form.get('incendio'),
            animais=request.form.get('animais'),
            carga=request.form.get('carga'),
            instalacao=request.form.get('instalacao'),
            trabalho=request.form.get('trabalho'),
            cilindros=request.form.get('cilindros'),
            subst=request.form.get('subst'),
            transporteMaterial=request.form.get('transporteMaterial'),
            tubulacao=request.form.get('tubulacao'),
            maVisibilidade=request.form.get('maVisibilidade'),
            tombamento=request.form.get('tombamento'),
            pressao=request.form.get('pressao'),
            materiais=request.form.get('materiais'),
            transporte=request.form.get('transporte'),
            gasesEtc=request.form.get('gasesEtc'),
            falhas=request.form.get('falhas'),
            ventilacao=request.form.get('ventilacao'),
            perfurocortante=request.form.get('perfurocortante'),
            choque=request.form.get('choque'),
            espaçoLimitado=request.form.get('espaçoLimitado'),
            pisoRotativo=request.form.get('pisoRotativo'),
            pisoIrregular=request.form.get('pisoIrregular'),
            postura=request.form.get('postura'),
            deslocamento=request.form.get('deslocamento'),
            espaçoConfinado=request.form.get('espaçoConfinado'),
            desmoronamento=request.form.get('desmoronamento'),
            explosao=request.form.get('explosao'),
            equipIcamento=request.form.get('equipIcamento'),
            escada=request.form.get('escada'),
            queda=request.form.get('queda'),
            rompimento=request.form.get('rompimento'),
            riscosTerceiros=request.form.get('riscosTerceiros'),
            ruido=request.form.get('ruido'),
            outros=request.form.get('outros')
        )

        return redirect(url_for('views.closing'))

    return render_template("riscos.html", user=current_user)


@views.route('/closing', methods=['GET'])
@login_required
def closing():
    conn = psycopg2.connect(host=dbHost, database=dbName,
                            user=dbUser, password=dbPass)
    cursor = conn.cursor()
    print(session.get('ansList3'))

    # for key, value in session.get('ansList3'):
    #     tripaColuna = str(tripaColuna) + (',') + str(key)
    #     tripaDado = str(tripaDado) + (',') + str(value)

    cursor.execute(
        # f"INSERT INTO riscospotenciais ({tripaColuna},'codriscos','codart') VALUES ({tripaDado},{session.get('codriscos')},{session.get('codart')})")
        f"INSERT INTO riscospotenciais (codriscos) VALUES {session.get('codriscos')}")

    return render_template("closing.html", user=current_user)
