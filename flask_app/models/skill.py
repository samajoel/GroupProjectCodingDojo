# from dojosninjas_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash



class Skill():
    db_name = "DevsOnDeck"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.tipo = data['tipo']
        self.devicon = data['devicon']



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM skills;"
        result =  connectToMySQL(cls.db_name).query_db(query)
        # print('Contenido de result: ',result)
        skills =[]
        for row in result:
            skills.append(cls(row))
        return skills

    @classmethod
    def get_one_skill(cls,data):
        query = "SELECT * FROM skills WHERE skills.id = %(id)s and skills.name = %(name)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if len(result) > 0:
            return result
        else:
            return None

