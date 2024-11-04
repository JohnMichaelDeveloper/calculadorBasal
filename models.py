from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()  # Declarar bcrypt aqui

class Usuario(db.Model, UserMixin):  # Adicione UserMixin aqui
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)

    def set_password(self, senha):
        self.senha = bcrypt.generate_password_hash(senha).decode('utf-8')

    def check_password(self, senha):
        return bcrypt.check_password_hash(self.senha, senha)

    # Métodos do UserMixin
    def is_active(self):
        return True  # Retorna True para indicar que o usuário está ativo

class GastoCalorico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
