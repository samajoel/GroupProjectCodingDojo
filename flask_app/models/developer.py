# from dojosninjas_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re # El módulo regex
from flask_bcrypt import Bcrypt
from flask_app.models.skill import Skill
bcrypt = Bcrypt(app)     # estamos creando un objeto llamado bcrypt,
                                # que se realiza invocando la función Bcrypt con nuestra aplicación como argumento


# crea un objeto de expresión regular que usaremos más adelante
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')
LETRAS_REGEX = re.compile(r'^[a-zA-Z]+$')

class Developer():
    db_name = "DevsOnDeck"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.github_user = data['github_user']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.short_bio = data['short_bio']
        self.available = data['available']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skills = []

    @classmethod
    def create_developer(cls,data):
        query = """INSERT INTO developers (first_name, last_name, email, github_user, address, city, state, password, short_bio, available, created_at, updated_at)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(github_user)s, %(address)s, %(city)s, %(state)s, %(password)s, Null, %(available)s, NOW(), NOW())"""
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM developers;"
        result =  connectToMySQL(cls.db_name).query_db(query)
        # print('Contenido de result: ',result)
        users =[]
        for row in result:
            users.append(cls(row))
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM developers WHERE developers.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('Esto tiene el get_one:', result[0])
        return cls(result[0])

    @classmethod
    def getEmail(cls, data):
        query = "select * from developers where email = %(email)s;"
        mysql = connectToMySQL(cls.db_name)
        data = {
            'email': data
        }
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def getId(cls, data):
        query = "select * from developers where id = %(id)s;"
        mysql = connectToMySQL(cls.db_name)
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    
    @classmethod
    def get_skill_by_developer(cls, data):
        query = """SELECT first_name, last_name, email, github_user, address, city, state, password, short_bio, available, created_at, updated_at, 
                    skill_id AS id, name, tipo, devicon
                    FROM developers
                    LEFT JOIN skills_of_developers
                    ON developers.id = skills_of_developers.developer_id
                    LEFT JOIN skills
                    ON skills_of_developers.skill_id = skills.id
                    WHERE developers.id = %(id)s;"""
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        print('CONTENIDO de results completo: ', results)
        print('Contenido de results[0]: ',results[0])
        developer = cls(results[0])
        for result in results:
            skill_data = {
                'id': result['id'],
                'name': result['name'],
                'tipo': result['tipo'],
                'devicon': result['devicon']
            }
            
            developer.skills.append(Skill(skill_data))
        print('ESTO tiene DEVELOPER: ', developer)
        return developer


    @classmethod
    def update(cls, data):
        # print('Estoy en el método UPDATE y soy el data: ', data)
        query = """UPDATE developers SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, github_user=%(github_user)s, address=%(address)s, city=%(city)s, state=%(state)s,
                    password=%(password)s, short_bio=%(short_bio)s, available=%(available)s, updated_at = NOW() WHERE id = %(id)s"""
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def update_short_bio(cls, data):
        # print('Estoy en el método UPDATE y soy el data: ', data)
        query = "UPDATE developers SET short_bio=%(short_bio)s, updated_at = NOW() WHERE id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result


    @classmethod
    def destroy(cls,data):
        # print('ESTOY EN EL DESTROY CON DATA:', data)
        query = "DELETE FROM developers WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @staticmethod
    def validate_register(data):

        is_valid = True # asumimos que esto es true
        query = "select * from developers where email = %(email)s;"
        results = connectToMySQL(Developer.db_name).query_db(query,data)

        if len(results) >= 1:
            flash("El email ya esta en uso.", "register")
        if not LETRAS_REGEX.match(data['first_name']): 
            flash("El nombre solo puede tener Letras", "register")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if not LETRAS_REGEX.match(data['last_name']): 
            flash("El apellido solo puede tener Letras", "register")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if len(data['github_user']) < 3:
            flash("El usuario debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Formato de Email incorrecto!", "register")
            is_valid = False
        if len(data['address']) < 8:
            flash("La dirección debe tener al menos 8 caracteres", "register")
            is_valid = False
        if len(data['city']) < 5:
            flash("La ciudad debe tener al menos 5 caracteres", "register")
            is_valid = False
        if data['state'] == 'Select State':
            flash("Debe seleccionar un Estado", "register")
            is_valid = False
        if not PASS_REGEX.match(data['password']): 
            flash("La contraseña debe tener de 8 a 16 caracteres, al menos 1 dígito, al menos 1 minúscula y al menos 1 mayúscula.!", "register")
            is_valid = False    
        if (data['password'] != data['confir_password']):
            flash("Las contraseñas no coinciden", "register")
            is_valid = False
        return is_valid
    
