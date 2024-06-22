from app import db

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