from django.db import models
from django.contrib.auth.models import User, Group
#from django.contrib.gis.db import models  # Para datos geográficos


# Tablas relacionadas a la geolocalización
class Paises(models.Model):
    PaisID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.Nombre


class Provincias(models.Model):
    ProvinciaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)
    PaisID = models.ForeignKey(Paises, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre


class Ciudades(models.Model):
    CiudadID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)
    ProvinciaID = models.ForeignKey(Provincias, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre


class Direcciones(models.Model):
    DireccionID = models.AutoField(primary_key=True)
    Calle = models.CharField(max_length=255)
    Numero = models.CharField(max_length=50, null=True, blank=True)
    Piso = models.CharField(max_length=10, null=True, blank=True)
    Departamento = models.CharField(max_length=10, null=True, blank=True)
    CiudadID = models.ForeignKey(Ciudades, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Calle}, {self.Numero}, {self.CiudadID}"


# Tabla para sexos
class Sexos(models.Model):
    SexoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


# Modificación de TiposIdentificacion
class TiposIdentificacion(models.Model):
    TipoIdentificacionID = models.AutoField(primary_key=True, editable=False)
    Codigo = models.CharField(max_length=10, default='Otro')
    Descripcion = models.CharField(max_length=25)
    PaisID = models.ForeignKey(Paises, on_delete=models.PROTECT, null=True, blank=True) # cambiar null=True, blank=True por default=1 (o el que corresponda) luego de agregar datos

    def __str__(self):
        return self.Descripcion


# Modificación de Personas
class Personas(models.Model):
    UserID = models.OneToOneField(User, on_delete=models.CASCADE)
    #Nombre = models.CharField(max_length=100)    # usamos la de auth_user (First_name)
    #Apellido = models.CharField(max_length=100)  # usamos la de auth_user (Last_name)
    Alias = models.CharField(max_length=50)
    TipoIdentificacionID = models.ForeignKey(TiposIdentificacion, on_delete=models.PROTECT)
    NroIdentificacion = models.CharField(max_length=20)
    FechaNacimiento = models.DateField()
    Telefono = models.CharField(max_length=20)
    SexoID = models.ForeignKey(Sexos, on_delete=models.PROTECT, null=True, blank=True) # cambiar null=True, blank=True por default=1 (o el que corresponda) luego de agregar datos

    def __str__(self):
        return f"{self.Nombre} {self.Alias} {self.Apellido}"

# Tipos disciplinas (Masculina, femenino, mixto...)
class TiposDisciplinas(models.Model):
    TipoDisciplinaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)    

    def __str__(self):
        return self.Nombre

# Tabla de disciplinas
class Disciplinas(models.Model):
    DisciplinaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    TipoDisciplinaID = models.ForeignKey(TiposDisciplinas, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.Nombre


# Tabla de canchas
class Canchas(models.Model):
    CanchaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    #Geolocalizacion = models.PointField()  # Tipo de dato geográfico
    CiudadID = models.ForeignKey(Ciudades, on_delete=models.PROTECT)
    DisciplinaID = models.ForeignKey(Disciplinas, on_delete=models.PROTECT)
    DireccionID = models.ForeignKey(Direcciones, on_delete=models.PROTECT)

    def __str__(self):
        return self.Nombre


# Otras tablas relacionadas
class Categorias(models.Model):
    CategoriaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


class Divisiones(models.Model):
    DivisionID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


class EstadosEquipos(models.Model):
    EstadoEquipoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.Nombre


class EstadosActores(models.Model):    # Activo, inactivo, suspendido...
    EstadoActorID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.Nombre


class EstadosTorneos(models.Model):   # Iniciado, Terminado, Preparado Sin comenzar, Incompleto...
    EstadoTorneoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.Nombre



class Torneos(models.Model):
    TorneoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    CiudadID = models.ForeignKey(Ciudades, on_delete=models.PROTECT)
    Logo = models.ImageField(upload_to='torneos/', null=True, blank=True)
    Edicion = models.IntegerField()
    DisciplinaID = models.ForeignKey(Disciplinas, on_delete=models.PROTECT)
    CategoriaID = models.ForeignKey(Categorias, on_delete=models.PROTECT)
    Tipo = models.CharField(max_length=255)
    FechaInicio = models.DateField()
    FechaFin = models.DateField()
    TipoPuntuacion = models.CharField(max_length=255)
    DuracionPartido = models.IntegerField()
    CantidadTiempos = models.IntegerField()
    DuracionEntretiempo = models.IntegerField()
    EstadoTorneoID = models.ForeignKey(EstadosTorneos, on_delete=models.PROTECT)
    AdministradorID = models.ForeignKey(User, on_delete=models.PROTECT)  # Con auth_User, no con Appback_Personas

    def __str__(self):
        return self.Nombre



class Equipos(models.Model):
    EquipoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    EstadoEquipoID = models.ForeignKey(EstadosEquipos, on_delete=models.PROTECT)
    DisciplinaID = models.ForeignKey(Disciplinas, on_delete=models.PROTECT)
    CategoriaID = models.ForeignKey(Categorias, on_delete=models.PROTECT)
    DivisionID = models.ForeignKey(Divisiones, on_delete=models.PROTECT)

    def __str__(self):
        return self.Nombre

class RolesEquipo(models.Model):    # Roles en principio: jugador ó tecnico
    RolID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
            return self.Nombre

class Jugadores(models.Model):
    JugadorID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.PROTECT) # Con auth_User, no con Appback_Personas
    EquipoID = models.ForeignKey(Equipos, on_delete=models.PROTECT)
    FechaIncorporacion = models.DateField()
    EstadoActorID = models.ForeignKey(EstadosActores, on_delete=models.PROTECT)
    Foto = models.ImageField(upload_to='actores/', null=True, blank=True)    
    Rol = models.ForeignKey(RolesEquipo, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return f"{self.UserID} - {self.EquipoID}"

class SubAdministradores(models.Model):
    SubAdministradorID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.PROTECT) # Con auth_User, no con Appback_Personas
    TorneoID = models.ForeignKey(Torneos, on_delete=models.PROTECT)
    FechaIncorporacion = models.DateField()        

    def __str__(self):
        return f"{self.UserID} - {self.TorneoID}"

class Arbitros(models.Model):
    ArbitroID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.PROTECT) # Con auth_User, no con Appback_Personas
    TorneoID = models.ForeignKey(Torneos, on_delete=models.PROTECT)
    FechaIncorporacion = models.DateField()
    EstadoActorID = models.ForeignKey(EstadosActores, on_delete=models.PROTECT)
    Foto = models.ImageField(upload_to='actores/', null=True, blank=True)

    def __str__(self):
        return f"{self.UserID} - {self.TorneoID}"
    

class Delegados(models.Model):
    DelegadoID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.PROTECT) # Con auth_User, no con Appback_Personas
    EquipoID = models.ForeignKey(Equipos, on_delete=models.PROTECT)
    FechaIncorporacion = models.DateField()
    EstadoActorID = models.ForeignKey(EstadosActores, on_delete=models.PROTECT)
    Foto = models.ImageField(upload_to='actores/', null=True, blank=True)

    def __str__(self):
        return f"{self.UserID} - {self.TorneoID}"    