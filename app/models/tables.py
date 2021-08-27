#aqui vamos contruido em python a estrutora da nossa tabela de banco que 
# sera convertido para sql por meio do sqlalquemy que vai ser hospedado dentro do sql lite
from app import db # essa variavel db esta vindo de __init__
                   #esse objeto db vai intermediar a comunucao entre flask e banco de dados sqlite
from datetime import datetime

class CategoriaItem(db.Model):
    __tablename__= 'CategoriaItem'
    codigo_categoria_item = db.Column(db.Integer, primary_key=True)
    descricao_categoria_item = db.Column(db.String(100), nullable=False)
    item = db.relationship('Item', backref='CategoriaItem', lazy=True, uselist=False)
   
    # construtor
    def __init__(self, descricao_categoria_item):

        self.descricao_categoria_item = descricao_categoria_item


class Item(db.Model):
    __tablename__= 'Item'
    codigo_item = db.Column(db.Integer, primary_key=True)
    descricao_item = db.Column(db.String(100), nullable=False)
    valor_unitario_item = db.Column(db.Float, nullable=False)
    codigo_categoria_item= db.Column(db.Integer, db.ForeignKey('CategoriaItem.codigo_categoria_item'))

    # construtor
    def __init__(self, descricao_item, valor_unitario_item, codigo_categoria_item):

        self.descricao_item = descricao_item
        self.valor_unitario_item = valor_unitario_item
        self.codigo_categoria_item = codigo_categoria_item


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
    
    # construtor
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

    def save_cliente(self): # ele eh auto inteligente, ja pega o objeto pelo self
        db.session.add(self)
        db.session.commit()
    