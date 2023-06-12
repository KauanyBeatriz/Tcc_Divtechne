# Rotas do site -> links
# render template para renderizar templates
from flask import render_template, url_for, redirect, flash, request, abort # Url for serve para direcionar as paginas pela função
# Importando o app, banco de dados e criptografia
from divtechne import app, database, bcrypt, mail, Message
# Para exigir que em determinadas rotas o usuario so pode entrar se estiver logado, login do user, logout do user, e o usuario atual
from flask_login import login_required, login_user, logout_user, current_user
# Importando os formularios
from divtechne.forms import FormLogin, FormCriarContaCliente, FormCriarContaProfissional, FormCriarVaga, FormCriarServico, FormCriarProjeto, FormEditarPerfilCliente, FormEditarSenha, FormEditarSenhaProfissional, FormEditarPerfilProfissional, FormEsqueciSenha, FormSolicitarToken, FormChat, FormEditarProjeto, FormEditarServico, FormEditarVaga
# Importando o models Usuario e Foto
from divtechne.models import Cliente, Profissional, Vaga, Servico, Projeto, Seguir, Chat, Contato, CandidatoVaga, CandidatoServico, CandidatoProjeto
# Importando os
import os
# Transforma o nome de arquivos de forma adequada
from werkzeug.utils import secure_filename
import secrets
from PIL import Image

@app.route("/", methods=["GET", "POST"])
# Função da página
def homepage():
    formlogin = FormLogin()
    # Se quando ele clicar para enviar as informações estiverem corretas como passamos para ser
    if formlogin.validate_on_submit() and 'botao' in request.form:
        # Procurando esse usuario no bd
        cliente = Cliente.query.filter_by(email=formlogin.email.data).first()
        profissional = Profissional.query.filter_by(email=formlogin.email.data).first()
        # Se esse usuario existir e Verifica a senha desse usuario do email descriptografada e se é igual ao campo digitado pelo usuario
        if cliente and bcrypt.check_password_hash(cliente.senha, formlogin.senha.data):
            # Faça o login do usuario
            login_user(cliente, remember=formlogin.lembrar_dados.data)
            flash("Login feito com sucesso: {}".format(formlogin.email.data), 'alert-success')
            # Vai pegar o parametro next da url
            parametro = request.args.get('next')
            # Caso tenha esse parametro
            if parametro:
                # Retorna a página que ele estava tentando entrar
                return redirect(parametro)
            # Caso contrario
            else:
                # Redirecionando o usuário para a home
                return redirect(url_for("home_cliente"))

        elif profissional and bcrypt.check_password_hash(profissional.senha, formlogin.senha.data):
            # Faça o login do usuario
            login_user(profissional, remember=formlogin.lembrar_dados.data)
            flash("Login feito com sucesso: {}".format(formlogin.email.data), 'alert-success')
            # Vai pegar o parametro next da url
            parametro = request.args.get('next')
            # Caso tenha esse parametro
            if parametro:
                # Retorna a página que ele estava tentando entrar
                return redirect(parametro)
            # Caso contrario
            else:
                # Redirecionando o usuário para a home
                return redirect(url_for("vagas"))

        else:
            flash("Usuário ou senha incorreta verifique as credenciais", 'alert-danger')

    formcriarconta = FormCriarContaCliente()
    # Se quando ele clicar para enviar as informações estiverem corretas como passamos para ser
    if formcriarconta.validate_on_submit() and 'botao_submit_cliente' in request.form:
        # Se alguem roubar o bd não vai ser possivel ver as senhas mesmo fazendo o caminho contrario no bcrypt por causa que ele usa da nossa secret key
        # Criptografando a senha -> Sequencia de caracteres
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        cpf = bcrypt.generate_password_hash(formcriarconta.cpf.data)
        secret = secrets.token_hex(32)
        chave = bcrypt.generate_password_hash(secret)
        # Caminho inverso para checar a senha
        # bcrypt.check_password_hash()
        # Dentro de uma variavel coloco as informações que serão adicionadas ou seja todos os data do form
        cliente = Cliente(nome=formcriarconta.nome.data, senha=senha,
                          email=formcriarconta.email.data, cpf=cpf,
                          data_nascimento=formcriarconta.data_nascimento.data, token=chave)
        # Adicionando o usuario
        database.session.add(cliente)
        # Commit para perpetuar a session
        database.session.commit()

        # Mandando email
        titulo = "Seja bem vindo a DIVTECHNE {}".format(formcriarconta.nome.data)
        remetente = "emanuelbrit16@gmail.com"
        msg = Message(titulo, sender=remetente, recipients=[formcriarconta.email.data])

        msg.subject = "Seja bem vindo a plataforma"

        msg.body = "Estamos muito felizes de você ter se juntado conosco!!"

        # Enviando email
        mail.send(msg)

        # Aqui colocamos que ele esta logado
        login_user(cliente)  # Aqui ele vai armazenar no cache seu login
        flash(f"Conta para o email {formcriarconta.email.data} criada com sucesso!", "alert-success")
        # Ele vai redirecionar para a função da página perfil e o usuário no link sera dinâmico
        return redirect(url_for("home_cliente"))

    formprofissional = FormCriarContaProfissional()
    if formprofissional.validate_on_submit() and 'botao_dev' in request.form:
        arquivo = formprofissional.foto.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        cpf = bcrypt.generate_password_hash(formcriarconta.cpf.data)
        secret = secrets.token_hex(32)
        chave = bcrypt.generate_password_hash(secret)
        profissional = Profissional(nome=formprofissional.nome.data, senha=senha,
                                    telefone=formprofissional.telefone.data,
                                    cpf=cpf, nacionalidade=formprofissional.nacionalidade.data,
                                    tecnologia=formprofissional.tecnologia.data, email=formprofissional.email.data,
                                    foto=nome_seguro, data_nascimento=formprofissional.data_nascimento.data,
                                    idioma=formprofissional.idioma.data,
                                    escolaridade=formprofissional.escolaridade.data,
                                    descricao=formprofissional.descricao.data, github=formprofissional.github.data,
                                    token=chave)
        database.session.add(profissional)
        database.session.commit()
        login_user(profissional)  # Aqui ele vai armazenar no cache seu login
        return redirect(url_for("vagas"))

    # Retornando o template html
    return render_template("index.html", form=formlogin, form_cliente=formcriarconta, form_profissional=formprofissional)


@app.route("/cliente", methods=["GET", "POST"])
@login_required
def home_cliente():
    formcriarvaga = FormCriarVaga()
    programador = Profissional.query.order_by(Profissional.tecnologia.desc()).all()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data, empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data, descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data, descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    foto = url_for('static', filename='posts/{}'.format(current_user.foto))

    return render_template("cliente/C_home.html", programadores=programador, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha, foto=foto)


@app.route("/profissional/projetos", methods=["GET", "POST"])
@login_required
def projetos():
    projeto = Projeto.query.order_by(Projeto.data_criacao.desc()).all()

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_projetos.html", projetos=projeto, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/profissional/vagas", methods=["GET", "POST"])
@login_required
def vagas():
    vaga = Vaga.query.order_by(Vaga.data_criacao.desc()).all()
    profissional = Profissional.query.filter_by(id=current_user.id).first()

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_home.html", vagas=vaga, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/profissional/servicos", methods=["GET", "POST"])
@login_required
def servicos():
    servico = Servico.query.order_by(Servico.data_criacao.desc()).all()

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_servicos.html", servicos=servico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/cliente/vagas/<id_cliente>", methods=["GET", "POST"])
@login_required
def minhas_vagas(id_cliente):
    cliente = Cliente.query.get(int(id_cliente))

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_minhasVagas.html", cliente=cliente, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/servicos/<id_cliente>", methods=["GET", "POST"])
@login_required
def meus_servicos(id_cliente):
    cliente = Cliente.query.get(int(id_cliente))

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_meusServicos.html", cliente=cliente, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/projetos/<id_cliente>", methods=["GET", "POST"])
@login_required
def meus_projetos(id_cliente):
    cliente = Cliente.query.get(int(id_cliente))

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_meusProjetos.html", cliente=cliente, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


def salvar_imagem(imagem):
    # Adicionar o codigo na imagem
    # Criei um codigo para o final da imagem
    codigo = secrets.token_hex(8)
    # Separei o nome do arquivo e extensão
    nome, extensao = os.path.splitext(imagem.filename)
    # Depois juntei o nome + codigo + extensao
    nome_arquivo = nome + codigo + extensao
    # Caminho da pasta que vamos salvar o arquivo
    caminho_completo = os.path.join(app.root_path, 'static/posts', nome_arquivo)
    # Reduzir tamanho da imagem
    tamanho = (185, 185)
    # Abrindo imagem
    imagem_reduzida = Image.open(imagem)
    # E reduzindo tamanho dela
    imagem_reduzida.thumbnail(tamanho)
    # Salvando a imagem na pasta static/fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # Salvar Imagem
    return nome_arquivo


@app.route("/perfil/cliente/<id_usuario>", methods=["GET", "POST"])
@login_required
def meu_perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        formcriarvaga = FormCriarVaga()

        if formcriarvaga.validate_on_submit():
            arquivo = formcriarvaga.foto_vaga.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"],
                                   nome_seguro)
            arquivo.save(caminho)
            vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                        empresa=formcriarvaga.empresa_vaga.data,
                        endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                        descricao=formcriarvaga.descricao_vaga.data,
                        descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                        beneficios=formcriarvaga.beneficios_vaga.data,
                        requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                        id_cliente_vaga=current_user.id)
            database.session.add(vaga)
            database.session.commit()
            return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
        else:
            pass

        formcriarservico = FormCriarServico()

        if formcriarservico.validate_on_submit():
            servico = Servico(nome=formcriarservico.nome_servico.data,
                              empregador=formcriarservico.empregador_servico.data,
                              salario=formcriarservico.salario_servico.data,
                              descricao=formcriarservico.descricao_servico.data,
                              requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
            database.session.add(servico)
            database.session.commit()
            return redirect(url_for("meus_servicos", id_cliente=current_user.id))
        else:
            pass

        formcriarprojeto = FormCriarProjeto()
        if formcriarprojeto.validate_on_submit():
            projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                              descricao=formcriarprojeto.descricao_projeto.data,
                              tecnologia=formcriarprojeto.tecnologia_projeto.data,
                              empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
            database.session.add(projeto)
            database.session.commit()
            return redirect(url_for("meus_projetos", id_cliente=current_user.id))
        else:
            pass
        return render_template("perfil.html", usuario=current_user, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)

    else:
        formcriarvaga = FormCriarVaga()

        if formcriarvaga.validate_on_submit():
            arquivo = formcriarvaga.foto_vaga.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"],
                                   nome_seguro)
            arquivo.save(caminho)
            vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                        empresa=formcriarvaga.empresa_vaga.data,
                        endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                        descricao=formcriarvaga.descricao_vaga.data,
                        descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                        beneficios=formcriarvaga.beneficios_vaga.data,
                        requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                        id_cliente_vaga=current_user.id)
            database.session.add(vaga)
            database.session.commit()
            return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
        else:
            pass

        formcriarservico = FormCriarServico()

        if formcriarservico.validate_on_submit():
            servico = Servico(nome=formcriarservico.nome_servico.data,
                              empregador=formcriarservico.empregador_servico.data,
                              salario=formcriarservico.salario_servico.data,
                              descricao=formcriarservico.descricao_servico.data,
                              requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
            database.session.add(servico)
            database.session.commit()
            return redirect(url_for("meus_servicos", id_cliente=current_user.id))
        else:
            pass

        formcriarprojeto = FormCriarProjeto()
        if formcriarprojeto.validate_on_submit():
            projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                              descricao=formcriarprojeto.descricao_projeto.data,
                              tecnologia=formcriarprojeto.tecnologia_projeto.data,
                              empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
            database.session.add(projeto)
            database.session.commit()
            return redirect(url_for("meus_projetos", id_cliente=current_user.id))
        else:
            pass
        usuario = Cliente.query.get(int(id_usuario))

        formeditarsenha = FormEditarSenha()
        if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
            if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
                senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
                usuario = Cliente.query.filter_by(email=current_user.email).first()
                usuario.senha = senha_nova
                database.session.commit()
                flash("Senha alterada com sucesso!", "alert-success")
            else:
                flash("Senha atual incorreta!", "alert-danger")

        return render_template("perfil.html", usuario=usuario, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)



@app.route("/meuperfil", methods=["GET", "POST"])
@login_required
def meu_perfil_cliente():
    formeditar = FormEditarPerfilCliente()
    if formeditar.validate_on_submit() and 'botao_submit_editar' in request.form:
        current_user.nacionalidade = formeditar.nacionalidade.data
        current_user.linkedin = formeditar.linkedin.data
        current_user.facebook = formeditar.facebook.data
        current_user.instagram = formeditar.instagram.data
        current_user.telefone = formeditar.telefone.data
        if formeditar.foto.data:
            nome_imagem = salvar_imagem(formeditar.foto.data)
            current_user.foto = nome_imagem
        database.session.commit()
        flash("Perfil alterado com sucesso", "alert-success")
        return redirect(url_for("meu_perfil_cliente"))
    elif request.method == "GET":
        formeditar.telefone.data = current_user.telefone
        formeditar.nacionalidade.data = current_user.nacionalidade
        formeditar.linkedin.data = current_user.linkedin
        formeditar.facebook.data = current_user.facebook
        formeditar.instagram.data = current_user.instagram
    else:
        flash("Erro", "alert-danger")

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_meu_perfil.html", form=formeditar, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/profissional/meuperfil", methods=["GET", "POST"])
@login_required
def meu_perfil_profissional():
    formeditar = FormEditarPerfilProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditar.validate_on_submit() and 'botao_submit_editar' in request.form:
        profissional.nacionalidade = formeditar.nacionalidade.data
        profissional.escolaridade = formeditar.escolaridade.data
        profissional.descricao = formeditar.descricao.data
        profissional.github = formeditar.github.data
        profissional.telefone = formeditar.telefone.data
        if formeditar.foto.data:
            nome_imagem = salvar_imagem(formeditar.foto.data)
            profissional.foto = nome_imagem
        database.session.commit()
        flash("Perfil alterado com sucesso", "alert-success")
        return redirect(url_for("meu_perfil_profissional"))
    elif request.method == "GET":
        formeditar.telefone.data = profissional.telefone
        formeditar.nacionalidade.data = profissional.nacionalidade
        formeditar.escolaridade.data = profissional.escolaridade
        formeditar.descricao.data = profissional.descricao
        formeditar.github.data = profissional.github
    else:
        flash("Erro", "alert-danger")

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_perfil.html", form=formeditar, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/perfil/profissional/<id_profissional>", methods=["GET", "POST"])
@login_required
def perfil_profissional(id_profissional):
    profissional = Profissional.query.get(int(id_profissional))

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data,
                          empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                          descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_ver_perfil_profissional.html", profissional=profissional, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/seguir/<id_profissional>", methods=["GET", "POST"])
@login_required
def seguir_profissional(id_profissional):
    print(current_user.seguir_cliente)
    for profissional in current_user.seguir_cliente:
        print(profissional)
        if str(id_profissional) in str(profissional.profissional.id):
            flash("Você já segue esse profissional {}!".format(profissional.profissional.nome), "alert-warning")
            return redirect(url_for("home_cliente", id_cliente=current_user.id))
    else:
        seguir = Seguir(id_cliente_seguir=current_user.id, id_programador_seguir=id_profissional)
        database.session.add(seguir)
        database.session.commit()
        flash("Programador seguido com sucesso!", "alert-success")
        return redirect(url_for("seguindo", id_cliente=current_user.id))


@app.route("/cliente/unfollow/<id_seguidor>", methods=["GET", "POST"])
@login_required
def parar_seguir(id_seguidor):
    seguidor = Seguir.query.get(id_seguidor)
    if current_user == seguidor.seguidor:
        print(seguidor.seguidor)
        database.session.delete(seguidor)
        database.session.commit()
        flash("Unfollow feito com sucesso", "alert-info")
        return redirect(url_for("home_cliente"))
    else:
        abort(403)


@app.route("/cliente/seguindo/<id_cliente>", methods=["GET", "POST"])
@login_required
def seguindo(id_cliente):
    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data,
                          empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                          descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    cliente = Cliente.query.get(int(id_cliente))
    profissional = Seguir.query.order_by(Seguir.id_programador_seguir.desc()).all()
    return render_template("cliente/C_favoritos.html", cliente=cliente, profissional=profissional, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/excluir-vaga/<id>", methods=["GET", "POST"])
@login_required
def excluir_vaga(id):
    vaga = Vaga.query.get(id)
    print(vaga)
    if current_user == vaga.cliente:
        database.session.delete(vaga)
        database.session.commit()
        flash("Vaga excluída com sucesso", "alert-info")
        return redirect(url_for("minhas_vagas", id_cliente=current_user.id))
    else:
        abort(403)


@app.route("/cliente/ver-vaga/<id>", methods=["GET", "POST"])
@login_required
def ver_mais_vaga(id):
    vaga = Vaga.query.filter_by(id=id).first()

    formcriarvaga = FormCriarVaga()
    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit() and 'botao_servico' in request.form:
        servico = Servico(nome=formcriarservico.nome_servico.data,
                          empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit() and 'botao_projeto' in request.form:
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                          descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    form_editar_vaga = FormEditarVaga()
    if form_editar_vaga.validate_on_submit() and 'botao_editar_vaga' in request.form:
        vaga.nome = form_editar_vaga.nome_vaga.data
        vaga.empresa = form_editar_vaga.empresa_vaga.data
        vaga.endereco = form_editar_vaga.endereco_vaga.data
        vaga.salario = form_editar_vaga.salario_vaga.data
        vaga.descricao = form_editar_vaga.descricao_vaga.data
        vaga.descricao_empresa = form_editar_vaga.descricao_empresa_vaga.data
        vaga.beneficios = form_editar_vaga.beneficios_vaga.data
        vaga.requisitos = form_editar_vaga.requisitos_vaga.data
        vaga.nivel = form_editar_vaga.nivel_vaga.data
        vaga.idioma = form_editar_vaga.idioma_vaga.data
        if form_editar_vaga.foto_vaga.data:
            nome_imagem = salvar_imagem(form_editar_vaga.foto_vaga.data)
            vaga.foto = nome_imagem
        database.session.commit()
        flash("Serviço alterado com sucesso", "alert-success")
        return redirect(url_for("ver_mais_vaga", id=id))
    elif request.method == "GET":
        form_editar_vaga.nome_vaga.data = vaga.nome
        form_editar_vaga.empresa_vaga.data = vaga.empresa
        form_editar_vaga.endereco_vaga.data = vaga.endereco
        form_editar_vaga.salario_vaga.data = vaga.salario
        form_editar_vaga.descricao_vaga.data = vaga.descricao
        form_editar_vaga.descricao_empresa_vaga.data = vaga.descricao_empresa
        form_editar_vaga.beneficios_vaga.data = vaga.beneficios
        form_editar_vaga.requisitos_vaga.data = vaga.requisitos
        form_editar_vaga.nivel_vaga.data = vaga.nivel
        form_editar_vaga.idioma_vaga.data = vaga.idioma

    else:
        flash("Erro", "alert-danger")

    return render_template("cliente/C_ver_mais_vaga.html", form=form_editar_vaga, vaga=vaga, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/excluir-servico/<id>", methods=["GET", "POST"])
@login_required
def excluir_servico(id):
    servico = Servico.query.get(id)
    if current_user == servico.cliente:
        database.session.delete(servico)
        database.session.commit()
        flash("Serviço excluído com sucesso", "alert-info")
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        abort(403)
        
        
@app.route("/cliente/ver-servico/<id>", methods=["GET", "POST"])
@login_required
def ver_mais_servico(id):
    servico = Servico.query.filter_by(id=id).first()

    formcriarvaga = FormCriarVaga()
    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit() and 'botao_servico' in request.form:
        servico = Servico(nome=formcriarservico.nome_servico.data,
                          empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit() and 'botao_projeto' in request.form:
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                          descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    form_editar_servico = FormEditarServico()
    if form_editar_servico.validate_on_submit() and 'botao_editar_servico' in request.form:
        servico.nome = form_editar_servico.nome_servico.data
        servico.empregador = form_editar_servico.empregador_servico.data
        servico.salario = form_editar_servico.salario_servico.data
        servico.requisitos = form_editar_servico.requisitos_servico.data
        servico.descricao = form_editar_servico.descricao_servico.data
        database.session.commit()
        flash("Serviço alterado com sucesso", "alert-success")
        return redirect(url_for("ver_mais_servico", id=id))
    elif request.method == "GET":
        form_editar_servico.nome_servico.data = servico.nome
        form_editar_servico.empregador_servico.data = servico.empregador
        form_editar_servico.salario_servico.data = servico.salario
        form_editar_servico.requisitos_servico.data = servico.requisitos
        form_editar_servico.descricao_servico.data = servico.descricao
    else:
        flash("Erro", "alert-danger")

    return render_template("cliente/C_ver_mais_servico.html", form=form_editar_servico, servico=servico, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/excluir-projeto/<id>", methods=["GET", "POST"])
@login_required
def excluir_projeto(id):
    projeto = Projeto.query.get(id)
    if current_user == projeto.cliente:
        database.session.delete(projeto)
        database.session.commit()
        flash("Projeto excluído com sucesso", "alert-info")
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        abort(403)


@app.route("/cliente/ver-projeto/<id>", methods=["GET", "POST"])
@login_required
def ver_mais_projeto(id):
    projeto = Projeto.query.filter_by(id=id).first()

    formcriarvaga = FormCriarVaga()
    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data,
                          empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit() and 'botao_projeto' in request.form:
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data,
                          descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    form_editar_projeto = FormEditarProjeto()
    if form_editar_projeto.validate_on_submit() and 'botao_editar_projeto' in request.form:
        projeto.nome = form_editar_projeto.nome_projeto.data
        projeto.empregador = form_editar_projeto.empregador_projeto.data
        projeto.tecnologia = form_editar_projeto.tecnologia_projeto.data
        projeto.descricao = form_editar_projeto.descricao_projeto.data
        database.session.commit()
        flash("Projeto alterado com sucesso", "alert-success")
        return redirect(url_for("ver_mais_projeto", id=id))
    elif request.method == "GET":
        form_editar_projeto.nome_projeto.data = projeto.nome
        form_editar_projeto.empregador_projeto.data = projeto.empregador
        form_editar_projeto.tecnologia_projeto.data = projeto.tecnologia
        form_editar_projeto.descricao_projeto.data = projeto.descricao
    else:
        flash("Erro", "alert-danger")

    return render_template("cliente/C_ver_mais_projeto.html", form=form_editar_projeto, projeto=projeto, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/chat/<id>", methods=["GET", "POST"])
def chat_cliente(id):
    contatos = Contato.query.filter_by(id_cliente_contato=current_user.id).all()
    profissional = Profissional.query.filter_by(id=id).first()


    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    FormMensagem = FormChat()

    if FormMensagem.validate_on_submit() and 'botao_enviar_mensagem' in request.form:
        if FormMensagem.anexos.data:
            mensagem = Chat(mensagem=FormMensagem.mensagem.data, anexos=FormMensagem.anexos.data,
                            id_cliente_chat=current_user.id, id_programador_chat=id)
            database.session.add(mensagem)
            database.session.commit()
            flash("Mensagem enviada!", "alert-success")
        else:
            mensagem = Chat(mensagem=FormMensagem.mensagem.data, id_cliente_chat=current_user.id,
                            id_programador_chat=id)
            database.session.add(mensagem)
            database.session.commit()
            flash("Mensagem enviada!", "alert-success")

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_chat.html", form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha, contatos=contatos, form_mensagem=FormMensagem, profissional=profissional)


@app.route("/cliente/chat", methods=["GET", "POST"])
def chat():
    contatos = Contato.query.filter_by(id_cliente_contato=current_user.id).all()


    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_chat_estatico.html", form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha, contatos=contatos)


@app.route("/cliente/vaga/candidatos/<id>")
def candidatos_vaga(id):
    vaga = Vaga.query.filter_by(id=id).first()

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_candidatos_vaga.html", vaga=vaga, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/servico/candidatos/<id>")
def candidatos_servico(id):
    servico = Servico.query.filter_by(id=id).first()

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_candidatos_servico.html", servico=servico, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/projeto/candidatos/<id>")
def candidatos_projeto(id):
    projeto = Projeto.query.filter_by(id=id).first()

    formcriarvaga = FormCriarVaga()

    if formcriarvaga.validate_on_submit():
        arquivo = formcriarvaga.foto_vaga.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"],
                               nome_seguro)
        arquivo.save(caminho)
        vaga = Vaga(nome=formcriarvaga.nome_vaga.data, foto=nome_seguro, nivel=formcriarvaga.nivel_vaga.data,
                    empresa=formcriarvaga.empresa_vaga.data,
                    endereco=formcriarvaga.endereco_vaga.data, salario=formcriarvaga.salario_vaga.data,
                    descricao=formcriarvaga.descricao_vaga.data,
                    descricao_empresa=formcriarvaga.descricao_empresa_vaga.data,
                    beneficios=formcriarvaga.beneficios_vaga.data,
                    requisitos=formcriarvaga.requisitos_vaga.data, idioma=formcriarvaga.idioma_vaga.data,
                    id_cliente_vaga=current_user.id)
        database.session.add(vaga)
        database.session.commit()
        return redirect(url_for('minhas_vagas', id_cliente=current_user.id))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data,
                          descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("meus_servicos", id_cliente=current_user.id))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("meus_projetos", id_cliente=current_user.id))
    else:
        pass

    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso!", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("cliente/C_candidatos_projeto.html", projeto=projeto, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/profissional/ver-mais/projeto/<id>")
def ver_mais_projeto_profissional(id):
    projeto = Projeto.query.filter_by(id=id).first()
    profissional = Profissional.query.filter_by(id=current_user.id).first()

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_ver_mais_projeto.html", projeto=projeto, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/profissional/ver-mais/servico/<id>")
def ver_mais_servico_profissional(id):
    servico = Servico.query.filter_by(id=id).first()
    profissional = Profissional.query.filter_by(id=current_user.id).first()

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_ver_mais_servico.html", servico=servico, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/profissional/ver-mais/vaga/<id>")
def ver_mais_vaga_profissional(id):
    vaga = Vaga.query.filter_by(id=id).first()
    profissional = Profissional.query.filter_by(id=current_user.id).first()

    formeditarsenhaprofissional = FormEditarSenhaProfissional()
    profissional = Profissional.query.filter_by(id=current_user.id).first()
    if formeditarsenhaprofissional.validate_on_submit() and 'botao_editar_senha_profissional' in request.form:
        if bcrypt.check_password_hash(profissional.senha, formeditarsenhaprofissional.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenhaprofissional.senha_nova.data)
            usuario = Profissional.query.filter_by(email=profissional.email).first()
            usuario.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
        else:
            flash("Senha atual incorreta!", "alert-danger")

    return render_template("dev/D_ver_mais_vaga.html", vaga=vaga, form_editar_senha=formeditarsenhaprofissional, profissional=profissional)


@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    formmudarsenha = FormEsqueciSenha()
    if formmudarsenha.validate_on_submit() and 'botao_esqueci_senha' in request.form:
        cliente = Cliente.query.filter_by(email=formmudarsenha.email.data).first()
        profissional = Profissional.query.filter_by(email=formmudarsenha.email.data).first()
        if cliente and bcrypt.check_password_hash(cliente.token, formmudarsenha.token.data):
            senha_nova = bcrypt.generate_password_hash(formmudarsenha.senha_nova.data)
            cliente.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
            redirect(url_for("homepage"))
        elif profissional and bcrypt.check_password_hash(profissional.token, formmudarsenha.token.data):
            senha_nova = bcrypt.generate_password_hash(formmudarsenha.senha_nova.data)
            profissional.senha = senha_nova
            database.session.commit()
            flash("Senha alterada com sucesso", "alert-success")
            redirect(url_for("homepage"))
        else:
            flash("Token ou email incorreto, verifique as credenciais", "alert-danger")

    formsolicitartoken = FormSolicitarToken()
    if formsolicitartoken.validate_on_submit() and 'botao_solicitar_token' in request.form:
        user = Cliente.query.filter_by(email=formsolicitartoken.email_token.data).first()
        profissional = Profissional.query.filter_by(email=formsolicitartoken.email_token.data).first()
        # Se o user existir dentro do banco de dados
        if user:
            # Cria uma secret para guardar o token
            secret = secrets.token_hex(32)
            # Criptografando a secret
            chave = bcrypt.generate_password_hash(secret)
            # Mudando o token do user para a chave
            user.token = chave
            # Fazendo um commit
            database.session.commit()

            # Enviando token
            titulo = "Ola {}! Aqui está sua solicitação de token para redefinição de senha".format(user.nome)
            remetente = "emanuelbrit16@gmail.com"
            msg = Message(titulo, sender=remetente, recipients=[formsolicitartoken.email_token.data])
            msg.subject = "Aqui está seu token {}".format(secret)
            msg.body = "Coloque o {} no campo para poder redefinir a senha".format(secret)
            flash(f"Token enviado para o email {formsolicitartoken.email_token.data} com sucesso", "alert-success")

            # Enviando email
            mail.send(msg)
        elif profissional:
            # Cria uma secret para guardar o token
            secret = secrets.token_hex(32)
            # Criptografando a secret
            chave = bcrypt.generate_password_hash(secret)
            # Mudando o token do user para a chave
            profissional.token = chave
            # Fazendo um commit
            database.session.commit()

            # Enviando token
            titulo = "Ola {}! Aqui está sua solicitação de token para redefinição de senha".format(profissional.nome)
            remetente = "emanuelbrit16@gmail.com"
            msg = Message(titulo, sender=remetente, recipients=[formsolicitartoken.email_token.data])
            msg.subject = "Aqui está seu token {}".format(secret)
            msg.body = "Coloque o {} no campo para poder redefinir a senha".format(secret)
            flash(f"Token enviado para o email {formsolicitartoken.email_token.data} com sucesso", "alert-success")

            # Enviando email
            mail.send(msg)
        else:
            flash("Email inexistente, verifique as credenciais!", "alert-danger")

    return render_template("cliente/esqueciSenha.html", form_mudar_senha=formmudarsenha, form_solicitar_token=formsolicitartoken)


@app.route("/cliente/adicionar-contato/<id>", methods=["GET", "POST"])
def adicionar_contato(id):
    for contato in current_user.contato_cliente:
        if str(id) in str(contato.profissional.id):
            flash("Você já tem esse profissional {} na lista de contato!".format(contato.profissional.nome), "alert-warning")
            return redirect(url_for("home_cliente"))
    else:
        contato = Contato(id_cliente_contato=current_user.id, id_programador_contato=id)
        database.session.add(contato)
        database.session.commit()
        flash("Programador adicionado na lista de contatos!", "alert-success")
        return redirect(url_for("chat"))


@app.route("/profissional/candidatar-vaga/<id>")
def candidatar_vaga(id):
    vaga = Vaga.query.filter_by(id=id).first()
    dev = Profissional.query.filter_by(id=current_user.id).first()

    for profissional in vaga.candidatar_vaga:
        if str(dev.id) in str(profissional.profissional.id):
            flash("Você já candidatou-se a essa vaga!", "alert-info")
            return redirect(url_for("vagas"))
    else:
        candidato = CandidatoVaga(id_vaga_candidato=id, id_programador_candidato=dev.id)
        database.session.add(candidato)
        database.session.commit()
        flash("Candidatura feita com sucesso!", "alert-success")
        return redirect(url_for("vagas"))


@app.route("/profissional/candidatar-servico/<id>")
def candidatar_servico(id):
    servico = Servico.query.filter_by(id=id).first()
    dev = Profissional.query.filter_by(id=current_user.id).first()

    for profissional in servico.candidatar_servico:
        if str(dev.id) in str(profissional.profissional.id):
            flash("Você já candidatou-se a esse serviço!", "alert-info")
            return redirect(url_for("servicos"))
    else:
        candidato = CandidatoServico(id_servico_candidato=id, id_programador_candidato=dev.id)
        database.session.add(candidato)
        database.session.commit()
        flash("Candidatura feita com sucesso!", "alert-success")
        return redirect(url_for("servicos"))


@app.route("/profissional/candidatar-projeto/<id>")
def candidatar_projeto(id):
    projeto = Projeto.query.filter_by(id=id).first()
    dev = Profissional.query.filter_by(id=current_user.id).first()

    for profissional in projeto.candidatar_projeto:
        if str(dev.id) in str(profissional.profissional.id):
            flash("Você já candidatou-se a esse projeto!", "alert-info")
            return redirect(url_for("projetos"))
    else:
        candidato = CandidatoProjeto(id_projeto_candidato=id, id_programador_candidato=dev.id)
        database.session.add(candidato)
        database.session.commit()
        flash("Candidatura feita com sucesso!", "alert-success")
        return redirect(url_for("projetos"))


@app.route("/cliente/mandar-proposta/<id>")
def mandar_proposta(id):
    pass


# Rota do logout
@app.route("/logout")
# Precisa estar logado
@login_required
def logout():
    # Faz o logout do user atual
    logout_user()
    # Mensagem de aviso de logout
    flash("Logout feito com sucesso!", 'alert-info')
    # E redireciona para a homepage
    return redirect(url_for("homepage"))