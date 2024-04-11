# myapp/management/commands/load_dummy_data.py
import json
from django.core.management.base import BaseCommand
from identity.models import Contact  # Import your model

class Command(BaseCommand):
    help = 'Load dummy data from JSON file'

    def handle(self, *args, **options):
        json_file = 'identity/management/commands/data.json'  # Path to your JSON file

        with open(json_file) as f:
            data = json.load(f)

        for item in data:
            email_exist = Contact.objects.filter(email=item['email'])
            phnNo_exist = Contact.objects.filter(phoneNumber=item['phoneNumber'])
            
            if phnNo_exist:
                primary = Contact.objects.filter(
                    phoneNumber=item['phoneNumber']
                ).first()
            elif email_exist:
                primary = Contact.objects.filter(
                    email=item['email'],
                    linkPrecedence=Contact.Precedence.PRIMARY
                ).first()
            
            if phnNo_exist or email_exist:
                Contact.objects.create(
                    email = item['email'],
                    phoneNumber = item['phoneNumber'],
                    linkPrecedence = Contact.Precedence.SECONDARY,
                    linkedId = primary
                )
            else:
                Contact.objects.create(
                    email = item['email'],
                    phoneNumber = item['phoneNumber'],
                    linkPrecedence = Contact.Precedence.PRIMARY,
                )
                
        self.stdout.write(self.style.SUCCESS('Dummy data loaded successfully'))
