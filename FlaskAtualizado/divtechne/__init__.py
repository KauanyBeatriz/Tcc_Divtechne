# Com o __init__ no projeto determinamos que essa pasta é um projeto
from flask import Flask
# Importando o bycript para criptografia -> segurança
from flask_bcrypt import Bcrypt
# Importando o gerenciador de banco de dados
from flask_sqlalchemy import SQLAlchemy
# Importando o gerenciador de Login
from flask_login import LoginManager

# Criando a instacia do site
app = Flask(__name__)

# Banco sqlite que sera criado no projeto
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
# Chave de segurança do app
app.config["SECRET_KEY"] = "f3366d95a8040838a0e645a12e2db329"
# Confirgurando uma pasta que vai receber todos os arquivos de upload
app.config["UPLOAD_FOLDER"] = "static/posts"

# Database
database = SQLAlchemy(app)

# Criptografia
bcrypt = Bcrypt(app)

# Gerenciador de login
login_manager = LoginManager(app)
login_manager.login_view = "homepage" # Rota da página que tera o login

# Caso o usuario tente entrar em uma pagina que necessite que esteja logado ele redireciona para o login caso não esteja
login_manager.login_view = 'homepage' # após isso se fizer login ele é redirecionado a route que ele estava tentando entrar
# Personalizando o alerta da mensagem
login_manager.login_message_category = 'alert-info'
login_manager.login_message = "Faça o login para continuar"

# Sempre importar os outros arquivos depois pois o app tem que ser criado primeiro para depois ser importado os outros arquivos

# importando as rotas
from divtechne import routes