# -*- coding: utf-8 -*-
#arquivo princpal da regra de negocio das nossas aplicacao
#ira controlar toda nossas nossa aplicacao por meio das rotas de protocolo http

from flask import render_template, request, url_for, redirect, flash, jsonify
from app import  app, db
from datetime import datetime, timedelta

#Biblioteca para o bot do telegram
import telebot

#from app.models.tables import Pessoas
from app.models.tables import *

#configurações do bot
chave_api = "2031294195:AAFB3OtBVLEtDfAzS7SVgXuxBEnhNPFYwmY"

bot = telebot.TeleBot(chave_api)


#-------------------------- index --------------------------#
#-------------------------- index --------------------------#
#-------------------------- index --------------------------#

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

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

#-------------------------- BOT --------------------------#
#-------------------------- BOT --------------------------#
#-------------------------- BOT --------------------------#

@bot.message_handler(commands=["Voltar"])
def opcao1(mensagem):
    msg = '''/Designer - Falar com nossos designers de interiores
/Loja - Ir para a loja
/FeedBack - Elogios, dúvidas, sugestões e reclamações'''
    bot.send_message(mensagem.chat.id, msg)

@bot.message_handler(commands=['FeedBack'])
def opcao1(mensagem):
    bot.send_message(mensagem.chat.id, 'Por favor, mande seu Feed Back abaixo')
    

@bot.message_handler(commands=["Loja"])
def opcao1(mensagem):
    msg = '''Em desenvolvimento
/Voltar'''
    bot.reply_to(mensagem, msg)

@bot.message_handler(commands=["Designer"])
def opcao1(mensagem):
    msg = '''Gabriel: https://api.whatsapp.com/send?phone=5511846548844

Priscila: https://api.whatsapp.com/send?phone=5511246548741

/Voltar'''
    bot.reply_to(mensagem, msg)

def mensagem_aberta(mensagem):
        return True

@bot.message_handler(func=mensagem_aberta)
def responder(mensagem):
    apresentacao = '''Olá, sou o Assistente Virtual do Decor Stadia, prazer! 😁
Por favor, clicar na opção desejada:

/Designer - Falar com nossos designers de interiores
/Loja - Ir para a loja
/FeedBack - Elogios, dúvidas, sugestões e reclamações'''
    bot.reply_to(mensagem, apresentacao)

bot.polling()