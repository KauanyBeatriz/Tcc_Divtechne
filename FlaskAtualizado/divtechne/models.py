# Models do projeto

# Importando a database, modulo datetime e o login manager
from divtechne import database, login_manager
from datetime import datetime
# Com essa importacao posso dizer para o programa qual classe é a do login no caso usuario
from flask_login import UserMixin

# Funcao que carrega o usuario
@login_manager.user_loader
# Essa função é necessária para o funcionamento do login -> Vai receber o id de um usuario e tem que retornar quem ele é
def load_usuario(id_usuario):
    # Buscando por query na classe usuario fazendo um get no id do usario que é int
    return Cliente.query.get(int(id_usuario))


# Tabela de Cliente
class Cliente(database.Model, UserMixin):
    # Colunas do banco de dados
    id = database.Column(database.Integer, primary_key=True) # Chave primária
    nome = database.Column(database.String, nullable=False, unique=True) # Nome de cliente único
    email = database.Column(database.String, nullable=False, unique=True) # Email tem que ser unico
    senha = database.Column(database.String, nullable=False)
    cpf = database.Column(database.String, unique=True)  # Cpf tem que ser único
    telefone = database.Column(database.String, default="11111111111") # Telefone
    nacionalidade = database.Column(database.String, default="Brasileiro") # Nacionalidade
    foto = database.Column(database.String, default="default.png")
    data_nascimento = database.Column(database.Date, nullable=False) # Data
    linkedin = database.Column(database.String, default="Não informado") # Link linkedin
    facebook = database.Column(database.String, default="Não informado")
    instagram = database.Column(database.String, default="Não informado")
    # Relacionamento
    vagas = database.relationship("Vaga", backref="cliente", lazy=True)
    servicos = database.relationship("Servico", backref="cliente", lazy=True)
    projetos = database.relationship("Projeto", backref="cliente", lazy=True)
    seguir_cliente = database.relationship("Seguir", backref="seguidor", lazy=True)


class Vaga(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    foto = database.Column(database.String, nullable=False)
    nome = database.Column(database.String, nullable=False)
    empresa = database.Column(database.String, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    salario = database.Column(database.Float, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    descricao_empresa = database.Column(database.Text, nullable=False)
    beneficios = database.Column(database.String, nullable=False)
    requisitos = database.Column(database.String, nullable=False)
    nivel = database.Column(database.String, nullable=False)
    idioma = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_cliente_vaga = database.Column(database.Integer, database.ForeignKey("cliente.id"), nullable=False) # Fk


class Servico(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    empregador = database.Column(database.String, nullable=False)
    salario = database.Column(database.Float, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    requisitos = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_cliente_servico = database.Column(database.Integer, database.ForeignKey("cliente.id"), nullable=False) # Fk


class Projeto(database.Model):
    id = database.Column(database.Integer, primary_key=True) # Chave Primária
    nome = database.Column(database.String, nullable=False) # Nome do projeto
    empregador = database.Column(database.String, nullable=False) # Nome do empregador
    descricao = database.Column(database.Text, nullable=False) # Descrição do projeto
    tecnologia = database.Column(database.String, nullable=False) # Tecnologia que vai ser usada
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_cliente_projeto = database.Column(database.Integer, database.ForeignKey("cliente.id"), nullable=False) # Fk


# Tabela de Profissional
class Profissional(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True) # Nome de profissional único
    email = database.Column(database.String, nullable=False, unique=True) # Email profissional tem que ser unico
    senha = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String, nullable=False) # Telefone
    tecnologia = database.Column(database.String, nullable=False) # Tecnologias conhecidas
    nacionalidade = database.Column(database.String, default="Brasileiro") # Nacionalidade
    cpf = database.Column(database.String, unique=True) # Cpf tem que ser único
    data_nascimento = database.Column(database.Date) # Data
    foto = database.Column(database.String, nullable=False)
    idioma = database.Column(database.String) # Idioma
    escolaridade = database.Column(database.String) # Escolaridade
    descricao = database.Column(database.Text) # Descrição
    github = database.Column(database.String) # link github
    seguir_profissional = database.relationship("Seguir", backref="profissional", lazy=True)


class Seguir(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_cliente_seguir = database.Column(database.Integer, database.ForeignKey("cliente.id"), nullable=False)
    id_programador_seguir = database.Column(database.Integer, database.ForeignKey("profissional.id"), nullable=False)