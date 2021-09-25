# run eh nsso arqivo de arranque do servidor

from app import manager
# ---- para o heroku
from app import  app
import os
# ------

manager.run()

if __name__ == '__main__':
    # ---- para o heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, host='0.0.0.0', port=port) #threaded - muitas sessoes ao mesmo tempo
    # ----- 

#para criar a estrutura esse manager precisa vir antes do __name__
#ja para rodar no heroku precisa colocar dps do __name__


    