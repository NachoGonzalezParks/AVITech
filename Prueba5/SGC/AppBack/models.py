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
    Descripcion = models.CharField(max_length=50)
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
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Nombre} {self.Alias} {self.Apellido} "


class LoginPersona(models.Model):
    id = models.IntegerField(primary_key=True) 
    mail = models.EmailField(unique=True, max_length=255) 

    def __str__(self):
        return self.mail

    # class Meta:
    #     db_table = 'login_personas' 
    #     verbose_name = 'Persona Login'
    #     verbose_name_plural = 'Personas Login'
    #     return f"{self.Nombre} {self.Alias} {self.Apellido}"


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
    

class Fases(models.Model):
    FaseID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


class Zonas(models.Model):
    ZonaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


class Fixture(models.Model):
    FixtureID = models.AutoField(primary_key=True)
    TorneoID = models.ForeignKey(Torneos, on_delete=models.PROTECT)
    FaseID = models.ForeignKey(Fases, on_delete=models.PROTECT)
    ZonaID = models.ForeignKey(Zonas, on_delete=models.PROTECT)
    FechaNumero = models.IntegerField() # Nro de Fecha dentro del fixture 
    FechaDesde = models.DateField() # Período previsto en que se juega la fecha nro x
    FechaHasta = models.DateField() # Período previsto en que se juega la fecha nro x

    def __str__(self):
        return f"Fixture {self.FixtureID}"


class EstadosPartidos(models.Model):
    EstadoPartidoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre


class Partidos(models.Model):
    PartidoID = models.AutoField(primary_key=True)
    FixtureID = models.ForeignKey(Fixture, on_delete=models.PROTECT)
    FechaPartido = models.DateField()  # Fecha programada o de juego efectivo del partido
    EquipoLocalID = models.ForeignKey(
        Equipos, 
        on_delete=models.PROTECT, 
        related_name='partidos_locales'  # Accesor para partidos donde este equipo es local
    )
    EquipoVisitanteID = models.ForeignKey(
        Equipos, 
        on_delete=models.PROTECT, 
        related_name='partidos_visitantes'  # Accesor para partidos donde este equipo es visitante
    )
    GolesLocal = models.IntegerField(null=True, blank=True)
    GolesVisitante = models.IntegerField(null=True, blank=True)
    EstadoPartidoID = models.ForeignKey(EstadosPartidos, on_delete=models.PROTECT)
    '''
    Para Obtener todos los partidos donde un equipo es local (Ej equipo 1 )
    equipo = Equipos.objects.get(pk=1)
    partidos_como_local = equipo.partidos_locales.all()    
    '''

    def __str__(self):
        return f"Partido {self.PartidoID}"


class JugadoresxPartidos(models.Model):
    JugadorxPartidoID = models.AutoField(primary_key=True)
    PartidoID = models.ForeignKey(Partidos, on_delete=models.PROTECT)
    JugadorID = models.ForeignKey(Jugadores, on_delete=models.PROTECT)
    EquipoID = models.ForeignKey(Equipos, on_delete=models.PROTECT)
    Titular = models.BooleanField
    
    def __str__(self):
        return f"Partido {self.JugadorxPartidoID}"  


class TiposIncidencias(models.Model):   # Gol, Gol en contra, Amonestación, Expulsión, Suspensión...
    TipoIncidenciaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    ValorTanteador = models.IntegerField(null=True)

    def __str__(self):
        return self.Nombre


class IncidenciasGenerales(models.Model):   
    IncidenciaGeneralID = models.AutoField(primary_key=True)
    PartidoID = models.ForeignKey(Partidos, on_delete=models.PROTECT)
    TipoIncidenciaID = models.ForeignKey(TiposIncidencias, on_delete=models.PROTECT)
    Detalle = models.CharField(max_length=255)

    def __str__(self):
        return f"Incidencia general {self.IncidenciaGeneralID}"  


class TiemposPartidos(models.Model):     # tiempos regulares, suplementarios, penales
    TiempoPartidoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    MinutosDuracion = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.nombre} ({self.nombre} min.) "        


class IncidenciasJugadores(models.Model):     
    IncidenciaJugadorID = models.AutoField(primary_key=True)
    PartidoID = models.ForeignKey(Partidos, on_delete=models.PROTECT)
    JugadorID = models.ForeignKey(Jugadores, on_delete=models.PROTECT)
    TipoIncidenciaID = models.ForeignKey(TiposIncidencias, on_delete=models.PROTECT)
    Minuto = models.IntegerField(null=True)  # 45, 47, 55..
    TiempoPartidoID = models.ForeignKey(TiemposPartidos, on_delete=models.PROTECT) 
    Detalle = models.CharField(max_length=255)

    def __str__(self):
        return f"Incidencia jugador {self.IncidenciaJugadorID}"

'''----------------Falta revisar de aca  para abajo (datos iniciales)------'''

class TablaPosiciones(models.Model):
    TablaPosicionesID = models.AutoField(primary_key=True)
    TorneoID = models.ForeignKey('Torneos', on_delete=models.PROTECT)
    FaseID = models.ForeignKey('Fases', on_delete=models.PROTECT)
    ZonaID = models.ForeignKey('Zonas', on_delete=models.PROTECT)
    EquipoID = models.ForeignKey('Equipos', on_delete=models.PROTECT)
    PartidosJugados = models.IntegerField(default=0)
    Puntos = models.IntegerField(default=0)
    Ganados = models.IntegerField(default=0)
    Empatados = models.IntegerField(default=0)
    Perdidos = models.IntegerField(default=0)
    GolesFavor = models.IntegerField(default=0)
    GolesContra = models.IntegerField(default=0)
    DiferenciaGoles = models.IntegerField(default=0)
    CriterioDesempate = models.CharField(max_length=255, blank=True, null=True)
    PosicionDestacada = models.CharField(max_length=255, blank=True, null=True)

class Suspensiones(models.Model):
    SuspensionID = models.AutoField(primary_key=True)
    EquipoID = models.ForeignKey('Equipos', on_delete=models.PROTECT)
    JugadorID = models.ForeignKey('Jugadores', on_delete=models.PROTECT)
    Fecha = models.DateField()
    FechasSuspension = models.IntegerField(default=0)
    DetalleInforme = models.CharField(max_length=255, blank=True, null=True)

class ReemplazosPartidos(models.Model):
    ReemplazoPartidoID = models.AutoField(primary_key=True)
    PartidoID = models.ForeignKey('Partidos', on_delete=models.PROTECT)
    JugadorEntraID = models.ForeignKey('Jugadores', on_delete=models.PROTECT, related_name='jugador_entra')
    JugadorSaleID = models.ForeignKey('Jugadores', on_delete=models.PROTECT, related_name='jugador_sale')
    MinutoReemplazo = models.IntegerField()

class TiposNotificaciones(models.Model):
    TipoNotificacionID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)

class Notificaciones(models.Model):
    NotificacionID = models.AutoField(primary_key=True)
    TipoNotificacionID = models.ForeignKey('TiposNotificaciones', on_delete=models.PROTECT)
    Generador = models.CharField(max_length=50)
    FechaHoraEvento = models.DateTimeField()
    FechaHoraNotificacion = models.DateTimeField()
    Detalle = models.CharField(max_length=255)

class TiposRespuestasNotificaciones(models.Model):
    TiposRespuestasNotificacionesID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)

class RespuestasNotificaciones(models.Model):
    RespuestaID = models.AutoField(primary_key=True)
    NotificacionID = models.ForeignKey('Notificaciones', on_delete=models.PROTECT)
    DestinatarioID = models.ForeignKey(User, on_delete=models.PROTECT)
    FechaHoraRespuesta = models.DateTimeField()
    TiposRespuestasNotificacionesID = models.ForeignKey('TiposRespuestasNotificaciones', on_delete=models.PROTECT)
    Contenido = models.CharField(max_length=255)

class NotificacionesDestinatarios(models.Model):
    NotificacionID = models.ForeignKey('Notificaciones', on_delete=models.PROTECT)
    DestinatarioID = models.ForeignKey(User, on_delete=models.PROTECT)
    TipoDestinatario = models.CharField(max_length=50)
    class Meta:
        unique_together = ('NotificacionID', 'DestinatarioID', 'TipoDestinatario')

class Anunciantes(models.Model):
    AnuncianteID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)

class Publicidad(models.Model):
    PublicidadID = models.AutoField(primary_key=True)
    Tipo = models.CharField(max_length=50)
    Formato = models.CharField(max_length=50)
    Comportamiento = models.CharField(max_length=50)
    Duracion = models.IntegerField()
    Frecuencia = models.IntegerField()
    Ubicacion = models.CharField(max_length=100)
    Link = models.URLField(max_length=255, blank=True, null=True)
    Objetivo = models.CharField(max_length=100, blank=True, null=True)
    VigenciaDesde = models.DateTimeField()
    VigenciaHasta = models.DateTimeField()
    AnuncianteID = models.ForeignKey('Anunciantes', on_delete=models.PROTECT)

class PublicidadVisualizaciones(models.Model):
    VisualizacionID = models.AutoField(primary_key=True)
    PublicidadID = models.ForeignKey('Publicidad', on_delete=models.PROTECT)
    UsuarioID = models.ForeignKey(User, on_delete=models.PROTECT)
    FechaHoraVisualizacion = models.DateTimeField()
    DuracionSegundos = models.IntegerField(default=0)

class UsuariosTemporales(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    tipo_identificacion = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=50)
    creado_por = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
