from django.db import models

# Create your models here.

#Tabla TiposIdentificacion
class TiposIdentificacion(models.Model):
    TipoIdentificacionID = models.AutoField(primary_key=True, editable=False)
    Descripcion = models.CharField(max_length=15)
    Campo_entero = models.IntegerField(null=True)
    Otro_campo = models.CharField(max_length=15, null=True)
    Otro_campo2 = models.CharField(max_length=15, null=False, default='A')
    Campo_entero2 = models.IntegerField(null=True)
    lcdll = models.DateField(null=True)
    lcdll2 = models.DateTimeField(null=True)

    def __str__(self):
        return self.Descripcion