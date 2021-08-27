import os.path #maniupulacoa de comandos do sistema operaciional. patch eh utilziado para controle de diretorios 
basedir = os.path.abspath(os.path.dirname(__file__))  #iremos armazenaro endereco string do nosso diretorio base. eh uma variavel.  __file__ variavel que armazena o diretorio  atual do python
                                                      # os.path.abspath  captura o diretorio absoluto e naosomente o atuaal endereco
DEBUG = True # outra variavel que coloca nosso projeto em nodo de debug para acompanhamos  os erros durante o desenolvimento              
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db') #variavel responsavel de armazar o endereco de criacao do nosso arquivo de dados do sqlite. o join junta o arquivo de banco que criamos com local
                                                                          #inserimos o endereco 'sqlite' porque estamos sqlite        
SQLALQUEMY_TRACK_MODIFICATIONS = True # ira nos possibiliar realizar modificacoes no banco de dados sem qualquer restricao durante as execucoes                                                      