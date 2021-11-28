# -*- coding: utf-8 -*-



#arquivo princpal da regra de negocio das nossas aplicacao
#ira controlar toda nossas nossa aplicacao por meio das rotas de protocolo http

from operator import eq
from re import A
import re
from flask import render_template, request, url_for, redirect, flash, jsonify,session, abort, redirect
from requests.models import HTTPBasicAuth
from werkzeug.wrappers import AuthorizationMixin
from app import  app, db
from telebot import types
import os
import requests
import json

# mercado livre
import meli
#boleto
from gerencianet import Gerencianet

#Biblioteca para o bot do telegram
import telebot
import urllib

#configurações do bot
chave_api = "2031294195"
bot = telebot.TeleBot(chave_api)

#from app.models.tables import Pessoas
from app.models.tables import *

#-------------------------- login --------------------------#
#-------------------------- login --------------------------#
#-------------------------- login --------------------------#

#-------------variavel de ambiente
from dotenv import load_dotenv
load_dotenv()  # obtém variáveis ​​de ambiente de .env.
MY_ENV_VAR = os.getenv('MY_ENV_VAR')
env_client_id = os.getenv('env_client_id')
env_client_secret = os.getenv('env_client_secret')
env_client_secret_key_mercadolivre = os.getenv('env_client_secret_key_mercadolivre')
env_google_client_id = os.getenv ('env_google_client_id')
print(MY_ENV_VAR)
#--------------- 

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

GOOGLE_CLIENT_ID = env_google_client_id
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


#-------------------------- produtos --------------------------#
#-------------------------- produtos --------------------------#
#-------------------------- produtos --------------------------#

@app.route('/produtos/<seller_id>')
def produtos(seller_id):
    produtos = Produto.list_produtos()
                                                                    #ex:143916881
    url = 'https://api.mercadolibre.com/sites/MLB/search?seller_id='+seller_id
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {env_client_secret_key_mercadolivre}'}

    return_request = requests.get(url, headers=headers).json()
    #print(r)
    produtos_m = return_request['results']
    #print(produtos_m)

    return render_template('produtos.html', produtos=produtos, produtos_m=produtos_m)

@app.route('/produto/carrinho/<int:codigo_produto>')
def produto_carrinho(codigo_produto=0):
    produto = Produto.find_produto(codigo_produto)

    return render_template('carrinho.html', produto=produto)

@app.route('/produto/carrinho/confirmar',methods=['POST'])
def produto_carrinho_confirmar():

    codigo_produto = int(request.form['codigo_produto'])
    descricao_produto = request.form['descricao_produto']
    quantidade_produto = int(request.form['quantidade_produto'])
    cor_produto = request.form['cor_produto']
    material_produto = request.form['material_produto']
    tamanho_produto = float(request.form['tamanho_produto'])
    valor_unitario_produto = int(request.form['valor_unitario_produto']) # x100 
    cep = request.form['cep']
    endereco = request.form['endereco']
    bairro = request.form['bairro']
    email = request.form['email']

    #utilizand variavel de ambiente contidas em .env
    credentials = {
    'client_id': env_client_id,
    'client_secret': env_client_secret,
    'sandbox': True
    }

    #instancia objeto
    gn = Gerencianet(credentials)

    #corpo da requisicao de transacao
    body_item = {
        'items': [{
            'name': descricao_produto,
            'value': valor_unitario_produto,
            'amount': quantidade_produto
        }],
        'shippings': [{
            'name': endereco,
            'value': 100
        }]
    }
    
    #cria cobranca
    return_create_charge = gn.create_charge(body=body_item)
    print(return_create_charge)


    #monta parametros para serem usados para montar forma de pagamento
    params = {
        'id': return_create_charge['data']['charge_id']
    }

    #monta corpo forma de pagamento
    body_metodo_pagamento = {
        'payment': {
            'banking_billet': {
                'expire_at': '2021-11-25',
                'customer': {
                    'name': "Cliente DecorStadia",
                    'email': email,
                    'cpf': "94271564656",
                    'birth': "2021-11-25",
                    'phone_number': "5144916523"
                }
            }
        }
    }
   
    # vincula a cobranca ao metodo de pagamento
    return_pay_change = gn.pay_charge(params=params, body=body_metodo_pagamento)
    print(return_pay_change)

    #monta paramentos consulta transacao/ passar parametro para proxima pagina para visualizar boleto
    params = {
        'id': return_create_charge['data']['charge_id']
    }

    #captura returno do boleto
    return_detail_charge =  gn.detail_charge(params=params)

    #captura link de acesso ao boleto
    print(return_detail_charge['data']['payment']['banking_billet']['link'])
    link_boleto_gerado = return_detail_charge['data']['payment']['banking_billet']['link']

    #direciona ao link do boleto
    return redirect(link_boleto_gerado)

    
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
    session["picture"] = id_info.get("picture")
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(session)
    return redirect(url_for("protected_area")) #direcionar para tela principal, porem com a rota protected_area . Ela ira utiliza o objeto session


@app.route("/logout")
def logout():
    session.clear() # limpa objeto
    #return redirect("index")
    return redirect(url_for("login") ) #direcionar para tela de login 


@app.route("/")
def index():
    

    # boleto cloud 

    #autenticacao

    #response = requests.get("https://sandbox.boletocloud.com/api/v1/boletos/1", auth=HTTPBasicAuth('api-key_-HjldUNq88GTvINdZlsOlTzUuvzltLHTPX0ptiKwJxY=','token') )
    #print(response.json())
    
    #get boleto
    #response = requests.get("https://sandbox.boletocloud.com/api/v1/boletos/cXaB4_0zXfl1I9URR8o7j-KZZwQa1dA26i06hIp7qpk=", auth=HTTPBasicAuth('api-key_-HjldUNq88GTvINdZlsOlTzUuvzltLHTPX0ptiKwJxY=','token') )
    #if response.status_code == 200:
        #print("The request was a success!")
     #   pass
        #print(response)

        

    #return "Hello World <a href='/login'><button>Login</button></a>"
    return render_template("index.html")

@app.route("/protected_area") #
#@login_is_required
def protected_area():

    #return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    #return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    return render_template("index.html", usuario_nome_completo=session['name'], foto_usuario=session['picture'])

#-------------------------- BOT --------------------------#
#-------------------------- BOT --------------------------#
#-------------------------- BOT --------------------------#

'''def get_url():
    contents = requests.get('https://thatcopy.pw/catapi/rest/').json()
    image_url = contents['url']
    return image_url'''

#Opção de fotos das decorações
def finalidades(mensagem):
    imagens = {'HomeOffice': ['https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg', 'https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg'],
                'Sala': ['https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg', 'https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg'],
                'Suite': ['https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg', 'https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg'],
                'Quarto': ['https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg', 'https://thatcopy.github.io/catAPI/imgs/jpg/96aff96.jpg']
                }
    if mensagem.text == '/HomeOffice':
        #bot.send_photo(mensagem.chat.id, imagens['HomeOffice'][0])
        bot.send_photo(mensagem.chat.id, imagens['HomeOffice'][0])
        bot.send_photo(mensagem.chat.id, imagens['HomeOffice'][1])

    elif mensagem.text == '/Sala':
        bot.send_photo(mensagem.chat.id, imagens['Sala'][0])
        bot.send_photo(mensagem.chat.id, imagens['Sala'][1])
    elif mensagem.text == '/Suite':
        bot.send_photo(mensagem.chat.id, imagens['Suite'][0])
        bot.send_photo(mensagem.chat.id, imagens['Suite'][1])
    elif mensagem.text == '/Quarto':
        bot.send_photo(mensagem.chat.id, imagens['Quarto'][0])
        bot.send_photo(mensagem.chat.id, imagens['Quarto'][1])
  



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
=======
# -*- coding: utf-8 -*-
#arquivo princpal da regra de negocio das nossas aplicacao
#ira controlar toda nossas nossa aplicacao por meio das rotas de protocolo http

from flask import render_template, request, url_for, redirect, flash, jsonify
from app import  app, db
from datetime import datetime, timedelta

#from app.models.tables import Pessoas
from app.models.tables import *



#-------------------------- index --------------------------#
#-------------------------- index --------------------------#
#-------------------------- index --------------------------#

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
@login_required
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


#-------------------------- facebook --------------------------#
#-------------------------- facebook --------------------------#
#-------------------------- facebook --------------------------#

@app.route('/me')
@login_required
def user():
    return render_template('user.html', user=current_user)

@app.route('/login-facebook')
def login():
    if current_user.is_anonymous():
        return facebook.authorize(callback=url_for('facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))
    return redirect(url_for('.user'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))
