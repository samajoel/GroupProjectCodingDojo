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

class Position():
    db_name = "DevsOnDeck"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.organization_id = data['organization_id']
        self.skills = []


    @classmethod
    def create_position(cls,data):
        query = """INSERT INTO positions (name, description, created_at, updated_at, organization_id)
                    VALUES (%(name)s, %(description)s, NOW(), NOW(), %(organization_id)s)"""
        return connectToMySQL(cls.db_name).query_db(query,data)


    # ========================== SIN UTILIZAR AÚN ==========================
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM positions;"
        result =  connectToMySQL(cls.db_name).query_db(query)
        # print('Contenido de result: ',result)
        users =[]
        for row in result:
            users.append(cls(row))
        return users


    # ========================== SIN UTILIZAR AÚN ==========================
    @classmethod
    def get_one_position(cls,data):
        query = "SELECT * FROM positions WHERE positions.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('Esto tiene el get_one en POSITIONS:', result[0])
        return cls(result[0])


    # ========================== SIN UTILIZAR AÚN ==========================
    @classmethod
    def getId(cls, data):
        query = "select * from positions where id = %(id)s;"
        mysql = connectToMySQL(cls.db_name)
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    


    @classmethod
    def getPosition_by_organization(cls, data):
        query = "SELECT * FROM positions where organization_id = %(organization_id)s;"
        mysql = connectToMySQL(cls.db_name)
        result = mysql.query_db(query, data)
        print("RESULT en getPosition_by_organization TRAE:", result)
        print("RESULT en getPosition_by_organization TRAE:", result[0])
        positions =[]
        for position in result:
            positions.append(cls(position))
        print('LA LISTA POSITIONS TIENE:',positions)
        return positions

        '''
        if len(result) > 0:
            return cls(result)
        else:
            return None
        '''
    
    
    @classmethod
    def get_skill_by_position(cls, data):
        query = """SELECT positions.id AS id, positions.name AS name, description, created_at, updated_at, organization_id,
                    skills.id AS skillsID, skills.name AS skillName, tipo, devicon
                    FROM positions
                    LEFT JOIN skills_of_positions
                    ON positions.id = skills_of_positions.position_id
                    LEFT JOIN skills
                    ON skills_of_positions.skill_id = skills.id
                    WHERE positions.id = %(id)s AND positions.organization_id = 1;"""
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        print('CONTENIDO de results completo en get_skill_by_position: ', results)
        if len(results) > 0 :
            print('Contenido de results[0] en get_skill_by_position: ',results[0])
            position = cls(results[0])
            for result in results:
                skill_data = {
                    'id': result['skillsID'],
                    'name': result['skillName'],
                    'tipo': result['tipo'],
                    'devicon': result['devicon']
                }
                
                position.skills.append(Skill(skill_data))
            print('ESTO tiene POSITION: ', position)
            return position
        else:
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
                    'id': None,
                    'name': None,
                    'tipo': None,
                    'devicon': None
                }
                
                developer.skills.append(Skill(skill_data))
            print('ESTO tiene DEVELOPER: ', developer)
            return developer
        

    '''
    @classmethod
    def get_skill_fram_by_developer(cls, data):
        query = """SELECT first_name, last_name, email, github_user, address, city, state, password, short_bio, available, created_at, updated_at, 
                    skill_id AS id, name, tipo, devicon
                    FROM developers
                    LEFT JOIN skills_of_developers
                    ON developers.id = skills_of_developers.developer_id
                    LEFT JOIN skills
                    ON skills_of_developers.skill_id = skills.id
                    WHERE developers.id = %(id)s AND skills.tipo = 'fram';"""

        results =  connectToMySQL(cls.db_name).query_db(query,data)
        print('CONTENIDO de results completo: ', results)
        if len(results) > 0 :
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
        else:
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
                    'id': None,
                    'name': None,
                    'tipo': None,
                    'devicon': None
                }
                
                developer.skills.append(Skill(skill_data))
            print('ESTO tiene DEVELOPER: ', developer)
            return developer
        '''

    # ========================== SIN UTILIZAR AÚN ==========================
    
    @classmethod
    def update(cls, data):
        # print('Estoy en el método UPDATE y soy el data: ', data)
        query = """UPDATE positions SET name=%(name)s, description=%(description)s, updated_at = NOW() WHERE id = %(id)s
        AND positions.organization_id = %(organization_id)s"""
        return connectToMySQL(cls.db_name).query_db(query,data)
    


    # ========================== SIN UTILIZAR AÚN ==========================
    @classmethod
    def destroy(cls,data):
        # print('ESTOY EN EL DESTROY CON DATA:', data)
        query = "DELETE FROM positions WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @staticmethod
    def validate_position(data):

        is_valid = True # asumimos que esto es true

        if len(data['name']) < 5:
            flash("El nombre debe tener al menos 5 caracteres.", "add_position")
            is_valid = False
        if len(data['description']) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "add_position")
            is_valid = False
        return is_valid
    

    @staticmethod
    def validate_position_redirect(data):

        is_valid = True # asumimos que esto es true

        if len(data['name']) < 5:
            flash("El nombre debe tener al menos 5 caracteres.", "add_position_redirect")
            is_valid = False
        if len(data['description']) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "add_position_redirect")
            is_valid = False
        return is_valid
    
