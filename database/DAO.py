from database.DB_connect import DBConnect
from model.business import Business


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_cities():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct b.city from business b order by b.city """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["city"])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_nodes(city):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from business b where b.city = %s """
        cursor.execute(query, (city,))
        result = []
        for row in cursor:
            result.append(Business(**row))
        cursor.close()
        cnx.close()
        return result
