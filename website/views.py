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


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user, requesterName=session['requesterName'])


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
def closing():
    return render_template("riscos.html", user=current_user)
