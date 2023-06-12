# Forms do projeto

# Estrutura de criação de formulário do flask
from flask_wtf import FlaskForm
# Importando os tipos de campo
from wtforms import StringField, SubmitField, PasswordField, DateField, TextAreaField, FloatField, SelectField, BooleanField
# Validadores -> Validador de preenchimento, email, igual a, tamanho
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
# Importando Cliente e Profissional do models para fazer a validação
from divtechne.models import Cliente, Profissional
# Arquivo de foto e qual extensoes esse arquivo pode ter
from flask_wtf.file import FileField, FileAllowed


class FormLogin(FlaskForm):
    # Campo de email -> validador de email e é obrigatorio preencher
    email = StringField("Digite seu Email", validators=[Email(), DataRequired()])
    # Campo de senha -> Obrigátorio de preencher
    senha = PasswordField("Digite a senha", validators=[DataRequired()])
    # Checkbox para lembrar dados de acesso
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    # Botao para logar
    botao = SubmitField("Login")


class FormCriarContaCliente(FlaskForm):
    # Campo de email -> validador de email e é obrigatorio preencher
    email = StringField("Digite o Email", validators=[DataRequired(), Email()])
    # Campo de nome -> obrigatorio preencher
    nome = StringField("Seu nome", validators=[DataRequired()])
    # Campo de senha -> Obrigatorio de preencher e o tamanho tem que ser entre 6 e 20
    senha = PasswordField("Digite a senha", validators=[DataRequired(), Length(6, 20)])
    # Campo de confirmação de senha -> Obrigatorio de preencher e tem que ser igual ao campo de senha
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    # Campo de cpf -> Único e onze digitos
    cpf = StringField("Cpf (onze digitos)", validators=[DataRequired(), Length(11)])
    data_nascimento = DateField("Data de nascimento", validators=[DataRequired()])
    # Botao para criar conta
    botao_submit_cliente = SubmitField("Criar Conta")

    # Função validate para validar se o email já é existente na tentativa de cadastro
    def validate_email(self, email):
        # Filtrando se existe um email igual
        email = Cliente.query.filter_by(email=email.data).first() # .data seria o campo do email
        # Se existir um email igual no banco
        if email:
            # Exiba uma mensagem de erro
            raise ValidationError("Email já cadastrado, faça login para entrar no site")

    # Função validate para validar se o email já é existente na tentativa de cadastro
    def validate_nome(self, nome):
        # Filtrando se existe um nome igual
        nome = Cliente.query.filter_by(nome=nome.data).first()  # .data seria o campo do email
        # Se existir um nome igual no banco
        if nome:
            # Exiba uma mensagem de erro
            raise ValidationError("Nome já cadastrado, tente outro")

    # Função validate para validar se o cpf já é existente na tentativa de cadastro
    def validate_cpf(self, cpf):
        # Filtrando se existe um nome igual
        cpf = Cliente.query.filter_by(cpf=cpf.data).first()  # .data seria o campo do email
        # Se existir um nome igual no banco
        if cpf:
            # Exiba uma mensagem de erro
            raise ValidationError("Cpf já cadastrado!")


class FormEditarPerfilCliente(FlaskForm):
    facebook = StringField("Facebook", validators=[DataRequired()])
    instagram = StringField("Instagram", validators=[DataRequired()])
    linkedin = StringField("Linkedin", validators=[DataRequired()])
    telefone = StringField("Telefone", validators=[DataRequired()])
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])
    nacionalidade = StringField("Nacionalidade", validators=[DataRequired()])
    botao_submit_editar = SubmitField("Editar Perfil")


class FormEditarPerfilProfissional(FlaskForm):
    escolaridade = StringField("Escolaridade", validators=[DataRequired()])
    descricao = TextAreaField("Descrição", validators=[DataRequired()])
    github = StringField("Github", validators=[DataRequired()])
    telefone = StringField("Telefone", validators=[DataRequired()])
    foto = FileField('Foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg']), DataRequired()])
    nacionalidade = StringField("Nacionalidade", validators=[DataRequired()])
    botao_submit_editar = SubmitField("Editar Perfil")


class FormCriarVaga(FlaskForm):
    nome_vaga = StringField("Nome da Vaga", validators=[DataRequired()])
    foto_vaga = FileField("Foto", validators=[DataRequired()])
    empresa_vaga = StringField("Nome da Empresa", validators=[DataRequired()])
    endereco_vaga = StringField("Endereço da Empresa", validators=[DataRequired()])
    salario_vaga = FloatField("Salário", validators=[DataRequired()])
    descricao_vaga = TextAreaField("Descrição da Vaga", validators=[DataRequired()])
    descricao_empresa_vaga = TextAreaField("Descrição da Empresa", validators=[DataRequired()])
    beneficios_vaga = StringField("Benefícios da Vaga", validators=[DataRequired()])
    requisitos_vaga = StringField("Requisitos da Vaga", validators=[DataRequired()])
    nivel_vaga = StringField("Nível da Vaga", validators=[DataRequired()])
    idioma_vaga = StringField("Idioma Necessário")
    botao_vaga = SubmitField("Enviar")


class FormCriarServico(FlaskForm):
    nome_servico = StringField("Nome do Serviço", validators=[DataRequired()])
    empregador_servico = StringField("Nome do Empregador", validators=[DataRequired()])
    salario_servico = FloatField("Salário", validators=[DataRequired()])
    descricao_servico = TextAreaField("Descrição do Serviço", validators=[DataRequired()])
    requisitos_servico = StringField("Requisitos do Serviço", validators=[DataRequired()])
    botao_servico = SubmitField("Enviar")



class FormCriarProjeto(FlaskForm):
    nome_projeto = StringField("Nome do Projeto", validators=[DataRequired()])
    empregador_projeto = StringField("Empregador do Projeto", validators=[DataRequired()])
    tecnologia_projeto = StringField("Tecnologia a ser usada", validators=[DataRequired()])
    descricao_projeto = TextAreaField("Descrição do Projeto", validators=[DataRequired()])
    botao_projeto = SubmitField("Enviar")


class FormCriarContaProfissional(FlaskForm):
    email = StringField("Digite o Email", validators=[DataRequired(), Email()])
    nome = StringField("Seu nome", validators=[DataRequired()])
    telefone = StringField("Telefone", validators=[DataRequired()])
    tecnologia = SelectField("Tecnologias", validators=[DataRequired()], choices=["PYTHON", "PHP", "JAVASCRIPT", "C#", "C++", "TYPESCRIPT", "RUBY", "C", "SWIFT", "R", "OBJECTIVE-C", "SCALA", "SHELL", "GO", "POWERSHELL", "KOTLIN", "RUST", "DART"])
    senha = PasswordField("Digite a senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    nacionalidade = StringField("Nacionalidade", validators=[DataRequired()])
    cpf = StringField("Cpf (onze digitos)", validators=[DataRequired(), Length(11)])
    data_nascimento = DateField("Data de nascimento", validators=[DataRequired()])
    foto = FileField("Foto", validators=[DataRequired()])
    idioma = StringField("Idioma", validators=[DataRequired()])
    escolaridade = StringField("Escolaridade", validators=[DataRequired()])
    descricao = TextAreaField("Sua Descrição", validators=[DataRequired()])
    github = StringField("Github", validators=[DataRequired()])
    botao_dev = SubmitField("Criar Conta")

    def validate_email(self, email):
        email = Profissional.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(f"Email já cadastrado, faça login para entrar no site")

    def validate_user(self, nome):
        nome = Profissional.query.filter_by(nome=nome.data).first()
        if nome:
            raise ValidationError("Nome já cadastrado, tente outro")

    def validate_cpf(self, cpf):
        cpf = Profissional.query.filter_by(cpf=cpf.data).first()
        if cpf:
            raise ValidationError("Cpf já cadastrado!")


class FormEditarSenha(FlaskForm):
    senha_atual = PasswordField("Digite a senha atual", validators=[DataRequired(), Length(6, 20)])
    senha_nova = PasswordField("Digite a nova senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha_nova = PasswordField("Confirmação de Senha nova", validators=[DataRequired(), EqualTo("senha_nova")])
    botao_editar_senha = SubmitField("Editar Senha")


class FormEditarSenhaProfissional(FlaskForm):
    senha_atual = PasswordField("Digite a senha atual", validators=[DataRequired(), Length(6, 20)])
    senha_nova = PasswordField("Digite a nova senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha_nova = PasswordField("Confirmação de Senha nova", validators=[DataRequired(), EqualTo("senha_nova")])
    botao_editar_senha_profissional = SubmitField("Editar Senha")


class FormChat(FlaskForm):
    mensagem = StringField("Digite a mensagem", validators=[DataRequired()])
    anexos = FileField('Anexo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg', 'txt', 'zip', 'rar'])])
    botao_enviar_mensagem = SubmitField("Enviar Mensagem")


class FormEsqueciSenha(FlaskForm):
    email = StringField("Digite o seu Email", validators=[DataRequired(), Email()])
    senha_nova = PasswordField("Digite a senha nova", validators=[DataRequired()])
    confirmacao_senha_nova = PasswordField("Confirmação de Senha nova", validators=[DataRequired(), EqualTo("senha_nova")])
    token = StringField("Token de redefinição de senha", validators=[DataRequired()])
    botao_esqueci_senha = SubmitField("Redefinir minha Senha")


class FormSolicitarToken(FlaskForm):
    email_token = StringField("Digite o seu Email", validators=[DataRequired(), Email()])
    botao_solicitar_token = SubmitField("Solicitar Token")


class FormEditarProjeto(FlaskForm):
    nome_projeto = StringField("Nome do Projeto", validators=[DataRequired()])
    empregador_projeto = StringField("Empregador do Projeto", validators=[DataRequired()])
    tecnologia_projeto = StringField("Tecnologia a ser usada", validators=[DataRequired()])
    descricao_projeto = TextAreaField("Descrição do Projeto", validators=[DataRequired()])
    botao_editar_projeto = SubmitField("Editar Projeto")


class FormEditarServico(FlaskForm):
    nome_servico = StringField("Nome do Serviço", validators=[DataRequired()])
    empregador_servico = StringField("Nome do Empregador", validators=[DataRequired()])
    salario_servico = FloatField("Salário", validators=[DataRequired()])
    descricao_servico = TextAreaField("Descrição do Serviço", validators=[DataRequired()])
    requisitos_servico = StringField("Requisitos do Serviço", validators=[DataRequired()])
    botao_editar_servico = SubmitField("Editar Serviço")


class FormEditarVaga(FlaskForm):
    nome_vaga = StringField("Nome da Vaga", validators=[DataRequired()])
    foto_vaga = FileField("Foto", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg']), DataRequired()])
    empresa_vaga = StringField("Nome da Empresa", validators=[DataRequired()])
    endereco_vaga = StringField("Endereço da Empresa", validators=[DataRequired()])
    salario_vaga = FloatField("Salário", validators=[DataRequired()])
    descricao_vaga = TextAreaField("Descrição da Vaga", validators=[DataRequired()])
    descricao_empresa_vaga = TextAreaField("Descrição da Empresa", validators=[DataRequired()])
    beneficios_vaga = StringField("Benefícios da Vaga", validators=[DataRequired()])
    requisitos_vaga = StringField("Requisitos da Vaga", validators=[DataRequired()])
    nivel_vaga = StringField("Nível da Vaga", validators=[DataRequired()])
    idioma_vaga = StringField("Idioma Necessário")
    botao_editar_vaga = SubmitField("Editar Vaga")