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

        emails = list()
        phoneNumbers = list()
        secondaryContactIds = list()
        
        if phnNo_exist:
            phn_obj = Contact.objects.filter(
                phoneNumber=phnNo
            ).first()
        if email_exist:
            email_obj = Contact.objects.filter(
                email=email,
            ).first()   

        if phnNo_exist and email_exist:
            #check if the same record has been entered
            if email_obj.id == phn_obj.id:
                return Response({'message':'same record entered'},status=status.HTTP_204_NO_CONTENT)
            #if the record has different email and phone number of different record
            print("if executed")
            if email_obj.linkPrecedence==Contact.Precedence.PRIMARY:
                email_created_time = email_obj.createdAt
            if phn_obj.linkPrecedence==Contact.Precedence.PRIMARY:
                phn_created_time = phn_obj.createdAt
            
            if email_created_time<phn_created_time:
                phn_obj.linkPrecedence = Contact.Precedence.SECONDARY
                phn_obj.linkedId = email_obj
                phn_obj.save()
                primary = email_obj
            else:
                email_obj.linkPrecedence = Contact.Precedence.SECONDARY
                email_obj.linkedId = phn_obj          
                email_obj.save()
                primary = phn_obj  

        elif phnNo_exist or email_exist:
            if phnNo_exist:
                primary = phn_obj
            else:
                primary = email_obj

            print("elif executed")
            if primary.linkPrecedence == Contact.Precedence.PRIMARY:
                created_object = Contact.objects.create(
                email = email,  
                phoneNumber = phnNo,
                linkPrecedence = Contact.Precedence.SECONDARY,
                linkedId = primary
                )
            else:
                print("else executed")
                created_object = Contact.objects.create(
                email = email,
                phoneNumber = phnNo,
                linkPrecedence = Contact.Precedence.SECONDARY,
                linkedId = primary.linkedId
                )
                primary = primary.linkedId
            
        #for new record with unrelated phone number or email    
        else:
            primary = Contact.objects.create(
                email = email,
                phoneNumber = phnNo,
                linkPrecedence = Contact.Precedence.PRIMARY,
            )

        emails.append(primary.email)
        phoneNumbers.append(primary.phoneNumber)

        related_objects = Contact.objects.filter(linkedId=primary.id)

        if related_objects:
            for r in related_objects:
                secondaryContactIds.append(r.id)
                print(r.id)
                if r.email not in emails:
                    emails.append(r.email)
                if r.phoneNumber not in phoneNumbers:
                    phoneNumbers.append(r.phoneNumber)
        
        data = {
            'primarycontactId':primary.id,
            'phoneNumbers':phoneNumbers,
            'emails':emails,
            'secondaryContactIds':secondaryContactIds
        }

        serializer = ContactSerializer(data=data)

        if serializer.is_valid():
            return Response({'contact':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)