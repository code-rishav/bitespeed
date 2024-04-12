from rest_framework import serializers
from .models import Contact
from base.query import execute

class ContactSerializer(serializers.ModelSerializer):
    primarycontactId = serializers.IntegerField()
    phoneNumbers = serializers.ListField(child=serializers.CharField())
    secondaryContactIds = serializers.ListField(child=serializers.IntegerField(),allow_null=True,required=False)
    emails = serializers.ListField(child=serializers.EmailField())
    class Meta():
        model = Contact
        fields = ['primarycontactId','phoneNumbers','secondaryContactIds','emails']
        read_only_fields = ['phoneNumbers','secondaryContactIds','emails']

class IdentitySerializer(serializers.ModelSerializer):
    class Meta():
        model = Contact
        fields = '__all__'
        exclude_fields = ['createdAt','updatedAt','deleteAt']

