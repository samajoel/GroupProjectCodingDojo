from flask import render_template,redirect,session,request, flash
from flask_app.models.developer import Developer
from flask_app.models.organization import Organization
from flask_app.models.skill import Skill
from flask_app.models.skill_of_developer import Skill_of_developer
from flask_app.models.count import Count
from flask_app.models.position import Position
from flask_app.models.skill_of_position import Skill_of_position
from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ===================================== CIERRA SESIÓN =====================================
@app.route('/logout_org')
def logout_org():
    session.clear()
    return redirect('/orgs/login')


# ===================================== VISTA DEL LOGIN DE ORGANIZACIÓN =====================================
@app.route('/orgs/login')
def index_loginorg():
    return render_template('loginorg.html')


# ===================================== VISTA DE DEVELOPERS DISPONIBLES - 'MATCH' =====================================
@app.route('/orgs/jobs/availabledevs')
def availabledevs():
    if 'org_id' not in session:
        return redirect('/logout_org')
    

    return render_template('availabledevs.html', allDevelopers = Developer.get_all())


# ===================================== VISTA DE ADDPOSITIONS =====================================
@app.route('/orgs/jobs/new')
def addposition():
    if 'org_id' not in session:
        return redirect('/logout_org')
    return render_template('addposition.html')


# ===================================== VISTA DE ADDPOSITIONS redireccionado desde el add_new_position =====================================
@app.route('/orgs/jobss/new/<int:id_position>')
def addpositions(id_position):
    if 'org_id' not in session:
        return redirect('/logout_org')

    data ={
        "id": id_position,
        "organization_id": session['org_id']
    }
    # print('Esto TRAE EL GET ONE DESDE EL REDIRECCIONAMIENTO DE ADD POSITION: ', Position.get_one_position(data))

    # Prueba = Position.get_skill_by_position(data)
    # print('PRUEBA TIENE:', Prueba)

    return render_template('addposition_redirect.html', position = Position.get_one_position(data), all_skill_by_position = Position.get_skill_by_position(data))


# ===================================== VISTA DE DASHBOARD DE ORGANIZACIÓN =====================================
@app.route('/orgs/dashboard_org')
def dashboard_org():
    if 'org_id' not in session:
        return redirect('/logout_org')
    
    data ={
        "organization_id": session['org_id']
    }
    
    #allPositionByOrganization = Position.getPosition_by_organization(data)
    # print('ALL POSITION BY ORGANIZATION:',allPositionByOrganization)

    # allDevelopers = Developer.get_all_developer()
    # print('ALL DEVELOPERS: ', allDevelopers)

    return render_template('dashboard_org.html', allPositionByOrganization = Position.getPosition_by_organization(data), allDevelopers = Developer.get_all())


# ===================================== VISTA DE REGISTRO DE NUEVA ORGANIZACIÓN =====================================
@app.route('/orgs/register')
def index_org():
    return render_template('registerorg.html')


# ===================================== REGISTRAR NUEVA ORGANIZACIÓN=====================================
@app.route('/register_new_org', methods=['POST'])
def register_new_org():
    print(request.form)
    if not Organization.validate_register(request.form):
        return redirect('/orgs/register')
    data ={
        "org_name": request.form["org_name"],
        "email" : request.form["email"],
        "address" : request.form["address"],
        "city" : request.form["city"],
        "state" : request.form["state"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    id = Organization.create_organization(data)
    print('EL ID EN EL REGISTER DE ORGANIZATION TIENE VALOR:', id)
    session['org_id'] = id
    return redirect('/orgs/dashboard_org')


# ===================================== COMPROBAR QUE LOS DATOS DEL LOGIN SEAN CORRECTOS =====================================
@app.route('/orgs/login', methods=['POST'])
def loginorg():
    user_org = Organization.getEmail(request.form['email'])
    print('USER EN EL LOGIN TIENE:', user_org)

    if not user_org:
        flash("Email inválido", "login_org")
        return redirect('/orgs/login')
    if user_org is None or not bcrypt.check_password_hash(user_org.password, request.form['password']):
        flash("Contraseña inválida", "login_org")
        return redirect('/orgs/login')
    print('USER.ID TIENE:', user_org.id)
    session['org_id'] = user_org.id
    return redirect('/orgs/dashboard_org')


# ===================================== CREAR UNA NUEVA POSITION - Solo Name y Description =====================================
@app.route('/add_new_position', methods=['POST'])
def add_new_position():
    print('DATOS OBTENIDOS DEL FORMULARIO DE ADD POSITION', request.form)
    if not Position.validate_position(request.form):
        return redirect('/orgs/jobs/new')
    data ={
        "name": request.form["name"],
        "description" : request.form["description"],
        "organization_id" : session['org_id']
    }
    id_position = Position.create_position(data)
    print('EL ID DE LA NUEVA ORGANIZACIÓN CREADA TIENE:', id_position)

    return redirect(f'/orgs/jobss/new/{id_position}')


# ===================================== UPDATE POSITION - Solo Name y Description =====================================
@app.route('/update_position', methods=['POST'])
def update_position():
    print('DATOS OBTENIDOS DEL FORMULARIO DESDE update_position', request.form)
    if not Position.validate_position_redirect(request.form):
        return redirect(f'/orgs/jobss/new/{request.form["id"]}')
    data ={
        "id" : request.form["id"], # ID de la position que se va actualizar
        "name": request.form["name"],
        "description" : request.form["description"],
        "organization_id": session['org_id']
    }
    vista = Position.update(data)
    print('DEVOLUCIÓN DEL UPDATE:', vista)

    return redirect(f'/orgs/jobss/new/{request.form["id"]}')



# ===================================== AGREGA LOS SKILLS DE LA POSITION =====================================
@app.route('/five_skill_of_position/<int:skill_id>/<string:name_skill>/<int:position_id>')
def five_skill_of_position(skill_id,name_skill,position_id):

    organization_id = session['org_id']
    
    if 'org_id' not in session: # Compruebo que el usuario este logueado para poder guardar el skill, si no esta logueado entonces limpiamos la session
        return redirect('/logout_org')
    data ={
        "id": skill_id,
        "name" : name_skill
    }

    data_skill_of_position={
        "organization_id": organization_id,
        "skill_id": skill_id,
        "position_id": position_id

    }

    # Verifica si existe el 'skill' con el 'skill_id' y 'name_skill'
    verificar = Skill.get_one_skill(data)
    print('VERIFICAR TIENE', verificar)

    # Verifica la cantidad de 'Skill' que tiene el POSITION
    verificarCantidadSkill = Count.getCount_all_Skill_by_position(data_skill_of_position)
    print('VERIFICAR CANTIDAD DE SKILL TIENE', verificarCantidadSkill[0]['count'])

    # Si es que el verificar devuelve None entonces el Skill no existe, por tanto se lanza un mensaje de 'Skill Inexistente'
    if verificar is not None: # Si verificar no esta vacío entonces entra
        if verificarCantidadSkill[0]['count'] < 5: # Si es que la cantidad de Skill del developer es menor a 5 entonces guarda en la base de datos
            Skill_of_position.save(data_skill_of_position)
        else:
            flash("DENEGADO: Máximo 5 Skills", "add_position_redirect") # Si la cantidad de Skill es 5 o mayor a 5 entonces lanza el mensaje
    else:
        flash("Skill Inexistente", "add_position_redirect") # Si el Skill no existe entontonces lanza este mensaje

    return redirect(f'/orgs/jobss/new/{position_id}')



# ===================================== ELIMINA UN SKILL DE LA POSITION =====================================
@app.route('/delete_Skill_position/<int:skill_id>/<string:name_skill>/<int:position_id>')
def delete_Skill_position(skill_id, name_skill,position_id):

    data={
        "organization_id": session['org_id'],
        "skill_id": skill_id,
        "position_id": position_id,

        "id": skill_id,
        "name" : name_skill
    }
    verificar = Skill.get_one_skill(data)
    print('VERIFICAR EN DELETE TIENE', verificar)

    if verificar is not None: # Si verificar no esta vacío entonces entra
        Skill_of_position.destroy(data)
    else:
        flash("Skill Inexistente", "skill_lan")

    return redirect(f'/orgs/jobss/new/{position_id}')

