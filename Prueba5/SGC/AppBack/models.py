from django.db import models

# Create your models here.

#Tabla TiposIdentificacion
class TiposIdentificacion(models.Model):
    TipoIdentificacionID = models.AutoField(primary_key=True, editable=False)
    Codigo = models.CharField(max_length=10)
    Descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.Descripcion
    
class Personas(models.Model):
    PersonaID = models.AutoField(primary_key=True, editable=False)
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    Alias = models.CharField(max_length=50)
    TipoIdentificacionID = models.ForeignKey(TiposIdentificacion, on_delete=models.PROTECT)
    NroIdentificacion = models.CharField(max_length=20)
    FechaNacimiento = models.DateField()
    Telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.Nombre} {self.Alias} {self.Apellido} "
