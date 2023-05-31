# Rotas do site -> links
# render template para renderizar templates
from flask import render_template, url_for, redirect, flash, request, abort # Url for serve para direcionar as paginas pela função
# Importando o app, banco de dados e criptografia
from divtechne import app, database, bcrypt
# Para exigir que em determinadas rotas o usuario so pode entrar se estiver logado, login do user, logout do user, e o usuario atual
from flask_login import login_required, login_user, logout_user, current_user
# Importando os formularios
from divtechne.forms import FormLogin, FormCriarContaCliente, FormCriarContaProfissional, FormCriarVaga, FormCriarServico, FormCriarProjeto, FormEditarPerfilCliente, FormEditarSenha
# Importando o models Usuario e Foto
from divtechne.models import Cliente, Profissional, Vaga, Servico, Projeto, Seguir
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
        # Se esse usuario existir e Verifica a senha desse usuario do email descriptografada e se é igual ao campo digitado pelo usuario
        if cliente and bcrypt.check_password_hash(cliente.senha, formlogin.senha.data):
            # Faça o login do usuario
            login_user(cliente)
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
        else:
            flash("Usuário ou senha incorreta verifique as credenciais", 'alert-danger')

    formcriarconta = FormCriarContaCliente()
    # Se quando ele clicar para enviar as informações estiverem corretas como passamos para ser
    if formcriarconta.validate_on_submit() and 'botao_submit_cliente' in request.form:
        # Se alguem roubar o bd não vai ser possivel ver as senhas mesmo fazendo o caminho contrario no bcrypt por causa que ele usa da nossa secret key
        # Criptografando a senha -> Sequencia de caracteres
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        cpf = bcrypt.generate_password_hash(formcriarconta.cpf.data)
        # Caminho inverso para checar a senha
        # bcrypt.check_password_hash()
        # Dentro de uma variavel coloco as informações que serão adicionadas ou seja todos os data do form
        cliente = Cliente(nome=formcriarconta.nome.data, senha=senha,
                          email=formcriarconta.email.data, cpf=cpf,
                          data_nascimento=formcriarconta.data_nascimento.data)
        # Adicionando o usuario
        database.session.add(cliente)
        # Commit para perpetuar a session
        database.session.commit()
        # Aqui colocamos que ele esta logado
        login_user(cliente, remember=True)  # Aqui ele vai armazenar no cache seu login
        flash(f"Conta para o email {formcriarconta.email.data} criada com sucesso!", "alert-success")
        # Ele vai redirecionar para a função da página perfil e o usuário no link sera dinâmico
        return redirect(url_for("home_cliente"))
    else:
        flash("Verifique as credenciais", "alert-danger")

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
        profissional = Profissional(nome=formprofissional.nome.data, senha=senha,
                                    telefone=formprofissional.telefone.data,
                                    cpf=cpf, nacionalidade=formprofissional.nacionalidade.data,
                                    tecnologia=formprofissional.tecnologia.data, email=formprofissional.email.data,
                                    foto=nome_seguro, data_nascimento=formprofissional.data_nascimento.data,
                                    idioma=formprofissional.idioma.data,
                                    escolaridade=formprofissional.escolaridade.data,
                                    descricao=formprofissional.descricao.data, github=formprofissional.github.data
                                    )
        database.session.add(profissional)
        database.session.commit()
        return redirect(url_for("homepage"))

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
        return redirect(url_for("vagas"))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data, descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
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

    return render_template("cliente/C_home.html", programadores=programador, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto, form_editar_senha=formeditarsenha)


@app.route("/cliente/projetos", methods=["GET", "POST"])
@login_required
def projetos():
    projeto = Projeto.query.order_by(Projeto.data_criacao.desc()).all()

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
        return redirect(url_for("vagas"))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data, descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("projetos.html", projetos=projeto, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


@app.route("/cliente/vagas", methods=["GET", "POST"])
@login_required
def vagas():
    vaga = Vaga.query.order_by(Vaga.data_criacao.desc()).all()

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
        return redirect(url_for("vagas"))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data, descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("vagas.html", vagas=vaga, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


@app.route("/cliente/servicos", methods=["GET", "POST"])
@login_required
def servicos():
    servico = Servico.query.order_by(Servico.data_criacao.desc()).all()

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
        return redirect(url_for("vagas"))
    else:
        pass

    formcriarservico = FormCriarServico()

    if formcriarservico.validate_on_submit():
        servico = Servico(nome=formcriarservico.nome_servico.data, empregador=formcriarservico.empregador_servico.data,
                          salario=formcriarservico.salario_servico.data, descricao=formcriarservico.descricao_servico.data,
                          requisitos=formcriarservico.requisitos_servico.data, id_cliente_servico=current_user.id)
        database.session.add(servico)
        database.session.commit()
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("servicos.html", servicos=servico, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


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
        return redirect(url_for("vagas"))
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
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("minhas_vagas.html", cliente=cliente, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


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
        return redirect(url_for("vagas"))
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
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("meus_servicos.html", cliente=cliente, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


@app.route("/cliente/projetos/<id_cliente>", methods=["GET", "POST"])
@login_required
def meus_projetos(id_cliente):
    cliente = Cliente.query.get(int(id_cliente))

    formcriarvaga = FormCriarVaga()
    programador = Profissional.query.order_by(Profissional.tecnologia.desc()).all()

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
        return redirect(url_for("vagas"))
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
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("meus_projetos.html", cliente=cliente, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


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
            return redirect(url_for("vagas"))
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
            return redirect(url_for("servicos"))
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
            return redirect(url_for("projetos"))
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
            return redirect(url_for("vagas"))
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
            return redirect(url_for("servicos"))
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
            return redirect(url_for("projetos"))
        else:
            pass
        usuario = Cliente.query.get(int(id_usuario))

        return render_template("perfil.html", usuario=usuario, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)



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
        return redirect(url_for("vagas"))
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
        return redirect(url_for("servicos"))
    else:
        pass

    formcriarprojeto = FormCriarProjeto()
    if formcriarprojeto.validate_on_submit():
        projeto = Projeto(nome=formcriarprojeto.nome_projeto.data, descricao=formcriarprojeto.descricao_projeto.data,
                          tecnologia=formcriarprojeto.tecnologia_projeto.data,
                          empregador=formcriarprojeto.empregador_projeto.data, id_cliente_projeto=current_user.id)
        database.session.add(projeto)
        database.session.commit()
        return redirect(url_for("projetos"))
    else:
        pass

    return render_template("meuperfilcliente.html", form=formeditar, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


@app.route("/perfil/profissional/<id_profissional>", methods=["GET", "POST"])
@login_required
def perfil_profissional(id_profissional):

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
        return redirect(url_for("vagas"))
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
        return redirect(url_for("servicos"))
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
        return redirect(url_for("projetos"))
    else:
        pass
    profissional = Profissional.query.get(int(id_profissional))

    return render_template("perfil_profissional.html", profissional=profissional, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


@app.route("/seguir/<id_profissional>", methods=["GET", "POST"])
@login_required
def seguir_profissional(id_profissional):
    id_profissionais = Seguir.query.filter_by(id_programador_seguir=id_profissional).all()
    print(current_user.seguir_cliente)
    for profissional in current_user.seguir_cliente:
        print(profissional)
        if str(id_profissional) in str(profissional.id_programador_seguir):
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
        return redirect(url_for("vagas"))
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
        return redirect(url_for("servicos"))
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
        return redirect(url_for("projetos"))
    else:
        pass

    cliente = Cliente.query.get(int(id_cliente))
    profissional = Seguir.query.order_by(Seguir.id_programador_seguir.desc()).all()
    return render_template("seguindo.html", cliente=cliente, profissional=profissional, form_vaga=formcriarvaga, form_servico=formcriarservico, form_projeto=formcriarprojeto)


@app.route("/cliente/editar_senha")
def editar_senha():
    formeditarsenha = FormEditarSenha()
    if formeditarsenha.validate_on_submit() and 'botao_editar_senha' in request.form:
        if bcrypt.check_password_hash(current_user.senha, formeditarsenha.senha_atual.data):
            senha_nova = bcrypt.generate_password_hash(formeditarsenha.senha_nova.data)
            usuario = Cliente.query.filter_by(email=current_user.email).first()
            usuario.senha = senha_nova
            database.session.commit()
        else:
            flash("Senha atual incorreta!", "alert-danger")


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