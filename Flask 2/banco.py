# Importando a database e o app e tambem os models
from divtechne import database, app
from divtechne.models import Cliente, Vaga, Servico, Projeto, Seguir, Chat, Contato

# Criando o banco por meio de um contexto
with app.app_context():
    database.create_all()


# with app.app_context():
#     profissional = Seguir.query.filter_by(id_programador_seguir=1).first()
#     print(profissional.profissional.nome)