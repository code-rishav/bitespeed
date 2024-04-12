from django.db import models
# Create your models here.


class Contact(models.Model):

    class Precedence(models.TextChoices):
        PRIMARY = 'PRIMARY','primary'
        SECONDARY = 'SECONDARY','secondary'


    phoneNumber = models.CharField(max_length=10,db_index=True)
    email = models.EmailField(db_index=True)
    linkedId = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    linkPrecedence = models.CharField(max_length=12,choices=Precedence.choices)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deleteAt = models.DateField(null=True,blank=True)


    


