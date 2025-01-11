# Carga de datos iniciales
# Pararse en AppBack (cd ...)
# Ejecutar desde terminal: python cargar_datos_iniciales.py
import os
import sys
import django

# Agregar la ruta del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append('C:/Users/aleja/OneDrive/Documentos/Ale/SistemaGC/AVITech/Prueba5/SGC')

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGC.settings")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "C:\Users\aleja\OneDrive\Documentos\Ale\SistemaGC\AVITech\prueba5\SGC\SGC\sgc.settings")
django.setup()
from django.contrib.auth.models import Group
from AppBack.models import Paises, Provincias, Ciudades, Sexos, TiposIdentificacion, TiposDisciplinas, Disciplinas, EstadosTorneos, EstadosActores, EstadosEquipos, RolesEquipo, Categorias, Divisiones, Fases, Zonas, Fixture, EstadosPartidos, Partidos , TiposIncidencias, TiemposPartidos

def cargar_datos_iniciales():

   # Datos iniciales para la tabla Auth_group (Grupos)
    grupos_data = [
        {"name": "Administrador de torneo"},
        {"name": "Coadministrador"},
        {"name": "Jugador"},
        {"name": "Delegado"},
        {"name": "Arbitro"},
    ]
    for grupo in grupos_data:
        Group.objects.update_or_create(name=grupo["name"])

    # Datos iniciales para la tabla Paises
    paises_data = [
        {"PaisID": 1, "Nombre": "Argentina"},
        {"PaisID": 2, "Nombre": "Brasil"},
        {"PaisID": 3, "Nombre": "Uruguay"},
        {"PaisID": 4, "Nombre": "Otro"},
    ]

    for pais in paises_data:
        Paises.objects.get_or_create(PaisID=pais["PaisID"], defaults={"Nombre": pais["Nombre"]})

    # Datos iniciales para la tabla Provincias
    provincias_data = [
        {"ProvinciaID": 1, "Nombre": "Capital Federal", "PaisID": 1},
        {"ProvinciaID": 2, "Nombre": "Buenos Aires", "PaisID": 1},
        {"ProvinciaID": 3, "Nombre": "Córdoba", "PaisID": 1},
        {"ProvinciaID": 4, "Nombre": "Santa Fe", "PaisID": 1},
        {"ProvinciaID": 5, "Nombre": "Mendoza", "PaisID": 1},
        {"ProvinciaID": 6, "Nombre": "Sao Paulo", "PaisID": 2},
        {"ProvinciaID": 7, "Nombre": "Rio de Janeiro", "PaisID": 2},
        {"ProvinciaID": 8, "Nombre": "Rio Grande do Sul", "PaisID": 2},
        {"ProvinciaID": 9, "Nombre": "Minas Gerais", "PaisID": 2},
        {"ProvinciaID": 10, "Nombre": "Montevideo", "PaisID": 3},
        {"ProvinciaID": 11, "Nombre": "Otro", "PaisID": 4},
    ]

    for provincia in provincias_data:
        pais = Paises.objects.get(PaisID=provincia["PaisID"])
        Provincias.objects.get_or_create(
            ProvinciaID=provincia["ProvinciaID"],
            defaults={"Nombre": provincia["Nombre"], "PaisID": pais},
        )

    # Datos iniciales para la tabla Ciudades
    ciudades_data = [
        {"CiudadID": 1, "Nombre": "Capital Federal", "ProvinciaID": 1},
        {"CiudadID": 2, "Nombre": "La Plata", "ProvinciaID": 2},
        {"CiudadID": 3, "Nombre": "Avellaneda", "ProvinciaID": 2},
        {"CiudadID": 4, "Nombre": "Tigre", "ProvinciaID": 2},
        {"CiudadID": 5, "Nombre": "Mar del Plata", "ProvinciaID": 2},
        {"CiudadID": 6, "Nombre": "Córdoba", "ProvinciaID": 3},
        {"CiudadID": 7, "Nombre": "Río Cuarto", "ProvinciaID": 3},
        {"CiudadID": 8, "Nombre": "Villa María", "ProvinciaID": 3},
        {"CiudadID": 9, "Nombre": "San Francisco", "ProvinciaID": 3},
        {"CiudadID": 10, "Nombre": "Rosario", "ProvinciaID": 4},
        {"CiudadID": 11, "Nombre": "Santa Fe", "ProvinciaID": 4},
        {"CiudadID": 12, "Nombre": "Rafaela", "ProvinciaID": 4},
        {"CiudadID": 13, "Nombre": "Mendoza", "ProvinciaID": 5},
        {"CiudadID": 14, "Nombre": "San Rafael", "ProvinciaID": 5},
        {"CiudadID": 15, "Nombre": "Sao Paulo", "ProvinciaID": 6},
        {"CiudadID": 16, "Nombre": "Santos", "ProvinciaID": 6},
        {"CiudadID": 17, "Nombre": "Rio de Janeiro", "ProvinciaID": 7},
        {"CiudadID": 18, "Nombre": "Porto Alegre", "ProvinciaID": 8},
        {"CiudadID": 19, "Nombre": "Belo Horizonte", "ProvinciaID": 9},
        {"CiudadID": 20, "Nombre": "Montevideo", "ProvinciaID": 10},
        {"CiudadID": 21, "Nombre": "Otro", "ProvinciaID": 11},
    ]

    for ciudad in ciudades_data:
        provincia = Provincias.objects.get(ProvinciaID=ciudad["ProvinciaID"])
        Ciudades.objects.get_or_create(
            CiudadID=ciudad["CiudadID"],
            defaults={"Nombre": ciudad["Nombre"], "ProvinciaID": provincia},
        )

    # Datos iniciales para la tabla tipos_identificacion
    tipos_identificacion_data = [
        {"TipoIdentificacionID": 1, "Codigo": "DNI", "Descripcion": "Documento nacional de identidad argentino", "PaisID_id": 1},
        {"TipoIdentificacionID": 2, "Codigo": "PASAPORTE", "Descripcion": "Pasaporte argentino", "PaisID_id": 1},
        {"TipoIdentificacionID": 3, "Codigo": "OTRO", "Descripcion": "Otra Identificación", "PaisID_id": 1},
        {"TipoIdentificacionID": 4, "Codigo": "CPF", "Descripcion": "Cadastro de Pessoas Físicas", "PaisID_id": 2},
        {"TipoIdentificacionID": 5, "Codigo": "RG", "Descripcion": "Registro Geral", "PaisID_id": 2},
        {"TipoIdentificacionID": 6, "Codigo": "PASSAPORTE", "Descripcion": "Pasaporte brasilero", "PaisID_id": 2},
        {"TipoIdentificacionID": 7, "Codigo": "OUTRO", "Descripcion": "Outro ID", "PaisID_id": 2},
        {"TipoIdentificacionID": 8, "Codigo": "DNI", "Descripcion": "Documento nacional de identidad digital uruguayo", "PaisID_id": 3},
        {"TipoIdentificacionID": 9, "Codigo": "PASAPORTE", "Descripcion": "Pasaporte uruguayo", "PaisID_id": 3},
        {"TipoIdentificacionID": 10, "Codigo": "OTRO", "Descripcion": "Otra Identificación", "PaisID_id": 3},
        {"TipoIdentificacionID": 11, "Codigo": "OTRO", "Descripcion": "Identificación genérica", "PaisID_id": 4},
    ]
    for tipo in tipos_identificacion_data:
        TiposIdentificacion.objects.update_or_create(TipoIdentificacionID=tipo["TipoIdentificacionID"], defaults=tipo)

    # Datos iniciales para la tabla Sexos
    sexos_data = [
        {"SexoID": 1, "Nombre": "Masculino"},
        {"SexoID": 2, "Nombre": "Femenino"},
        {"SexoID": 3, "Nombre": "Otro"},
    ]
    for sexo in sexos_data:
        Sexos.objects.update_or_create(SexoID=sexo["SexoID"], defaults=sexo)

    # Datos iniciales para la tabla TiposDisciplinas
    tipos_disciplinas_data = [
        {"TipoDisciplinaID": 1, "Nombre": "Masculina grupal"},
        {"TipoDisciplinaID": 2, "Nombre": "Femenina grupal"},
        {"TipoDisciplinaID": 3, "Nombre": "Mixta"},
        {"TipoDisciplinaID": 4, "Nombre": "Masculina individual"},
        {"TipoDisciplinaID": 5, "Nombre": "Femenina individual"},
    ]
    for tipo in tipos_disciplinas_data:
        TiposDisciplinas.objects.update_or_create(TipoDisciplinaID=tipo["TipoDisciplinaID"], defaults=tipo)

    # Datos iniciales para la tabla Disciplinas
    disciplinas_data = [
        {"DisciplinaID": 1, "Nombre": "Futbol 11", "TipoDisciplinaID_id": 1},
        {"DisciplinaID": 2, "Nombre": "Futbol 11", "TipoDisciplinaID_id": 2},
        {"DisciplinaID": 3, "Nombre": "Futbol 11", "TipoDisciplinaID_id": 3},
        {"DisciplinaID": 4, "Nombre": "Futbol 7", "TipoDisciplinaID_id": 1},
        {"DisciplinaID": 5, "Nombre": "Futbol 7", "TipoDisciplinaID_id": 2},
        {"DisciplinaID": 6, "Nombre": "Futbol 7", "TipoDisciplinaID_id": 3},
        {"DisciplinaID": 7, "Nombre": "Futbol 5", "TipoDisciplinaID_id": 1},
        {"DisciplinaID": 8, "Nombre": "Futbol 5", "TipoDisciplinaID_id": 2},
        {"DisciplinaID": 9, "Nombre": "Futbol 5", "TipoDisciplinaID_id": 3},
        {"DisciplinaID": 10, "Nombre": "Basket", "TipoDisciplinaID_id": 1},
        {"DisciplinaID": 11, "Nombre": "Basket", "TipoDisciplinaID_id": 2},
        {"DisciplinaID": 12, "Nombre": "Basket", "TipoDisciplinaID_id": 3},
        {"DisciplinaID": 13, "Nombre": "Voley", "TipoDisciplinaID_id": 1},
        {"DisciplinaID": 14, "Nombre": "Voley", "TipoDisciplinaID_id": 2},
        {"DisciplinaID": 15, "Nombre": "Voley", "TipoDisciplinaID_id": 3},
        {"DisciplinaID": 16, "Nombre": "Tenis", "TipoDisciplinaID_id": 4},
        {"DisciplinaID": 17, "Nombre": "Tenis", "TipoDisciplinaID_id": 5},
    ]
    for disciplina in disciplinas_data:
        Disciplinas.objects.update_or_create(DisciplinaID=disciplina["DisciplinaID"], defaults=disciplina)

    # Datos iniciales para la tabla EstadosTorneos
    estados_torneos_data = [
        {"EstadoTorneoID": 1, "Nombre": "Iniciado"},
        {"EstadoTorneoID": 2, "Nombre": "Finalizado"},
        {"EstadoTorneoID": 3, "Nombre": "Sin comenzar"},
        {"EstadoTorneoID": 4, "Nombre": "Incompleto"},
    ]
    for estado in estados_torneos_data:
        EstadosTorneos.objects.update_or_create(EstadoTorneoID=estado["EstadoTorneoID"], defaults=estado)

    # Datos iniciales para la tablaEstadosActores
    estados_actores_data = [
        {"EstadoActorID": 1, "Nombre": "Activo"},
        {"EstadoActorID": 2, "Nombre": "Inactivo"},
        {"EstadoActorID": 3, "Nombre": "Suspendido"},
    ]
    for estado in estados_actores_data:
        EstadosActores.objects.update_or_create(EstadoActorID=estado["EstadoActorID"], defaults=estado)

    # Datos iniciales para la tabla EstadosEquipos
    estados_equipos_data = [
        {"EstadoEquipoID": 1, "Nombre": "Activo"},
        {"EstadoEquipoID": 2, "Nombre": "Inactivo"},
        {"EstadoEquipoID": 3, "Nombre": "Suspendido"},
    ]
    for estado in estados_equipos_data:
        EstadosEquipos.objects.update_or_create(EstadoEquipoID=estado["EstadoEquipoID"], defaults=estado)

    # Datos iniciales para la tabla RolesEquipo
    roles_equipo_data = [
        {"RolID": 1, "Nombre": "Jugador de campo"},
        {"RolID": 2, "Nombre": "Arquero"},
        {"RolID": 3, "Nombre": "Técnico"},
        {"RolID": 4, "Nombre": "Otro"},
    ]
    for rol in roles_equipo_data:
        RolesEquipo.objects.update_or_create(RolID=rol["RolID"], defaults=rol)

    # Datos iniciales para la tablaCategorias
    categorias_data = [
        {"CategoriaID": 1, "Nombre": "Libre"},
        {"CategoriaID": 2, "Nombre": "Sub 17"},
        {"CategoriaID": 3, "Nombre": "Sub 20"},
        {"CategoriaID": 4, "Nombre": "Sub 23"},
        {"CategoriaID": 5, "Nombre": "+30"},
        {"CategoriaID": 6, "Nombre": "+40"},
        {"CategoriaID": 7, "Nombre": "+50"},
    ]
    for categoria in categorias_data:
        Categorias.objects.update_or_create(CategoriaID=categoria["CategoriaID"], defaults=categoria)

    # Datos iniciales para la tabla Divisiones
    divisiones_data = [
        {"DivisionID": 1, "Nombre": "Única"},
        {"DivisionID": 2, "Nombre": "A"},
        {"DivisionID": 3, "Nombre": "B"},
        {"DivisionID": 4, "Nombre": "C"},
        {"DivisionID": 5, "Nombre": "D"},
    ]
    for division in divisiones_data:
        Divisiones.objects.update_or_create(DivisionID=division["DivisionID"], defaults=division)

    # Datos iniciales para la tabla Fases
    fases_data = [
        {"FaseID": i, "Nombre": nombre}
        for i, nombre in enumerate(
            [
                "Fase única", "Fase de grupos 1", "Fase de grupos 2", "Fase de grupos 3",
                "Fase de grupos única", "32avos de final", "16avos de final", "Octavos de final",
                "Cuartos de final", "Semi final", "Final", "Primera rueda", "Segunda rueda"
            ],
            start=1
        )
    ]
    for fase in fases_data:
        Fases.objects.update_or_create(FaseID=fase["FaseID"], defaults=fase)

    # Datos iniciales para la tabla Zonas
    zonas_data = [
        {"ZonaID": i, "Nombre": nombre}
        for i, nombre in enumerate(
            [
                "Zona única", "Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4", "Grupo 5", "Grupo 6",
                "Grupo 7", "Grupo 8", "Grupo A", "Grupo B", "Grupo C", "Grupo D", "Grupo E",
                "Grupo F", "Grupo G", "Grupo H"
            ],
            start=1
        )
    ]
    for zona in zonas_data:
        Zonas.objects.update_or_create(ZonaID=zona["ZonaID"], defaults=zona)

    # Datos iniciales para la tabla EstadosPartidos
    estados_partidos_data = [
        {"EstadoPartidoID": i, "Nombre": nombre}
        for i, nombre in enumerate(["Jugado", "Programado", "Suspendido"], start=1)
    ]
    for estado in estados_partidos_data:
        EstadosPartidos.objects.update_or_create(EstadoPartidoID=estado["EstadoPartidoID"], defaults=estado)

    # Datos iniciales para la tabla TiposIncidencias
    tipos_incidencias_data = [
        {"TipoIncidenciaID": 1, "Nombre": "Gol", "ValorTanteador": 1},
        {"TipoIncidenciaID": 2, "Nombre": "Gol en contra", "ValorTanteador": -1},
        {"TipoIncidenciaID": 3, "Nombre": "Amonestacón", "ValorTanteador": 0},
        {"TipoIncidenciaID": 4, "Nombre": "Expulsión", "ValorTanteador": 0},        
        {"TipoIncidenciaID": 5, "Nombre": "Suspensión", "ValorTanteador": 0},
    ]
    for tipo in tipos_incidencias_data:
        TiposIncidencias.objects.update_or_create(TipoIncidenciaID=tipo["TipoIncidenciaID"], defaults=tipo)

   # Datos iniciales para la tabla TiemposPartidos  
    tiempos_data = [
        {"TiempoPartidoID": 1, "Nombre": "Primer tiempo", "MinutosDuracion": 90},
        {"TiempoPartidoID": 2, "Nombre": "Segundo tiempo", "MinutosDuracion": 90},
        {"TiempoPartidoID": 3, "Nombre": "Primer suplementario", "MinutosDuracion": 15},
        {"TiempoPartidoID": 4, "Nombre": "Segundo Suplementario", "MinutosDuracion": 15},        
        {"TiempoPartidoID": 5, "Nombre": "Definición por penales", "MinutosDuracion": 0},
        {"TiempoPartidoID": 6, "Nombre": "Suplementario (único)", "MinutosDuracion": 0},
        {"TiempoPartidoID": 7, "Nombre": "Suplementario gol de oro", "MinutosDuracion": 0},
        {"TiempoPartidoID": 8, "Nombre": "Otro", "MinutosDuracion": 0},
    ]
    for tiempos in tiempos_data:
        TiemposPartidos.objects.update_or_create(TiempoPartidoID=tiempos["TiempoPartidoID"], defaults=tiempos)

    print("Datos iniciales cargados exitosamente.")





if __name__ == "__main__":
    cargar_datos_iniciales()

