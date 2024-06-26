from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, validators, SubmitField, DateField

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

class FormularioVenda(FlaskForm):
    nf = IntegerField('N° da Nota Fiscal', [validators.DataRequired()])
    data = DateField('Data da venda', [validators.DataRequired()])
    empresa = IntegerField('Empresa (Digite o n°)', [validators.DataRequired()])
    vendedor = ""
    cliente = StringField('Nome do Cliente/Empresa', [validators.DataRequired(), validators.Length(min=1, max=150)])
    produto = StringField('Nome do produto', [validators.DataRequired(), validators.Length(min=1, max=200)])
    estado = StringField('UF do Cliente/Empresa', [validators.DataRequired(), validators.Length(min=1, max=20)])
    valor = StringField('Valor da venda (ex. 2160.00)', [validators.DataRequired()])
    valor_final = StringField('Valor da venda final (ex. 2160.00)', [validators.DataRequired()])
    parceiro = StringField('Nome do Parceiro (caso não tenha, digite "--")',[validators.DataRequired(), validators.Length(min=1, max=40)])

    enviar = SubmitField('Enviar') 