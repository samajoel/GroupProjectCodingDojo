# from dojosninjas_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash



class Count():
    db_name = "DevsOnDeck"

    def __init__(self,data):
        self.count = data['count']
    

    # OBSERVACIÓN:
    # lan: language
    # fram: framework


    # Se utiliza para obtener los Skills con tipo 'lan' que sería de los lenguajes
    @classmethod
    def getCountSkill_lang_by_developer(cls,data):
        query = """SELECT COUNT(*) AS count
                    FROM developers
                    LEFT JOIN skills_of_developers
                    ON developers.id = skills_of_developers.developer_id
                    LEFT JOIN skills
                    ON skills_of_developers.skill_id = skills.id
                    WHERE developers.id = %(developer_id)s AND skills.tipo = 'lang';"""
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('EL CONTADOR DE LANG TRAE:======================', result)
        return result
    

    # Se utiliza para obtener los Skills con tipo 'fram' que sería de los frameworks
    @classmethod
    def getCountSkill_fram_by_developer(cls,data):
        query = """SELECT COUNT(*) AS count
                    FROM developers
                    LEFT JOIN skills_of_developers
                    ON developers.id = skills_of_developers.developer_id
                    LEFT JOIN skills
                    ON skills_of_developers.skill_id = skills.id
                    WHERE developers.id = %(developer_id)s AND skills.tipo = 'fram';"""
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('EL CONTADOR DE FRAM TRAE:======================', result)
        return result


    # Se utiliza para obtener todos los Skills de un usuario, sin importar si es de tipo 'lan' o 'fram'
    @classmethod
    def getCount_all_Skill_by_developer(cls,data):
        query = """SELECT COUNT(*) AS count
                    FROM developers
                    JOIN skills_of_developers
                    ON developers.id = skills_of_developers.developer_id
                    JOIN skills
                    ON skills_of_developers.skill_id = skills.id
                    WHERE developers.id = %(developer_id)s;"""
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('EL CONTADOR DE FRAM TRAE:======================', result)
        return result
    

    # Se utiliza para obtener todos los Skills de un Position, sin importar si es de tipo 'lan' o 'fram'
    @classmethod
    def getCount_all_Skill_by_position(cls,data):
        query = """SELECT COUNT(*) AS count
                    FROM positions
                    JOIN skills_of_positions
                    ON positions.id = skills_of_positions.position_id
                    JOIN skills
                    ON skills_of_positions.skill_id = skills.id
                    WHERE positions.id = %(position_id)s AND positions.organization_id = %(organization_id)s;"""
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('EL CONTADOR DE SKILL DE POSITION TRAE:======================', result)
        return result
    