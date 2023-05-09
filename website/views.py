from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
import requests
from flask_login import login_required, current_user
import psycopg2
import pandas as pd
import datetime
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

flagGlobal = 0

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


def prepList(workList):
    """ESSA FUNÇÃO É IMPORTANTE PACAS, BORA LÁ:

    Ela separa o dicionário de respostas do formulário em uma string usada no INSERT lá embaixo

    Um detalhe importante é a inclusão das aspas simples nas respostas. Quase todos os campos
    precisam ter essas aspas incluídas pro comando SQL funcionar.

    Alguns campos já recebem essas aspas no momento da declaração e outros são incluídos aqui. 
    """
    tripaColuna = []
    tripaDado = []

    for key in workList:
        print(f"{key} : {workList[key]}")
        tripaColuna.append(key)
        if workList[key] == None:
            tripaDado.append('FALSE')
        else:
            tripaDado.append(workList[key])

    separador = ', '
    tripaColuna = separador.join(tripaColuna)
    tripaDado = separador.join(tripaDado)
    tripaDado = f"{tripaDado}"
    return tripaColuna, tripaDado


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/novaSolicitacao', methods=['GET', 'POST'])
@login_required
def novaSolicitacao():
    global flagGlobal
    flagGlobal += 1
    print(f"\n\n\nVariável Global: {flagGlobal}\n\n\n")

    if request.method == 'POST':
        session['flag'] = True
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário
        session['ansListArt'] = dict(
            treinado=request.form.get('treinado'),
            equipbloqueado=request.form.get('equipbloqueado'),
            possuiepi=request.form.get('possuiepi'),
            condferramenta=request.form.get('condferramenta'),
            tarefa=f"'{request.form.get('tarefa')}'",
            local=f"'{request.form.get('local')}'",
            contrato=f"'{request.form.get('contrato')}'",
            datauser=convertData(request.form.get('datauser')),
            ativrotina=request.form.get('ativrotina'),
            numeroos=f"'{request.form.get('numeroos')}'")

        # esse comando cria o código único para ser utilizado como chave no banco
        session['codart'] = str(uuid.uuid4())

        return redirect(url_for('views.formulario'))

    return render_template("novaSolicitacao.html", user=current_user)


@views.route('/escada', methods=['GET', 'POST'])
@login_required
def escada():
    if request.method == 'POST':
        session['ansListEscada'] = dict(
            numescada=f"'{request.form.get('numescada')}'")

        if request.form.get('escadatipo') == 'tesoura':
            session['ansListEscadaTipo'] = dict(
                tamanhoescada=f"'{request.form.get('tamanhoescada')}'",
                materialescada=request.form.get('materialescada'),
                degraus=request.form.get('degraus'),
                montantes=request.form.get('montantes'),
                etiqueta=request.form.get('etiqueta'),
                patamarsuperior=request.form.get('patamarsuperior'),
                topo=request.form.get('topo'),
                sapatas=request.form.get('sapatas'),
                geral=request.form.get('geral'),
                outros=f"'{request.form.get('outros')}'",
                acao=f"'{request.form.get('acao')}'")

        else:
            session['ansListEscadaTipo'] = dict(
                tamanhoescada=f"'{request.form.get('tamanhoescada')}'",
                materialescada=request.form.get('materialescada'),
                degraus=request.form.get('degraus'),
                montantes=request.form.get('montantes'),
                etiqueta=request.form.get('etiqueta'),
                catracadeseguranca=request.form.get('catracadeseguranca'),
                sapatas=request.form.get('sapatas'),
                cordapolia=request.form.get('cordapolia'),
                geral=request.form.get('geral'),
                outros=f"'{request.form.get('outros')}'",
                acao=f"'{request.form.get('acao')}'")

        session['codescada'] = str(uuid.uuid4())

        # esse IF statement controla o fluxo da aplicação. Se o formulário de escada foi acessado a partir da art,
        # ele envia para o próximo passo. Senão, executa o insert no banco

        if session.get('flag'):
            session['flag'] = False
            session['escadatipo'] = request.form.get('escadatipo')
            return redirect(url_for('views.epis'))

        else:
            tripaDado, tripaCol = prepList(session.get('ansListEscada'))
            tripaDado2, tripaCol2 = prepList(session.get('ansListEscadaTipo'))

            conn = psycopg2.connect(host=dbHost, database=dbName,
                                    user=dbUser, password=dbPass)
            cursor = conn.cursor()

            insert1 = f"INSERT INTO escadadados (codescada, declarante, {tripaDado}, dataescada) VALUES ('{session.get('codescada')}', '{session.get('username')}', {tripaCol}, '{datetime.datetime.now()}');"
            if request.form.get('escadatipo') == 'tesoura':
                insert2 = f"INSERT INTO escadatesoura (codescada, {tripaDado2}) VALUES ('{session.get('codescada')}', {tripaCol2});"

            else:
                insert2 = f"INSERT INTO escadaextensivel (codescada, {tripaDado2}) VALUES ('{session.get('codescada')}', {tripaCol2});"

            cursor.execute(insert1)
            cursor.execute(insert2)
            conn.commit()
            conn.close()

        return redirect(url_for('views.home'))

    return render_template("escada.html", user=current_user)


@views.route('/formulario', methods=['GET', 'POST'])
@login_required
def formulario():
    global flagGlobal
    flagGlobal += 1
    print(f"\n\n\nVariável Global: {flagGlobal}\n\n\n")
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário

        session['ansListRec'] = dict(
            ferrmanual=request.form.get('ferrmanual'),
            ferrpneumatica=request.form.get('ferrpneumatica'),
            escada=request.form.get('escada'),
            furadeira=request.form.get('furadeira'),
            lixadeira=request.form.get('lixadeira'),
            solda=request.form.get('solda'),
            oxicorte=request.form.get('oxicorte'))

        session['codrecursos'] = str(uuid.uuid4())

        if request.form.get('escada') == 'TRUE':
            return redirect(url_for('views.escada'))
        else:
            return redirect(url_for('views.epis'))

    return render_template('formulario.html', user=current_user)

@views.route('/epis', methods=['GET', 'POST'])
@login_required
def epis():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário

        session['ansListEpis'] = dict(
            avental=request.form.get('avental'),
            bota=request.form.get('bota'),
            botina=request.form.get('botina'),
            blusao=request.form.get('blusao'),
            capacete=request.form.get('capacete'),
            cinto=request.form.get('cinto'),
            conjunto=request.form.get('conjunto'),
            camiscalca=request.form.get('camiscalca'),
            creme=request.form.get('creme'),
            luva=request.form.get('luva'),
            mascarafuga=request.form.get('mascarafuga'),
            mascarasolda=request.form.get('mascarasolda'),
            mangote=request.form.get('mangote'),
            oculosseg=request.form.get('oculosseg'),
            oculosmacarico=request.form.get('oculosmacarico'),
            perneira=request.form.get('perneira'),
            protfacial=request.form.get('protfacial'),
            protarco=request.form.get('protarco'),
            resppoeiras=request.form.get('resppoeiras'),
            respvapores=request.form.get('respvapores'))

        session['codepis'] = str(uuid.uuid4())

        return redirect(url_for('views.riscos'))

    return render_template('epis.html', user=current_user)

@views.route('/riscos', methods=['GET', 'POST'])
@login_required
def riscos():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário

        session['codriscos'] = str(uuid.uuid4())
        session['ansListRiscos'] = dict(
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
            outros=f"'{request.form.get('outros')}'"
        )

        return redirect(url_for('views.acoes'))

    return render_template("riscos.html", user=current_user)

@views.route('/acoes', methods=['GET', 'POST'])
@login_required
def acoes():
    if request.method == 'POST':
        # esse é o comando utilizado pra pegar as informações preenchidas no formulário

        session['codacoes'] = str(uuid.uuid4())
        session['ansListAcoes'] = dict(
            aterramento=request.form.get('aterramento'),
            enclausuramento=request.form.get('enclausuramento'),
            iluminacao=request.form.get('iluminacao'),
            passarela=request.form.get('passarela'),
            isolamento=request.form.get('isolamento'),
            limpeza=request.form.get('limpeza'),
            extintor=request.form.get('extintor'),
            sinalizacao=request.form.get('sinalizacao'),
            tela=request.form.get('tela'),
            travamento=request.form.get('travamento'),
            ventilacao=request.form.get('ventilacao'),
            portateis=request.form.get('portateis'),
            ferrisolantes=request.form.get('ferrisolantes'),
            outrosacoes=f"'{request.form.get('outrosacoes')}'"            
        )

        return redirect(url_for('views.closing'))

    return render_template("acoes.html", user=current_user)


@views.route('/closing', methods=['GET'])
@login_required
def closing():
    conn = psycopg2.connect(host=dbHost, database=dbName,
                            user=dbUser, password=dbPass)
    cursor = conn.cursor()

    tripaArt, tripaArtCol = prepList(session.get('ansListArt'))
    tripaRec, tripaRecCol = prepList(session.get('ansListRec'))
    tripaRiscos, tripaRiscosCol = prepList(session.get('ansListRiscos'))
    tripaEpis, tripaEpisCol = prepList(session.get('ansListEpis'))
    tripaAcoes, tripaAcoesCol = prepList(session.get('ansListAcoes'))

    css1 = f"INSERT INTO art ({tripaArt}, codart, codrecursos, codriscos, data, codepis, codacoes) VALUES ({tripaArtCol},'{session.get('codart')}','{session.get('codrecursos')}','{session.get('codriscos')}', '{datetime.datetime.now()}','{session.get('codepis')}','{session.get('codacoes')}');"
    css2 = f"INSERT INTO recursosmateriais ({tripaRec}, codrecursos) VALUES ({tripaRecCol},'{session.get('codrecursos')}');"
    css3 = f"INSERT INTO riscospontenciais ({tripaRiscos}, codriscos) VALUES ({tripaRiscosCol},'{session.get('codriscos')}');"
    css7 = f"INSERT INTO epis ({tripaEpis}, codepis) VALUES ({tripaEpisCol},'{session.get('codepis')}');"
    css8 = f"INSERT INTO acoes ({tripaAcoes}, codacoes) VALUES ({tripaAcoesCol},'{session.get('codacoes')}');"

    if session.get('codescada'):
        tripaEscada, tripaEscadaCol = prepList(session.get('ansListEscada'))
        tripaEscada2, tripaEscadaCol2 = prepList(
            session.get('ansListEscadaTipo'))

        css4 = f"INSERT INTO escadadados (codescada, codart, declarante, {tripaEscada}) VALUES ('{session.get('codescada')}', '{session.get('codart')}', '{session.get('username')}', {tripaEscadaCol});"

        if session.get('escadatipo') == 'tesoura':
            css5 = f"INSERT INTO escadatesoura (codescada, {tripaEscada2}) VALUES ('{session.get('codescada')}', {tripaEscadaCol2});"
        else:
            css5 = f"INSERT INTO escadaextensivel (codescada, {tripaEscada2}) VALUES ('{session.get('codescada')}', {tripaEscadaCol2});"

    css6 = f"INSERT INTO artdeclarante (coddeclarante, codart) VALUES ('{session.get('username')}', '{session.get('codart')}')"

    # a ordem dos inserts é muito importante para respeitar os vínculos criados no db
    cursor.execute(css8)
    cursor.execute(css7)
    cursor.execute(css3)
    cursor.execute(css2)
    cursor.execute(css1)

    try:
        cursor.execute(css4)
        cursor.execute(css5)
    except UnboundLocalError:
        pass

    cursor.execute(css6)

    conn.commit()
    conn.close()

    return render_template("closing.html", user=current_user)
