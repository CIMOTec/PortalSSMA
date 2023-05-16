from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
import pandas as pd
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import psycopg2
from .creds import *
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session['username'] = username

        conn = psycopg2.connect(host=dbHost, database=dbName,
                                user=dbUser, password=dbPass)

        cursor = conn.cursor()

        query1 = f"SELECT senha FROM declarante WHERE cpf = '{username}'"
        cursor.execute(query1)
        rows = cursor.fetchone()

        try:
            passwordOk = check_password_hash(rows[0], password)
        except TypeError:
            passwordOk = False

        if passwordOk:
            user = User.query.filter_by(username=username).first()
            if user:
                login_user(user, remember=True)
                flash('Logado com sucesso!', category='success')
            else:
                new_user = User(username=username, password=generate_password_hash(
                    password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Logado com sucesso!', category='success')

            return redirect(url_for('views.home'))

        else:
            flash('Senha Incorreta ou cadastro não existe', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))
