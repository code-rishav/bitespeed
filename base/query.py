from django.db import connection

def execute(query,params):

    with connection.cursor() as cursor:
        # Execute the raw SQL query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows