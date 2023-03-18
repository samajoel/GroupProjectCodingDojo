# from dojosninjas_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash



class Count():
    db_name = "DevsOnDeck"

    def __init__(self,data):
        self.count = data['count']
    


    @classmethod
    def getCountSkill_lang_by_developer(cls,data):
        query = """SELECT COUNT(*) AS count
                    FROM developers
                    LEFT JOIN skills_of_developers
                    ON developers.id = skills_of_developers.developer_id
                    LEFT JOIN skills
                    ON skills_of_developers.skill_id = skills.id
                    WHERE developers.id = 1 AND skills.tipo = 'lang';"""
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('EL CONTADOR TRAE:======================', result)
        return result