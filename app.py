from flask import Flask, render_template, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'vds_gpcit'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}@{servidor}/{database}'.format(
      SGBD = 'mysql',
      usuario= 'root',
      servidor= 'localhost',
      database= 'vendas_gpc'
    )

db = SQLAlchemy(app)

class Vendas(db.Model):
  nf = db.Column(db.Integer, primary_key=True, nullable=False)
  data = db.Column(db.String(50), nullable=False)
  empresa = db.Column(db.Integer, nullable=False)
  vendedor = db.Column(db.String(40), nullable=False)
  cliente = db.Column(db.String(150), nullable=False)
  produto = db.Column(db.String(200), nullable=False)
  estado = db.Column(db.String(20), nullable=False)
  valor = db.Column(db.Float, nullable=False)
  valor_final = db.Column(db.Float, nullable=False)
  parceiro = db.Column(db.String(40), nullable=False)

  def __repr__(self) :
    return '<Name %r>' % self.name
  
class Usuarios(db.Model):
  nome = db.Column(db.String(50), nullable=False)
  nome_de_usuario = db.Column(db.String(20), primary_key=True, nullable=False)
  senha = db.Column(db.String(100), nullable=False)
  

  def __repr__(self) :
    return '<Name %r>' % self.name

@app.route('/')
def index():

  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect('/login')
  else:
    vendas = Vendas.query.order_by(Vendas.nf)

    usuario = Usuarios.query.filter_by(nome_de_usuario=session['usuario_logado']).first()

    return render_template('index.html', usuario=usuario.nome, vendas=vendas)

@app.route('/nova-venda')
def nova_venda():
  return render_template('nova_venda.html')

@app.route('/inserir', methods=['POST',])
def inserir():
  nf = request.form['nf']
  data = request.form['data']
  empresa = request.form['empresa']
  vendedor = request.form['vendedor']
  cliente = request.form['cliente']
  produto = request.form['produto']
  estado = request.form['estado']
  valor = request.form['valor']
  valor_final = request.form['valor_final']
  parceiro = request.form['parceiro']

  venda = Vendas.query.filter_by(nf=nf).first()

  if venda:
    flash('Jogo já existente')
    return redirect('/')
  
  nova_vd = Vendas(nf=nf, data=data, empresa=empresa, vendedor=vendedor,cliente=cliente,produto=produto,estado=estado,valor=valor,valor_final=valor_final, parceiro=parceiro)

  db.session.add(nova_vd)
  db.session.commit()

  return redirect('/')

@app.route('/login')
def login():

  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return render_template('login.html')
  else: 
    return redirect('/')



@app.route('/autenticar', methods=['POST',])
def autenticar():

    usuario = Usuarios.query.filter_by(nome_de_usuario=request.form['nome_de_usuario']).first()

    if usuario:
        if request.form['senha_do_usuario'] == usuario.senha:
          session['usuario_logado'] = usuario.nome_de_usuario
          flash(usuario.nome_de_usuario + "logado com sucesso")
          return redirect('/')
    else:
      flash('Usuário não logado!')
      return redirect('/login')
  
@app.route('/logout')
def logout():
  session['usuario_logado'] = None
  flash('Logout efetuado com sucesso!')
  return redirect('/login')

app.run(debug=True)