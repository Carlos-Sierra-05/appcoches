# database.py
# Gestión de la conexión a la base de datos

import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    """Crea y retorna una conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    Ejecuta una query en la base de datos
    
    Args:
        query: La consulta SQL
        params: Parámetros para la consulta (tupla)
        fetch: Si True, retorna los resultados (SELECT)
    
    Returns:
        Para SELECT: lista de resultados o None
        Para INSERT/UPDATE/DELETE: número de filas afectadas o None
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            connection.commit()
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return {'affected_rows': affected_rows, 'last_id': last_id}
    
    except mysql.connector.Error as err:
        print(f"Error en la consulta: {err}")
        if connection:
            connection.close()
        return None
