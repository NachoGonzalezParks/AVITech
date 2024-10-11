from django.contrib.auth.models import User, Group
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'groups']





'''  Para usar solo usr y pass, si maill = No funcionó
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    email = None  # Eliminamos el campo email
'''

'''
from .models import TiposIdentificacion
class TiposIdentificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposIdentificacion
        fields = ['TipoIdentificacionID', 'Descripcion']
'''