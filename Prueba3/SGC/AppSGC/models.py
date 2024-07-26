from django.db import models

# Create your models here.


#Tabla TiposIdentificacion
class TiposIdentificacion(models.Model):
    TipoIdentificacionID = models.AutoField(primary_key=True, editable=False)
    Descripcion = models.CharField(max_length=15)    

    def __str__(self):
        return self.Descripcion
   
# Tabla Personas
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
        return f"{self.Nombre} {self.Apellido} {self.Alias}"

'''
# Tabla Usuarios
class Usuarios(models.Model):
    UsuarioID = models.AutoField(primary_key=True, editable=False)
    Email = models.EmailField()  # Utilizamos EmailField para el email
    Clave = models.CharField(max_length=100)  # Campo para la contraseña
    Verificado = models.BooleanField(default=False)  # BooleanField para indicar si está Verificado
    PersonaID = models.ForeignKey(Personas, on_delete=models.CASCADE)  # ForeignKey para la relación con Personas

    def __str__(self):
        return self.Email
'''