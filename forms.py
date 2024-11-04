from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from email_validator import validate_email, EmailNotValidError

class RegistroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    idade = IntegerField('Idade', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')], validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=30)])
    confirmar_senha = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
    # submit = SubmitField('Registrar')

    def validate_email_format(self, field):
        try:
            # Valida o e-mail
            validate_email(field.data)
        except EmailNotValidError as e:
            # Se o e-mail não for válido, lance um erro
            raise ValueError(str(e))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class CalculadoraForm(FlaskForm):
    peso = FloatField('Peso (kg)', validators=[DataRequired()])
    altura = FloatField('Altura (cm)', validators=[DataRequired()])
    submit = SubmitField('Calcular Gasto Calórico')

