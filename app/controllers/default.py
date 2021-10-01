# -*- coding: utf-8 -*-



#arquivo princpal da regra de negocio das nossas aplicacao
#ira controlar toda nossas nossa aplicacao por meio das rotas de protocolo http

from flask import render_template, request, url_for, redirect, flash, jsonify,session, abort, redirect
from app import  app, db
from telebot import types

#Biblioteca para o bot do telegram
import telebot
import urllib

#configurações do bot
chave_api = "2031294195:AAGLZVrZ4pA5w45u4fmpyRq"
bot = telebot.TeleBot(chave_api)

#from app.models.tables import Pessoas
from app.models.tables import *

#-------------------------- login --------------------------#
#-------------------------- login --------------------------#
#-------------------------- login --------------------------#

#google
import os
import pathlib

import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app.secret_key = "CodeSpecialist.com"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "646561352344-k00r23h9lfel4s1spjpetto3bcvr57r0.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


#-------------------------- index --------------------------#
#-------------------------- index --------------------------#
#-------------------------- index --------------------------#

#@app.route('/')
#def login():
#    return render_template('login.html')

#@app.route('/index')
#def index():
#    return render_template('index.html')

#-------------------------- cliente --------------------------#
#-------------------------- cliente --------------------------#
#-------------------------- cliente --------------------------#

@app.route('/clientes')
def clientes():
    clientes = Cliente.list_cliente()

    return render_template('clientes.html', clientes=clientes)

@app.route('/cliente/cadastrar')
def cliente_cadastrar():
    return render_template('cliente_cadastrar.html')

@app.route('/cliente/cadastrar/salvar',methods=['POST'])
def cliente_cadastrar_salvar():
    nome_cliente = request.form['nome_cliente']
    cep_cliente = request.form['cep']
    rua_cliente = request.form['endereco']
    bairro_cliente = request.form['bairro']
    data_nascimento_cliente = request.form['data_nascimento_cliente']
    CPF_cliente = request.form['CPF_cliente']
    email_cliente = request.form['email_cliente']
    telefone_celular = request.form['telefone_celular']

    cliente = Cliente(nome_cliente,cep_cliente, rua_cliente,bairro_cliente,
   data_nascimento_cliente,CPF_cliente,email_cliente,telefone_celular)
    
    cliente.save_cliente()

    return redirect(url_for('clientes'))


@app.route('/cliente/editar/<int:codigo_cliente>')
def cliente_editar(codigo_cliente=0):
    cliente = Cliente.find_cliente(codigo_cliente)

    return render_template('cliente_editar.html', cliente=cliente)


@app.route ('/cliente/editar/salvar', methods=['POST']) 
def cliente_editar_salvar(): 
    #recupera campos do formulario
    codigo_cliente= int(request.form['codigo_cliente'])
    nome_cliente = request.form['nome_cliente']
    email_cliente = request.form['email_cliente']
    telefone_celular = request.form['telefone_celular']
    CPF_cliente = request.form['CPF_cliente']
    cep_cliente = request.form['cep']
    rua_cliente = request.form['endereco']
    data_nascimento_cliente = request.form['data_nascimento_cliente']
    bairro_cliente = request.form['bairro']
    #string to datetime object
    data_nascimento_obj = datetime.strptime(data_nascimento_cliente,'%Y-%m-%d').date()
    #data_nascimento_obj = datetime.utcnow()

    cliente_encontrado = Cliente.find_cliente(codigo_cliente)
    if cliente_encontrado:
        cliente_encontrado.update_cliente(nome_cliente,email_cliente,telefone_celular,CPF_cliente,cep_cliente,rua_cliente,bairro_cliente,data_nascimento_cliente)
        cliente_encontrado.save_cliente()
        flash("Edicao Salva!",category="success")

    return redirect(url_for("clientes"))


#-------------------------- login --------------------------#
#-------------------------- login --------------------------#
#-------------------------- login --------------------------#

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logar") #rota logar dentro do template login para efetivar acesso
def logar():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    #return redirectgitgit(url_for(index))
    return redirect(url_for("protected_area")) #direcionar para tela principal, porem com a rota protected_area . Ela utiliza o objeto session


@app.route("/logout")
def logout():
    session.clear() # limpa objeto
    #return redirect("index")
    return redirect(url_for("login") ) #direcionar para tela de login 


@app.route("/")
def index():
    #return "Hello World <a href='/login'><button>Login</button></a>"
    return render_template("index.html")

@app.route("/protected_area") #
#@login_is_required
def protected_area():
    
    #return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    #return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    return render_template("index.html", usuario_nome_completo=session['name'])

#-------------------------- BOT --------------------------#
#-------------------------- BOT --------------------------#
#-------------------------- BOT --------------------------#

#Opção de fotos das decorações
def finalidades(mensagem):
    imagens = {'HomeOffice': ['D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/homeoffice1.jpg', 'D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/homeoffice2.png'],
                'Sala': ['D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/sala1.jpg', 'D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/sala2.jpg'],
                'Suite': ['D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/suite1.jpg', 'D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/suite2.jpg'],
                'Quarto': ['D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/quarto1.jpg', 'D:/Documentos/Arquivos faculdade/5Semestre/APP/DecorStadia/app/images/quarto2.jpg']
                }
    if mensagem.text == '/HomeOffice':
        bot.send_photo(mensagem.chat.id, photo=open(imagens['HomeOffice'][0], 'rb'))
        bot.send_photo(mensagem.chat.id, photo=open(imagens['HomeOffice'][1], 'rb'))
    elif mensagem.text == '/Sala':
        bot.send_photo(mensagem.chat.id, photo=open(imagens['Sala'][0], 'rb'))
        bot.send_photo(mensagem.chat.id, photo=open(imagens['Sala'][1], 'rb'))
    elif mensagem.text == '/Suite':
        bot.send_photo(mensagem.chat.id, photo=open(imagens['Suite'][0], 'rb'))
        bot.send_photo(mensagem.chat.id, photo=open(imagens['Suite'][1], 'rb'))
    elif mensagem.text == '/Quarto':
        bot.send_photo(mensagem.chat.id, photo=open(imagens['Quarto'][0], 'rb'))
        bot.send_photo(mensagem.chat.id, photo=open(imagens['Quarto'][1], 'rb'))
  



@bot.message_handler(func=finalidades)
def responder_finalidades(mensagem):
    return True

@bot.message_handler(commands=["Voltar"])
def menu_principal(mensagem):
    msg = '''/Decoracoes - Ver decorações realizadas dos nossos clientes
/Designer - Falar com nossos designers de interiores
/Loja - Ir para a loja'''
    fileira = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton('/Decoracoes')
    b2 = types.KeyboardButton('/Designer')
    b3 = types.KeyboardButton('/Loja')
    fileira.add(b1, b2, b3)
    bot.reply_to(mensagem, msg, reply_markup=fileira)

@bot.message_handler(commands=['Decoracoes'])
def decoracoes(mensagem):
    msg = '''Por favor, escolha qual finalidade:
    '''
    fileira = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton('/HomeOffice')
    b2 = types.KeyboardButton('/Sala')
    b3 = types.KeyboardButton('/Suite')
    b4 = types.KeyboardButton('/Quarto')
    b5 = types.KeyboardButton('/Voltar')
    fileira.add(b1, b2, b3, b4, b5)
    bot.send_message(mensagem.chat.id, msg, reply_markup=fileira)
    
@bot.message_handler(commands=["Loja"])
def loja(mensagem):
    msg = '''Em desenvolvimento
/Voltar'''
    bot.reply_to(mensagem, msg)

@bot.message_handler(commands=["Designer"])
def designers(mensagem):
    msg = '''Gabriel: https://api.whatsapp.com/send?phone=5511846548844

Priscila: https://api.whatsapp.com/send?phone=5511246548741

Bruno: https://api.whatsapp.com/send?phone=5512246548223

/Voltar'''
    bot.reply_to(mensagem, msg)

@bot.message_handler(commands=["start"])
def apresentacao(mensagem):
    msg = '''Olá, sou o Assistente Virtual do Decor Stadia, prazer! 😁
Por favor, clicar na opção desejada:

/Decoracoes - Ver decorações realizadas para os nossos clientes
/Designer - Falar com nossos designers de interiores
/Loja - Ir para a loja
'''
    fileira = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton('/Decoracoes')
    b2 = types.KeyboardButton('/Designer')
    b3 = types.KeyboardButton('/Loja')
    fileira.add(b1, b2, b3)
    bot.reply_to(mensagem, msg, reply_markup=fileira)

def qualquer_mensagem(mensagem):
    return True

@bot.message_handler()
def responder(mensagem):
    comandos = ['/Decoracoes', '/Designer', '/Loja', '/HomeOffice', '/Sala', '/Suite', '/Quarto', '/Voltar']
    if mensagem.text not in comandos:
        bot.send_message(mensagem.chat.id, "Desculpe, não reconheço este comando")

bot.polling()