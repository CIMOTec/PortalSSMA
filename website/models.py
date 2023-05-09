from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import unicodedata
import re


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')


def convertData(data):
    # global ano, mes, dia, hora, minutos,resp
    ano = data[0:4]
    mes = data[5:7]
    dia = data[8:10]
    hora = data[11:13]
    minutos = data[14:16]
    resp = f"'{ano}-{mes}-{dia} {hora}:{minutos}:00'"
    return resp


def convertText(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join(
        [c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9]', ' ', palavraSemAcento)