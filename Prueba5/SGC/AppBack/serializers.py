from rest_framework import serializers
from .models import TiposIdentificacion

class TiposIdentificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposIdentificacion
        fields = ['TipoIdentificacionID', 'Descripcion']
