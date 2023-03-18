# from dojosninjas_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash



class Skill_of_developer():
    db_name = "DevsOnDeck"

    def __init__(self,data):
        self.developer_id = data['developer_id']
        self.skill_id = data['skill_id']


    @classmethod
    def save(cls,data):
        query = """INSERT INTO skills_of_developers (developer_id, skill_id)
                    VALUES (%(developer_id)s, %(skill_id)s)"""
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM skills_of_developers;"
        result =  connectToMySQL(cls.db_name).query_db(query)
        # print('Contenido de result: ',result)
        skills =[]
        for row in result:
            skills.append(cls(row))
        return skills
    

    @classmethod
    def destroy(cls,data):
        # print('ESTOY EN EL DESTROY CON DATA:', data)
        query = "DELETE FROM skills_of_developers WHERE developer_id = %(developer_id)s AND skill_id = %(skill_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    '''
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM skills WHERE skills.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        # print('Esto tiene el mostrar en la posición 0:', result[0])
        return cls(result[0])
    '''
