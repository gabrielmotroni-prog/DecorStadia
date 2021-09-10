# -*- coding: utf-8 -*-
from datetime import datetime
#aqui vamos contruido em python a estrutora da nossa tabela de banco que 
# sera convertido para sql por meio do sqlalquemy que vai ser hospedado dentro do sql lite
from app import db # essa variavel db esta vindo de __init__
                   #esse objeto db vai intermediar a comunucao entre flask e banco de dados sqlite
from datetime import datetime


class CategoriaProduto(db.Model):
    __tablename__= 'CategoriaProduto'
    codigo_categoria_produto = db.Column(db.Integer, primary_key=True)
    descricao_categoria_produto = db.Column(db.String(100), nullable=False)
    produto = db.relationship('Produto', backref='CategoriaItem', lazy=True, uselist=False)
   
    # construtor
    def __init__(self, descricao_categoria_produto):

        self.descricao_categoria_produto = descricao_categoria_produto


class Produto(db.Model):
    #Os produtos são cadastrados contendo tamanho, cor, material, preço, ambiente sugerido.
    __tablename__= 'Produto'
    codigo_produto = db.Column(db.Integer, primary_key=True)
    descricao_produto = db.Column(db.String(100), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False )
    cor = db.Column(db.String(60), nullable=False)
    material = db.Column(db.String(60), nullable=False)
    tamanho = db.Column(db.Float, nullable=False) # guardar no banco em cm / ou criar um tipo_tamanho
    #Ambiente_sugerido : havera uma tabela com essa relacao
    valor_unitario_produto = db.Column(db.Float, nullable=False)
    codigo_categoria_produto= db.Column(db.Integer, db.ForeignKey('CategoriaProduto.codigo_categoria_produto'))


    # construtor
    def __init__(self, descricao_produto, valor_unitario_produto, codigo_categoria_produto):

        self.descricao_produto = descricao_produto
        self.valor_unitario_produto = valor_unitario_produto
        self.codigo_categoria_produto = codigo_categoria_produto


class Cliente(db.Model):
    __tablename__= 'Cliente'
    codigo_cliente = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(200), nullable=False)
    cep_cliente = db.Column(db.String(9), nullable=False)
    rua_cliente = db.Column(db.String(200), nullable=False)
    bairro_cliente = db.Column(db.String(100), nullable=False)
    data_nascimento_cliente = db.Column(db.String(10), nullable=False)
    CPF_cliente = db.Column(db.String(11), nullable=False)
    email_cliente = db.Column(db.String(200), nullable=False) 
    telefone_celular = db.Column(db.String(23), nullable=False) 
    
    # construtor : passa o objeto via self para ser usado no save
    def __init__(self, nome_cliente, cep_cliente, rua_cliente, bairro_cliente, data_nascimento_cliente,  CPF_cliente, email_cliente, telefone_celular):

        self.nome_cliente = nome_cliente
        self.cep_cliente = cep_cliente
        self.rua_cliente = rua_cliente
        self.bairro_cliente = bairro_cliente
        self.data_nascimento_cliente = data_nascimento_cliente
        self.CPF_cliente = CPF_cliente
        self.email_cliente = email_cliente
        self.telefone_celular = telefone_celular

    @classmethod
    def find_cliente(cls, codigo_cliente):
        cliente = cls.query.filter_by(codigo_cliente=codigo_cliente).first()
        if cliente: # equivalente a: se existe cliente   
            return cliente
        return None
        #para utilizar o metodo filter_by demandouo @classmethod - metodo da clase

    @classmethod
    def list_cliente(cls):
        clientes = cls.query.all()
        return clientes

    def save_cliente(self): # ele eh auto inteligente, ja pega o objeto pelo self
        db.session.add(self)
        db.session.commit()

    def update_cliente(self,nome_cliente,email_cliente,telefone_celular,CPF_cliente,cep_cliente,rua_cliente,bairro_cliente,data_nascimento_cliente):
        self.nome_cliente = nome_cliente
        self.email_cliente = email_cliente
        self.telefone_celular = telefone_celular
        self.CPF_cliente = CPF_cliente
        self.cep_cliente = cep_cliente
        self.rua_cliente = rua_cliente
        self.bairro_cliente = bairro_cliente
        self.data_nascimento_cliente = data_nascimento_cliente


class Ambiente (db.Model):
    __tablename__ = 'Ambiente'
    codigo_ambiente = db.Column(db.Integer, primary_key=True);
    nome_ambiente = db.Column(db.String(200), nullable=False);
    descricao = db.Column(db.String(300), nullable=False);

    #construtor
    def __init__(self, nome_ambiente, descricao_ambiente ):
        self.nome_ambiente = nome_ambiente
        self.descricao_ambiente = descricao_ambiente

    @classmethod
    def find_ambiente(cls, codigo_ambiente):
        ambiente = cls.query.filter_by(codigo_ambiente=codigo_ambiente).first()
        if codigo_ambiente:
            return ambiente
        return None

    def save_ambiente(self): 
        db.session.add(self)
        db.session.commit()


class TipoDecoracao (db.Model):
    __tablename__ = "TipoDecoracao"
    codigo_tipo_decoracao = db.Column(db.Integer, primary_key=True);
    nome_tipo_decoracao = db.Column(db.String(200), nullable=False);
    descricao_tipo_decoracao = db.Column(db.String(300), nullable=False);

    #construtor
    def __init__(self, nome_tipo_decoracao, descricao_tipo_decoracao ):
        self.nome_tipo_decoracao = nome_tipo_decoracao
        self.descricao_tipo_decoracao = descricao_tipo_decoracao

    @classmethod
    def find_tipo_decoracao(cls, codigo_tipo_decoracao):
        tipo_decoracao = cls.query.filter_by(codigo_tipo_decoracao=codigo_tipo_decoracao).first()
        if tipo_decoracao:
            return tipo_decoracao
        return None

    def save_tipo_decoracao(self): 
        db.session.add(self)
        db.session.commit()


class FormaPagamento (db.Model):
    __tablename__ = "FormaPagamento"
    codigo_forma_pagamento = db.Column(db.Integer, primary_key=True);
    nome_forma_pagamento = db.Column(db.String(200), nullable=False);
    descricao_forma_pagamento = db.Column(db.String(300), nullable=False);

    #construtor
    def __init__(self, nome_forma_pagamento, descricao_forma_pagamento ):
        self.nome_forma_pagamento = nome_forma_pagamento
        self.descricao_forma_pagamento = descricao_forma_pagamento

    @classmethod
    def find_forma_pagamento(cls, codigo_forma_pagamento):
        forma_pagamento = cls.query.filter_by(codigo_forma_pagamento=codigo_forma_pagamento).first()
        if forma_pagamento:
            return forma_pagamento
        return None

    def save_forma_pagamento(self): 
        db.session.add(self)
        db.session.commit()

class Profissional (db.Model):
    '''Os serviços oferecidos são profissionais de arquitetura e design de interiores com nome do 
    profissional, foto, telefone e email para contato, comentários e reputação(estrelas).'''

    __tablename__ = "Profissional"
    codigo_profissional = db.Column(db.Integer, primary_key=True);
    nome_completo_profissional = db.Column(db.String(200), nullable=False);
    url_foto_profissional = db.Column(db.String(300));
    telefone_celular_profissional = db.Column(db.String(23), nullable=False);
    email_profissional= db.Column(db.String(200), nullable=False);
    reputacao_profissional  = db.Column(db.Float);
    codigo_tipo_profissinal = db.Column(db.Integer,  db.ForeignKey('TipoProfissional.codigo_tipo_profissional'))
    #comentarios : havera outra tabela com essa relacao

    #construtor
    def __init__(self, nome_completo_profissional, url_foto_profissional, telefone_celular_profissional, email_profissional,reputacao_profissional , codigo_tipo_profissinal):
        self.nome_completo_profissional = nome_completo_profissional
        self.url_foto_profissional = url_foto_profissional
        self.telefone_celular_profissional = telefone_celular_profissional
        self.email_profissional = email_profissional
        self.reputacao_profissional = reputacao_profissional  
        self.codigo_tipo_profissinal = codigo_tipo_profissinal


    @classmethod
    def find_profissional(cls, codigo_profissional):
        profissional = cls.query.filter_by(codigo_profissional=codigo_profissional).first()
        if profissional:
            return profissional
        return None

    def save_profissional(self): 
        db.session.add(self)
        db.session.commit()


class TipoProfissional (db.Model):
    __tablename__ = "TipoProfissional"
    codigo_tipo_profissional = db.Column(db.Integer, primary_key=True);
    nome_tipo_profissional = db.Column(db.String(200), nullable=False);
    descricao_tipo_profissional = db.Column(db.String(300), nullable=False);
    profissional = db.relationship('Profissional', backref='TipoProfissional', lazy=True, uselist=True) #TRUE ATENCAO

    #construtor
    def __init__(self, nome_tipo_profissional, descricao_tipo_profissional ):
        self.nome_tipo_profissional = nome_tipo_profissional
        self.descricao_tipo_profissional = descricao_tipo_profissional

    @classmethod
    def find_tipo_profissional(cls, codigo_tipo_profissional):
        tipo_profissional = cls.query.filter_by(codigo_tipo_profissional=codigo_tipo_profissional).first()
        if tipo_profissional:
            return tipo_profissional
        return None

    def save_tipo_profissional(self): 
        db.session.add(self)
        db.session.commit()

class Pedido (db.Model):
    __tablename__ = "Pedido"
    codigo_pedido = db.Column(db.Integer, primary_key=True);
    data_abertura_pedido = db.Column(db.DateTime, nullable=False);
    data_fechamento = db.Column(db.DateTime);
    situacao_pedido = db.Column(db.Integer,nullable=False);
    codigo_forma_pagamento = db.Column(db.ForeignKey('FormaPagamento.codigo_forma_pagamento'))

    #construtor
    def __init__(self, data_abertura_pedido, data_fechamento,situacao_pedido,codigo_forma_pagamento ):
        self.data_abertura_pedido = data_abertura_pedido
        self.data_fechamento = data_fechamento
        self.situacao_pedido = situacao_pedido
        self.codigo_forma_pagamento=codigo_forma_pagamento


    @classmethod
    def find_pedido(cls, codigo_pedido):
        pedido = cls.query.filter_by(codigo_pedido=codigo_pedido).first()
        if codigo_pedido:
            return pedido
        return None

    def save_pedido(self): 
        db.session.add(self)
        db.session.commit()

class ItemPedido (db.Model):
    __tablename__ = "ItemPedido"
    codigo_item_pedido = db.Column(db.Integer, primary_key=True);
    codigo_pedido = db.Column(db.Integer, nullable=False);
    qtd_item = db.Column(db.Integer,nullable=False);

    #construtor
    def __init__(self, codigo_pedido,qtd_item ):
        self.codigo_pedido = codigo_pedido
        self.qtd_item = qtd_item
    

    @classmethod
    def find_item_pedido(cls, codigo_pedido):
        pedido = cls.query.filter_by(codigo_pedido=codigo_pedido).first()
        if codigo_pedido:
            return pedido
        return None

    def save_item_pedido(self): 
        db.session.add(self)
        db.session.commit()


class Servico (db.Model):
    __tablename__ = "Servico"
    codigo_servico = db.Column(db.Integer, primary_key=True);
    codigo_profissinal = db.Column(db.Integer,  db.ForeignKey('Profissional.codigo_profissional'))
    codigo_cliente = db.Column(db.Integer,  db.ForeignKey('Profissional.codigo_profissional'))
    codigo_pedido = db.Column(db.Integer); # n obrigatorio
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow);
    data_fechamento = db.Column(db.DateTime, default=datetime.utcnow);
    status_servico = db.Column(db.Integer, nullable=False)

    #construtor
    def __init__(self, codigo_servico, codigo_profissinal,codigo_cliente,codigo_pedido, data_abertura,status_servico ):
        self.codigo_servico = codigo_servico
        self.codigo_profissinal = codigo_profissinal
        self.codigo_cliente = codigo_cliente
        self.codigo_pedido = codigo_pedido
        self.data_abertura = data_abertura
        self.status_servico = status_servico
    

    @classmethod
    def find_servico(cls, codigo_servico):
        servico = cls.query.filter_by(codigo_servico=codigo_servico).first()
        if codigo_servico:
            return codigo_servico
        return None

    def save_codigo_servico(self): 
        db.session.add(self)
        db.session.commit()


'''
status servico
'''