from django import forms
from .models import TiposIdentificacion

class TipoIdentificacionForm(forms.ModelForm):
    class Meta:
        model = TiposIdentificacion
        fields = ['Descripcion']