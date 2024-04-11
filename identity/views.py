from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Contact
from .serializer import ContactSerializer,IdentitySerializer
from base.query import execute

from rest_framework.response import Response

class ContactViewSet(viewsets.ViewSet):

    def list(self,request):
        try:
            queryset = Contact.objects.all()
            serializer = IdentitySerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'something went wrong'},status=status.HTTP_204_NO_CONTENT)

    
    def create(self,request):
            data = request.data

            email = data['email']
            phnNo = data['phonenumber']

            email_exist = Contact.objects.filter(email=email).exists()
            phnNo_exist = Contact.objects.filter(phoneNumber=phnNo).exists()


            if phnNo_exist:
                print(Contact.objects.filter(phoneNumber=phnNo))
                primary = Contact.objects.filter(
                    phoneNumber=phnNo
                ).first()
            elif email_exist:
                primary = Contact.objects.filter(
                    email=email,
                ).first()
            if (phnNo_exist or email_exist) and primary:
                if primary.linkPrecedence == Contact.Precedence.PRIMARY:
                    Contact.objects.create(
                    email = email,  
                    phoneNumber = phnNo,
                    linkPrecedence = Contact.Precedence.SECONDARY,
                    linkedId = primary
                )
                else:
                    primary = primary.linkedId
                    Contact.objects.create(
                    email = email,
                    phoneNumber = phnNo,
                    linkPrecedence = Contact.Precedence.SECONDARY,
                    linkedId = primary
                    )
                
            else:
                primary = Contact.objects.create(
                    email = email,
                    phoneNumber = phnNo,
                    linkPrecedence = Contact.Precedence.PRIMARY,
                )

            query = 'SELECT id,email,phoneNumber FROM identity_contact where linkedId_id=%s'
            params = [primary.id]
            related_records = execute(query,params)


            emails = list()
            contactNumbers = list()
            secondaryContactIds = list()

            emails.append(primary.email)
            contactNumbers.append(primary.phoneNumber)
            

            for r in related_records:
                secondaryContactIds.append(r[0])
                if r[1] not in emails:
                    print(r[1])
                    emails.append(r[1])
                if r[2] not in contactNumbers:
                    contactNumbers.append(r[2])

            data = {
                'primarycontactId':primary.pk,
                'emails':emails,
                'phoneNumbers':contactNumbers,
                'secondaryContactIds':secondaryContactIds
            }

            serializer = ContactSerializer(data=data,many=False)

            if serializer.is_valid():
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)