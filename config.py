import os

class Config:
    SECRET_KEY = 'sua palavra chave'
    SQLALCHEMY_DATABASE_URI = 'postgresql://SeuUsuario:suaSenha@localhost:5432/calculationbasal'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

