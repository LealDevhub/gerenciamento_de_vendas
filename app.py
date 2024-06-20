from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.secret_key = 'vds_gpcit'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}@{servidor}/{database}'.format(
      SGBD = 'mysql',
      usuario= 'root',
      servidor= 'localhost',
      database= 'vendas_gpc',
    )

db = SQLAlchemy(app)

class Vendas(db.Model):
  nf = db.Column(db.Integer, primary_key=True, nullable=False)
  data = db.Column(db.String(50), nullable=False)
  empresa = db.Column(db.Integer, nullable=False)
  vendedor = db.Column(db.String(40), nullable=False)
  vendedor_id = db.Column(db.String(40), nullable=False)
  cliente = db.Column(db.String(150), nullable=False)
  produto = db.Column(db.String(200), nullable=False)
  estado = db.Column(db.String(20), nullable=False)
  valor = db.Column(db.Float, nullable=False)
  valor_final = db.Column(db.Float, nullable=False)
  parceiro = db.Column(db.String(40), nullable=False)
  rma = db.Column(db.Boolean, nullable=False)

  def __repr__(self) :
    return '<Name %r>' % self.name
  
class Usuarios(db.Model):
  nome = db.Column(db.String(50), nullable=False)
  id_user = db.Column(db.String(50), primary_key=True, nullable=False)
  nome_de_usuario = db.Column(db.String(50), nullable=False)
  senha = db.Column(db.String(100), nullable=False)
  supervisor = db.Column(db.Boolean, nullable=False)
  email = db.Column(db.String(200), nullable=False)
  telefone = db.Column(db.String(50), nullable=False)
  

  def __repr__(self) :
    return '<Name %r>' % self.name

@app.route('/')
def index():
  # Condicional que identifica se o usuário está logado
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  else:
    # adiciona a uma variável "usuário" o item do banco da dados filtrado pelo nome de usuário 
    usuario = Usuarios.query.filter_by(nome_de_usuario=session['usuario_logado']).first()

    if usuario.supervisor == 1:
      vendas = Vendas.query.order_by(Vendas.data)
    else:
      # adiciona a uma variável "vendas" uma lista de vendas filtrada pelo id do usuário ordenada por meio das datas das vendas no banco de dados
      vendas = Vendas.query.filter_by(vendedor_id=usuario.id_user).order_by(Vendas.data)

    usuarios = Usuarios.query.order_by(Usuarios.nome)
    # renderiza o index, com atributos Nome, e envia a lista de vendas para o HTML
    return render_template('index.html', usuario=usuario.nome,
    supervisor=usuario.supervisor , vendas=vendas, usuarios=usuarios)

@app.route('/nova-venda')
def nova_venda():
  # Condicional que identifica se o usuário está logado
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  else:
    # a variárel usuários oferece uma lista com o nome dos vendedores para o HTML
    usuarios = Usuarios.query.order_by(Usuarios.nome)
    # renderiza o template de nova venda
    return render_template('nova_venda.html', users=usuarios, titulo="Nova venda - Gerenciamento de vendas")
# rota intermediária para inserir dados da app no Banco de dados
@app.route('/inserir', methods=['POST',])
def inserir():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')

  nf = request.form['nf']
  dt_input = request.form['data'].split('-')
  dt_input.reverse()
  # a data está sendo formatada para o modelo usado no Brasil
  data_br = '/'.join(dt_input)
  empresa = request.form['empresa']
  vendedor_id = request.form['ids-vendedor']

  #A variáriel user localiza no banco de dados "usuarios" o id do vendedor enviado pelo HTML
  user = Usuarios.query.filter_by(id_user=vendedor_id).first()
  # A variável vendedor_nome recebe o nome do id do usuário localizado anteriormente
  vendedor_nome = user.nome

  cliente = request.form['cliente']
  produto = request.form['produto']
  estado = request.form['estado']
  valor = request.form['valor']
  valor_final = request.form['valor_final']
  parceiro = request.form['parceiro']
  rma = False

  # adiciona a uma variável "venda" o item do banco da dados filtrado pelo numero da nf
  venda = Vendas.query.filter_by(nf=nf).first()

  # condicional se a venda já existir no banco de dados
  if venda:
    flash('Venda já existente')
    return redirect('/')
  
  # variável nova_vd é atribuida uma instanciação da classe vendas, inserindo os dados requisitados dos formulários HTML
  nova_vd = Vendas(nf=nf, data=data_br, empresa=empresa, vendedor=vendedor_nome, vendedor_id=vendedor_id,cliente=cliente,produto=produto,estado=estado,valor=valor,valor_final=valor_final, parceiro=parceiro, rma=rma)

  # Enviando e commitando os dados para o banco de dados
  db.session.add(nova_vd)
  db.session.commit()

  return redirect('/')

@app.route('/login')
def login():
  # Condicional que identifica se o usuário está logado
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return render_template('login.html', titulo="Login - Gerenciamento de vendas")
  else: 
    return redirect(url_for('index'))

@app.route('/novo-usuario')
def novo_usuario():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')

  return render_template('criar-novo-usuario.html', header_title='Cadastrar novo usuário',titulo="Cadastrar novo usuário - Gerenciamento de vendas")

@app.route('/criar-novo-usuario', methods=['POST',])
def criar_novo_usuario():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')

  nome_de_usuario = request.form['nome_de_usuario']
  nome = request.form['nome']
  senha = request.form['senha_do_usuario']
  supervisao = request.form['supervisao']
  email = request.form['email']
  telefone = request.form['telefone']
  alfabeto = string.ascii_lowercase
  numeros = '123456789'
  combinar = alfabeto + numeros
  comprimento = 6

  id_user = ''.join(random.sample(combinar, comprimento))

  novo_usuario = Usuarios(nome = nome, id_user = id_user, senha=senha, nome_de_usuario=nome_de_usuario, supervisor= bool(supervisao), email=email, telefone=telefone )

  db.session.add(novo_usuario)
  db.session.commit()

  return redirect(url_for('index'))

@app.route('/alterar-cadastro')
def alterar_cadastro():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')

  user_id = request.args.get('usuario')
  usuario = Usuarios.query.filter_by(id_user=user_id).first()

  return render_template('alterar-cadastro.html', titulo="Alterar cadastro - Gerenciamento de vendas", header_title='Alterar cadastro de usuário', usuario=usuario)

@app.route('/alterar-cadastro-bd', methods=['POST',])
def alterar_cadastro_bd():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  
  id_user = request.args.get('usuario')

  usuario = Usuarios.query.filter_by(id_user=id_user).first()

  usuario.nome_de_usuario = request.form['nome_de_usuario']
  usuario.nome = request.form['nome']
  usuario.senha = request.form['senha_do_usuario']
  supervisor = request.form['supervisao']
  usuario.email = request.form['email']
  usuario.telefone = request.form['telefone']
  
  if supervisor == '1':
    usuario.supervisor = True
  else:
    usuario.supervisor = False

  db.session.add(usuario)
  db.session.commit()

  return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect('/login')
    # a variável usuario é atribuida o item do banco de dados filtrado pelo nome de usuário requisitado pelo HTML
    usuario = Usuarios.query.filter_by(nome_de_usuario=request.form['nome_de_usuario']).first()

    # condicional, se usuário for existente, avaliando se a senha de usuário requisitado do HTML é o mesmo que o banco de dados
    if usuario:
        if request.form['senha_do_usuario'] == usuario.senha:
          session['usuario_logado'] = usuario.nome_de_usuario
          flash(usuario.nome_de_usuario + "logado com sucesso")
          return redirect(url_for('index'))
        else:
          flash('Senha incorreta')
    else:
      flash('Usuário não logado!')
    
    return redirect('/login')
    
@app.route('/alterar-venda')
def alterar():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect(url_for('login'))
  
  nf_req_url = request.args.get('venda')
  vd_localizada = Vendas.query.filter_by(nf=nf_req_url).first()

  dt_bd = vd_localizada.data.split('/')
  dt_bd.reverse()
  vd_localizada.data = '-'.join(dt_bd)

  return render_template("alterar.html", venda=vd_localizada, titulo="Alterar venda - Gerenciamento de vendas")

@app.route('/alterar-venda-bd', methods=['POST',])
def alterar_bd():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')

  nf = request.args.get('nf')
  venda = Vendas.query.filter_by(nf=nf).first()
  venda.nf = request.form['nf']
  dt_input = request.form['data'].split('-')
  dt_input.reverse()
  venda.data = '/'.join(dt_input)
  venda.empresa = request.form['empresa']
  venda.vendedor = request.form['vendedor']
  venda.cliente = request.form['cliente']
  venda.produto = request.form['produto']
  venda.estado = request.form['estado']
  venda.valor = request.form['valor']
  venda.valor_final = request.form['valor_final']
  venda.parceiro = request.form['parceiro']

  db.session.add(venda)
  db.session.commit()

  return redirect(url_for('index'))

@app.route('/excluir-venda', methods=['POST'],)
def excluir():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  
  nf_req_url = request.args.get('venda')
  vd_localizada = Vendas.query.filter_by(nf=nf_req_url).first()

  usuario = Usuarios.query.filter_by(nome_de_usuario=session['usuario_logado']).first()

  if request.form['senha'] == usuario.senha:
    db.session.delete(vd_localizada)
    db.session.commit()
  else:
    flash('Senha incorreta ao excluir, tente novamente !')

  return redirect(url_for('index'))

@app.route('/abrir-rma', methods=['POST',])
def abrir_rma():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  
  nf_req_url = request.args.get('venda')
  vd_localizada = Vendas.query.filter_by(nf=nf_req_url).first()
  vd_localizada.rma = True

  usuario = Usuarios.query.filter_by(nome_de_usuario=session['usuario_logado']).first()

  if request.form['senha'] == usuario.senha:
    db.session.add(vd_localizada)
    db.session.commit()
  else:
    
    flash('Senha incorreta ao abrir RMA, tente novamente !')

  return redirect(url_for('index'))

@app.route('/excluir-rma', methods=['POST',])
def excluir_rma():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  
  nf_req_url = request.args.get('venda')
  vd_localizada = Vendas.query.filter_by(nf=nf_req_url).first()
  vd_localizada.rma = False

  usuario = Usuarios.query.filter_by(nome_de_usuario=session['usuario_logado']).first()

  if request.form['senha'] == usuario.senha:
    db.session.add(vd_localizada)
    db.session.commit()
  else:
    flash('Senha incorreta ao abrir RMA, tente novamente !')

  return redirect(url_for('index'))

@app.route('/logout')
def logout():
  session['usuario_logado'] = None
  flash('Logout efetuado com sucesso!')
  return redirect(url_for('login'))

app.run(debug=True)