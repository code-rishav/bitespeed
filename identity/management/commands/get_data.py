from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection
from identity.models import Contact
class Command(BaseCommand):
    help = 'execute raw sql query'

    def handle(self, *args: Any, **options: Any):
        # # Your raw SQL query
        # raw_query = "SELECT * FROM identity_contact WHERE email = %s AND linkprecedence=%s"
        
        # # Parameters for the query (optional)
        # params = ['john@example.com','PRIMARY']

        # with connection.cursor() as cursor:
        #     # Execute the raw SQL query
        #     cursor.execute(raw_query, params)

        #     # Fetch results
        #     rows = cursor.fetchall()

        #     # Process the results as needed
        #     for row in rows:
        #         # Do something with each row
        #         self.stdout.write(self.style.SUCCESS(row))
            
        #fetch all related data
        #person = Contact.objects.filter(email='john@example.com').first()
        query = 'SELECT email,phoneNumber from identity_contact where linkedId_id=%s'

        params = [16]

        with connection.cursor() as cursor:
            cursor.execute(query,params)
            rows = cursor.fetchall()
        
        

        for row in rows:
            self.stdout.write(self.style.SUCCESS(row))
        
        print(connection.queries)

