from flask import render_template,redirect,session,request, flash
from flask_app.models.developer import Developer
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/devs/login')
def index():
    return render_template('logindev.html')


@app.route('/login', methods=['POST'])
def logindev():
    user = Developer.getEmail(request.form['email'])
    print('USER EN EL LOGIN TIENE:', user)

    if not user:
        flash("Email inválido", "login")
        return redirect('/devs/login')
    if user is None or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Contraseña inválida", "login")
        return redirect('/devs/login')
    print('USER.ID TIENE:', user.id)
    session['user_id'] = user.id
    return redirect('/devs/skill/languages')


@app.route('/registerdev')
def index_dev():
    return render_template('registerdev.html')


@app.route('/devs/skill/languages')
def dev_skill_language():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('skills.html')


@app.route('/register_new_dev', methods=['POST'])
def register_new_dev():
    print(request.form)
    if not Developer.validate_register(request.form):
        return redirect('/registerdev')
    data ={
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "github_user" : request.form["github_user"],
        "address" : request.form["address"],
        "city" : request.form["city"],
        "state" : request.form["state"],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "available" : request.form["available"],

    }
    id = Developer.create_developer(data)
    print('EL ID EN EL REGISTER TIENE VALOR:', id)
    session['user_id'] = id
    return redirect('/devs/skill/languages')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/devs/login')