from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
import pandas as pd
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # VALIDAÇÃO DO WEB SERVICE DO PRISMA

        url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
        headers = {'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="UTF-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                  <soap:Body>
                    <CheckUser xmlns="http://sisteplant.com/">
                      <user>""" + username + """</user>
                      <password>""" + password + """</password>
                      <company>MRVVT-ID02</company>
                    </CheckUser>
                  </soap:Body>
                </soap:Envelope>"""

        response = requests.post(url, data=body, headers=headers)
        soup = BeautifulSoup(response.content, features="xml")
        resp = soup.find_all('CheckUserResult')[0].text

        if resp == "OK":
            user = User.query.filter_by(username=username).first()
            if user:
                login_user(user, remember=False)
                flash('Logado com sucesso!', category='success')
            else:
                new_user = User(username=username, password=generate_password_hash(
                    password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user, remember=False)
                flash('Logado com sucesso!', category='success')

            return redirect(url_for('views.home'))

        elif resp == "Senha incorreta":
            flash('Senha Incorreta', category='error')

        else:
            flash('Usuário não existe.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
