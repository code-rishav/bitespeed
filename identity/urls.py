from django.urls import path,include
from rest_framework import routers

from .views import ContactViewSet

routers = routers.DefaultRouter()
routers.register(r'identify',ContactViewSet,basename='contacts')

urlpatterns = [
    path('',include(routers.urls))
]