from django.db import models

# Create your models here.

#Tabla TiposIdentificacion
class TiposIdentificacion(models.Model):
    TipoIdentificacionID = models.AutoField(primary_key=True, editable=False)
    Descripcion = models.CharField(max_length=15)

    def __str__(self):
        return self.Descripcion