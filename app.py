from flask import Flask, render_template, url_for, flash, redirect
from config import Config
from forms import RegistroForm, LoginForm, CalculadoraForm
from models import db, Usuario, GastoCalorico
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
from flask_login import logout_user, login_required
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

# Inicialize o db e as outras extensões com o app configurado
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.route('/')
def home():
    return render_template('base.html')  # Certifique-se de que o template existe

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        user = Usuario(nome=form.nome.data, email=form.email.data, idade=form.idade.data, sexo=form.sexo.data)
        user.set_password(form.senha.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.senha.data):
            login_user(user)
            return redirect(url_for('calculator'))
        else:
            flash('Login ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

def calcular_gasto_calorico(sexo, peso, altura, idade):
    if sexo == 'M':
        return 66 + (13.7 * peso) + (5.0 * altura) - (6.8 * idade)
    else:
        return 665 + (9.6 * peso) + (1.8 * altura) - (4.7 * idade)

@app.route("/calculator", methods=['GET', 'POST'])
@login_required
def calculator():
    form = CalculadoraForm()
    idade = current_user.idade
    saudacao = "Bem-vindo" if current_user.sexo == 'M' else "Bem-vinda"

    if form.validate_on_submit():
        peso = form.peso.data
        altura = form.altura.data
        total = calcular_gasto_calorico(current_user.sexo, peso, altura, idade)
        gasto = GastoCalorico(peso=peso, altura=altura, total=total, usuario_id=current_user.id)
        db.session.add(gasto)
        db.session.commit()
        return render_template('calculator.html', form=form, total=total, saudacao=saudacao, nome=current_user.nome,
                               idade=idade)

    return render_template('calculator.html', form=form, saudacao=saudacao, nome=current_user.nome, idade=idade)

@app.route('/logout')
@login_required  # Garante que apenas usuários autenticados possam fazer logout
def logout():
    logout_user()  # Desloga o usuário
    return redirect(url_for('login'))  # Redireciona para a página de login


if __name__ == "__main__":
    app.run(debug=True)
