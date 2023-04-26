from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import queue
import requests
import threading
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
    resp = f"{dia}/{mes}/{ano} {hora}:{minutos}"
    return int(resp)


def convertText(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join(
        [c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9]', ' ', palavraSemAcento)


def findValue(validator):
    resposta = ''
    if validator == "Mensageria":
        resposta = "MSG"
    elif validator == "Gerência e Administração":
        resposta = "GER"
    elif validator == "Serviços Gerais":
        resposta = "SGR"
    elif validator == "Refrigeração":
        resposta = "CLR"
    elif validator == "Elétrica":
        resposta = "ELE"
    elif validator == "Hidráulica":
        resposta = "HID"
    elif validator == "Civil":
        resposta = "CIV"
    elif validator == "Limpeza":
        resposta = "LIM"

    return resposta


def findCustomValue(validator):
    resposta = ''
    if (validator == "SERVICO DE CARTÓRIO"):
        resposta = "MENS001"
    elif (validator == "ENTREGA/RETIRADA DE DOCUMENTOS"):
        resposta = "MENS002"
    elif (validator == "MENSAGERIA INTERNA - UNIDADE SEDE RJ"):
        resposta = "MENS003"
    elif (validator == "MENSAGERIA MATERIAIS PARA PUBLICIDADE - ENVIO NORMAL"):
        resposta = "MENS004"
    elif (validator == "MENSAGERIA MATERIAIS PARA PUBLICIDADE - ENVIO EMERGENCIAL"):
        resposta = "MENS005"
    elif (validator == "MENSAGERIA MATERIAIS PROMOCIONAIS - ENVIO NORMAL"):
        resposta = "MENS006"
    elif (validator == "MENSAGERIA MATERIAIS PROMOCIONAIS - ENVIO EMERGENCIAL"):
        resposta = "MENS007"
    elif (validator == "MENSAGERIA MATERIAIS PLV - ENVIO NORMAL"):
        resposta = "MENS008"
    elif (validator == "MENSAGERIA MATERIAIS PLV - ENVIO EMERGENCIAL"):
        resposta = "MENS009"
    elif (validator == "MENSAGERIA MATERIAIS PARA EXECUTIVOS OU BA´s ENVIO NORMAL"):
        resposta = "MENS010"
    elif (validator == "MENSAGERIA MATERIAIS PARA EXECUTIVOS OU BA´s ENVIO EMERGENCIAL"):
        resposta = "MENS011"
    elif (validator == "MENSAGERIA ENVIOS DO CORPORATE / INSTITUCIONAL - ENVIO NORMAL"):
        resposta = "MENS012"
    elif (validator == "MENSAGERIA ENVIOS DO CORPORATE / INSTITUCIONAL - ENVIO EMERGENCIAL"):
        resposta = "MENS013"
    elif (validator == "MENSAGERIA MATERIAIS PARA RELAÇÕES PÚBLICAS - ENVIO NORMAL"):
        resposta = "MENS014"
    elif (validator == "MENSAGERIA MATERIAIS PARA RELAÇÕES PÚBLICAS - ENVIO EMERGENCIAL"):
        resposta = "MENS015"
    elif (validator == "SERVIÇO DE CARTÓRIO - RECONHECIMENTO DE FIRMA"):
        resposta = "MENS016"
    elif (validator == "SOLICITACOES DE CAIXA"):
        resposta = "MENS017"
    elif (validator == "SOLICITACOES DE ENVELOPE"):
        resposta = "MENS018"
    elif (validator == "SERVIÇOS BANCÁRIOS - PEDIDO FEITO APÓS AS 15H, SERÁ ATENDIDO NO PRÓXIMO DIA UTIL"):
        resposta = "MENS019"
    elif (validator == "SERVIÇOS BANCÁRIOS - PEDIDO FEITO APÓS AS 12H, SERÁ ATENDIDO NO PRÓXIMO DIA UTIL"):
        resposta = "MENS021"
    elif (validator == "COPIA DA CHAVE DO LOCKER - R$ 10,00"):
        resposta = "GADM008"
    elif (validator == "ABERTURA DO LOCKER R$ 25,00"):
        resposta = "GADM010"
    elif (validator == "CONFECÇÃO DE CHAVE PARA LOCKER  MAIS CÓPIA R$ 55,00"):
        resposta = "GADM011"
    elif (validator == "CARIMBO"):
        resposta = "GADM012"
    elif (validator == "SOLICITAR SERVIÇOS DE CHAVEIRO"):
        resposta = "GADM027"
    elif (validator == "ABERTURA DE ARMÁRIOS"):
        resposta = "GADM029"
    elif (validator == "SOLICITAÇÃO DE ARMÁRIO LOCKER"):
        resposta = "GADM030"
    elif (validator == "SOLICITAÇÃO ALTERAÇÃO DE ANDAR PARA LOCKER"):
        resposta = "GADM031"
    elif (validator == "MATERIAL DE DESTRUIÇÃO"):
        resposta = "SGER009"
    elif (validator == "RECOLHIMENTO E DESTRUIÇÃO DE PAPEL CONFIDENCIAL"):
        resposta = "SGER007"

    return resposta