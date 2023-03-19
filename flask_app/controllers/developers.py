from flask import render_template,redirect,session,request, flash
from flask_app.models.developer import Developer
from flask_app.models.skill import Skill
from flask_app.models.skill_of_developer import Skill_of_developer
from flask_app.models.count import Count
from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/devs/login')
def index():
    return render_template('logindev.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/devs/login')


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


@app.route('/devs/register')
def index_dev():
    return render_template('registerdev.html')


@app.route('/devs/dashboard_dev')
def dashboard_dev():
    return render_template('dashboard_dev.html')


@app.route('/devs/skill/languages')
def dev_skill_language():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }
    print('DATA TRAE:', data)
    # developer = Developer.get_skill_by_developer(data)

    # for dev in developer.skills:
    #    print('SKILLS:', dev.id)
    #    print('SKILLS:', dev.name)
    #   print('SKILLS:', dev.tipo)

    data_skill_of_developer={
        "developer_id": session['user_id']
    }
    verificarCantidadSkill = Count.getCountSkill_lang_by_developer(data_skill_of_developer)
    print('VERIFICAR CANTIDAD DE SKILL EN LISTAR TIENE////////////////////////////////', verificarCantidadSkill[0]['count'])

    return render_template('skills.html', developer = Developer.get_skill_lang_by_developer(data), cant_Skill = verificarCantidadSkill[0]['count'], dev_shortBio = Developer.get_one(data))


@app.route('/register_new_dev', methods=['POST'])
def register_new_dev():
    print(request.form)
    if not Developer.validate_register(request.form):
        return redirect('/devs/register')
    data ={
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "github_user" : request.form["github_user"],
        "address" : request.form["address"],
        "city" : request.form["city"],
        "state" : request.form["state"],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "available" : request.form["available"]
    }

    id = Developer.create_developer(data)
    print('EL ID EN EL REGISTER TIENE VALOR:', id)
    session['user_id'] = id
    return redirect('/devs/skill/languages')


@app.route('/topfiveskill_lang/<int:skill_id>/<string:name_skill>')
def topfiveskill_lang(skill_id,name_skill):

    developer_id = session['user_id']
    
    if 'user_id' not in session: # Compruebo que el usuario este logueado para poder guardar el skill, si no esta logueado entonces limpiamos la session
        return redirect('/logout')
    data ={
        "id": skill_id,
        "name" : name_skill
    }

    data_skill_of_developer={
        "developer_id": developer_id,
        "skill_id": skill_id
    }

    # Verifica si existe el 'skill' con el 'skill_id' y 'name_skill'
    verificar = Skill.get_one_skill(data)
    print('VERIFICAR TIENE', verificar)

    # Verifica la cantidad de 'Skill de lenguajes' que tiene el developer actual
    verificarCantidadSkill = Count.getCountSkill_lang_by_developer(data_skill_of_developer)
    print('VERIFICAR CANTIDAD DE SKILL TIENE', verificarCantidadSkill[0]['count'])

    # Si es que el verificar devuelve None entonces el Skill no existe, por tanto se lanza un mensaje de 'Skill Inexistente'
    if verificar is not None: # Si verificar no esta vacío entonces entra
        if verificarCantidadSkill[0]['count'] < 5: # Si es que la cantidad de Skill del developer es menor a 5 entonces guarda en la base de datos
            Skill_of_developer.save(data_skill_of_developer)
        else:
            flash("DENEGADO: Máximo 5 Skills", "skill_lan") # Si la cantidad de Skill es 5 o mayor a 5 entonces lanza el mensaje
    else:
        flash("Skill Inexistente", "skill_lan") # Si el Skill no existe entontonces lanza este mensaje

    return redirect('/devs/skill/languages')


@app.route('/update_shorBio', methods=['POST'])
def update_shortBio():
    data ={
        "id": session['user_id'],
        "short_bio": request.form["short_bio"]
    }
    Developer.update_short_bio(data)
    return redirect('/devs/skills/frameworks')


@app.route('/devs/skills/frameworks')
def devs_skills_frameworks():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }
    print('DATA TRAE:', data)
    # developer = Developer.get_skill_by_developer(data)

    # for dev in developer.skills:
    #    print('SKILLS:', dev.id)
    #    print('SKILLS:', dev.name)
    #   print('SKILLS:', dev.tipo)

    data_skill_of_developer={
        "developer_id": session['user_id']
    }
    verificarCantidad_total_Skill = Count.getCount_all_Skill_by_developer(data_skill_of_developer)
    print('VERIFICAR CANTIDAD DE SKILL EN LISTAR FRAMEWORKS TIENE////////////////////////////////', verificarCantidad_total_Skill[0]['count'])

    # developer = Developer.get_skill_lang_by_developer(data), cant_Skill = verificarCantidadSkill[0]['count'], dev_shortBio = Developer.get_one(data)
    return render_template('frameworks.html', developer = Developer.get_skill_fram_by_developer(data), cant_Skill = verificarCantidad_total_Skill[0]['count'])


@app.route('/delete_Skill_lang/<int:skill_id>/<string:name_skill>')
def delete_Skill_lang(skill_id, name_skill):

    data={
        "developer_id": session['user_id'],
        "skill_id": skill_id,

        "id": skill_id,
        "name" : name_skill
    }
    verificar = Skill.get_one_skill(data)
    print('VERIFICAR EN DELETE TIENE', verificar)

    if verificar is not None: # Si verificar no esta vacío entonces entra
        Skill_of_developer.destroy(data)
    else:
        flash("Skill Inexistente", "skill_lan")

    return redirect('/devs/skill/languages')


@app.route('/topfiveskill_fram/<int:skill_id>/<string:name_skill>')
def topfiveskill_fram(skill_id,name_skill):

    developer_id = session['user_id']
    
    if 'user_id' not in session: # Compruebo que el usuario este logueado para poder guardar el skill, si no esta logueado entonces limpiamos la session
        return redirect('/logout')
    data ={
        "id": skill_id,
        "name" : name_skill
    }

    data_skill_of_developer={
        "developer_id": developer_id,
        "skill_id": skill_id
    }

    # Verifica si existe el 'skill' con el 'skill_id' y 'name_skill'
    verificar = Skill.get_one_skill(data)
    print('VERIFICAR EN FRAMEWORKS TIENE', verificar)

    # Verifica la cantidad de 'Skill de frameworks' que tiene el developer actual
    verificarCantidadSkill = Count.getCountSkill_fram_by_developer(data_skill_of_developer)
    print('VERIFICAR CANTIDAD DE SKILL DE FRAMEWORKS TIENE', verificarCantidadSkill[0]['count'])

    # Si es que el verificar devuelve None entonces el Skill no existe, por tanto se lanza un mensaje de 'Skill Inexistente'
    if verificar is not None: # Si verificar no esta vacío entonces entra
        if verificarCantidadSkill[0]['count'] < 5: # Si es que la cantidad de 'Skill de frameworks' del developer es menor a 5 entonces guarda en la base de datos
            Skill_of_developer.save(data_skill_of_developer)
        else:
            flash("DENEGADO: Máximo 5 Skills", "skill_fram") # Si la cantidad de Skill es 5 o mayor a 5 entonces lanza el mensaje
    else:
        flash("Skill Inexistente", "skill_lan") # Si el Skill no existe entontonces lanza este mensaje

    return redirect('/devs/skills/frameworks')


@app.route('/delete_Skill_fram/<int:skill_id>/<string:name_skill>')
def delete_Skill_fram(skill_id, name_skill):

    data={
        "developer_id": session['user_id'],
        "skill_id": skill_id,

        "id": skill_id,
        "name" : name_skill
    }
    verificar = Skill.get_one_skill(data)
    print('VERIFICAR EN DELETE TIENE', verificar)

    if verificar is not None: # Si verificar no esta vacío entonces entra
        Skill_of_developer.destroy(data)
    else:
        flash("Skill Inexistente", "skill_lan")

    return redirect('/devs/skills/frameworks')
