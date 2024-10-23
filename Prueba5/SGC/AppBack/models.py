from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Tabla TiposIdentificacion
class TiposIdentificacion(models.Model):
    TipoIdentificacionID = models.AutoField(primary_key=True, editable=False)
    Codigo = models.CharField(max_length=10, default='Otro')
    Descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.Descripcion
    
class Personas(models.Model):
    UserID = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación 1 a 1 con el usuario 
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    Alias = models.CharField(max_length=50)
    TipoIdentificacionID = models.ForeignKey(TiposIdentificacion, on_delete=models.PROTECT)
    NroIdentificacion = models.CharField(max_length=20)
    FechaNacimiento = models.DateField()
    Telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.Nombre} {self.Alias} {self.Apellido} "
