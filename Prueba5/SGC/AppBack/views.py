import requests
from django.conf import settings
from django.db import transaction  # Para asegurar atomicidad
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token     
from rest_framework.exceptions import ValidationError as DRFValidationError   
from allauth.account.models import EmailAddress        
from .models import Personas, TiposIdentificacion, LoginPersona, Sexos, UsuariosTemporales, Paises, equipos, Ciudades, Disciplinas, Categorias, Divisiones, Equipos, Estadosequipos, EstadosEquipos, Jugadores, Delegados                      
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .Tokens import account_activation_token    # Crear un token personalizado para verificación
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from django.views import View
from django.utils.timezone import now
from django.utils.dateparse import parse_date
import logging
import pandas as pd
import re
import json
from io import BytesIO
from datetime import datetime
logger = logging.getLogger(__name__)


@api_view(['POST'])
def listar_paises(request):
    # Esta vista devuleve la lista de paises
    try:
        paises = Paises.objects.all().order_by('PaisID') # Por ahora Ordenado por Id, no por nombre
        if not paises.exists():
            return Response({'error': 'No hay registros de países en la base de datos.'}, status=404)
        
        paises_list = [pais.Nombre for pais in paises]
        return Response({'paises': paises_list}, status=200)
    except Exception as e:
        return Response({'error': f'Ocurrió un error: {str(e)}'}, status=500)
    

@api_view(['POST'])
def listar_tipos_identificacion_por_pais(request):
    # Esta vista devuelve los tipos de identificación del pais elegido. Devuelve el código (DNI, RUF etc., no la descipción larga)
    # Debe recibir el nombre del pais (nombre_pais)
    try:
        nombre_pais = request.data.get('nombre_pais')
        if not nombre_pais:
            return Response({'error': 'El nombre del país es requerido.'}, status=400)
        
        pais = Paises.objects.filter(Nombre=nombre_pais).first()
        if not pais:
            return Response({'error': 'El país especificado no existe en la base de datos.'}, status=404)
        
        tipos_identificacion = TiposIdentificacion.objects.filter(PaisID=pais)
        if not tipos_identificacion.exists():
            return Response({'error': f'No hay tipos de identificación disponibles para el país {nombre_pais}.'}, status=404)
        
        tipos_list = [tipo.Codigo for tipo in tipos_identificacion]
        return Response({'tipos_identificacion': tipos_list}, status=200)
    except Exception as e:
        return Response({'error': f'Ocurrió un error: {str(e)}'}, status=500)


@api_view(['POST'])
def listar_sexos(request):
    # Esta vista devuelve los registros de la tabla Sexos
    try:
        sexos = Sexos.objects.all()
        if not sexos.exists():
            return Response({'error': 'No hay registros de sexos en la base de datos.'}, status=404)
        
        sexos_list = [sexo.Nombre for sexo in sexos]
        return Response({'sexos': sexos_list}, status=200)
    except Exception as e:
        return Response({'error': f'Ocurrió un error: {str(e)}'}, status=500)



@api_view(['POST'])
def email_existe(request):   
    # Esta vista verificar si el email recibido del front ya existe en BD
    # (cuando el usuario ingresa el email con el cual se va a registrar) 
    
    email = request.data.get('email')

    # Verifica si el email ya está en uso
    email_existe = User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists()

    # Devuelve true si el email Existe, false si está Disponible (puede usarlo para registrarse)
    if email_existe:
        return Response({'existe': True}, status=status.HTTP_200_OK)
    else:
        return Response({'existe': False}, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic  
def registro_usuario(request):   
    # Esta vista crea un nuevo usuario y envía el mail de verificación 
    # Debe recibir: email, password1, password2, nombre, apellido, 
    #               pais (del tipo de identificación), tipo_identificacion, numero_identificacion, 
    #               sexo, fecha_nacimiento
    #   opcionales: alias, telefono       
    username = request.data.get('email')
    email = request.data.get('email')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    nombre = request.data.get('nombre')
    apellido = request.data.get('apellido')
    alias = request.data.get('alias')
    pais = request.data.get('pais')
    tipo_identificacion = request.data.get('tipo_identificacion')
    numero_identificacion = request.data.get('numero_identificacion')
    sexo = request.data.get('sexo')
    fecha_nacimiento = request.data.get('fecha_nacimiento')
    telefono = request.data.get('telefono')
    

    try:       
        if password1 != password2:
            return Response({'success': False, 'message': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password1)
        except ValidationError as password_error:
            return Response({'success': False, 'message': f'Contraseña débil: {", ".join(password_error.messages)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not nombre or not apellido:
            return Response({'success': False, 'message': 'El nombre y el apellido no pueden estar vacíos.'}, status=status.HTTP_400_BAD_REQUEST)

        if not numero_identificacion:
            return Response({'success': False, 'message': 'El número de identificación no pueden estar vacío.'}, status=status.HTTP_400_BAD_REQUEST)

        if not fecha_nacimiento:
            return Response({'success': False, 'message': 'La fecha de nacimiento no pueden estar vacía.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'success': False, 'message': 'El formato del email es inválido.'}, status=status.HTTP_400_BAD_REQUEST)
       
      
        user = User.objects.create_user(username=email, email=email, password=password1, last_name=apellido, first_name=nombre)
      
        email_address = EmailAddress.objects.create(
            user=user,
            email=email,
            verified=False,
            primary=True
        )
     
        token = Token.objects.create(user=user)        
        
        codigo_pais = Paises.objects.get(Nombre=pais)
        tipo_identificacion_obj = TiposIdentificacion.objects.get(Codigo=tipo_identificacion, PaisID=codigo_pais)            

        codigo_sexo = Sexos.objects.get(Nombre=sexo)        
    
        persona = Personas.objects.create(
            UserID=user,
            #Nombre=request.data['nombre'],
            #Apellido=request.data['apellido'],
            Alias=alias, #request.data['alias'],
            TipoIdentificacionID=tipo_identificacion_obj,
            NroIdentificacion= numero_identificacion, #request.data['numero_identificacion'],
            SexoID=codigo_sexo,
            FechaNacimiento=fecha_nacimiento, #request.data['fecha_nacimiento'],
            Telefono=telefono #request.data['telefono']
        )

        admin_group = Group.objects.get(name="Administrador de equipo")
        user.groups.add(admin_group)

        # Enviar email para requerir verificación de la cuenta
        enviar_email_enlace(usuario=user, persona=persona, tipo='activacion', request=request) 
        
        #return Response({'success': True, 'message': f'Registro exitoso. Revisa tu correo para confirmar tu cuenta. {message}'}, status=status.HTTP_201_CREATED)
        return Response({'success': True, 'message': f'Registro exitoso. Revisa tu correo para confirmar tu cuenta.'}, status=status.HTTP_201_CREATED)
          
    except Exception as e:
        transaction.set_rollback(True)
        return Response({'success': False, 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def activacion(request, uidb64, token):
    # Esta vista recibe la url de verificación, accedida desde el mail del usuario, y si el link es válido activa la cuenta 
    # pone EmailAddress.verified = True
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        email_address = EmailAddress.objects.get(user=user)
        email_address.verified = True
        email_address.save()
        return Response({'success': True, 'message': 'Cuenta activada correctamente.'}, status=status.HTTP_200_OK)
    else:
        return Response({'success': False, 'message': 'El link de activación es inválido.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_usuario(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'success': False, 'message': 'Nombre de usuario y contraseña son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=username, password=password)

        if user is None:
            raise AuthenticationFailed('Datos incorrectos')

        try:
            email_address = EmailAddress.objects.get(user=user, email=username)

        except ObjectDoesNotExist:
            return Response({'success': False, 'message': 'No se encontró una cuenta asociada a este correo.'}, status=status.HTTP_404_NOT_FOUND)

        if not email_address.verified:
            return Response({'success': False, 'message': 'La cuenta no ha sido verificada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)

        response = get_user_groups(user)

        if 'Administrador' in response.data['groups']:
            # Se marca como False el campo first_login de la tabla Personas
            try:
                persona = Personas.objects.get(user=user)
                persona.first_login = False
                persona.save()
            except ObjectDoesNotExist:
                return Response({'success': False, 'message': 'No se encontró la persona asociada a este usuario.'}, status=status.HTTP_404_NOT_FOUND)

            if verificar_pago(user):
                try:
                    # Loguear usuario
                    marcar_login('loguear', response.data['pk'], response.data['email'])
                except RuntimeError as e:
                    return Response({'success': False, 'message': f'Error al loguear: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response({'success': False, 'message': 'El pago de su cuenta no está completado.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Se comprueba si el campo 'first_login' está marcado como True para los demás roles
            if 'Co Administrador' in response.data['groups'] or 'Delegado' in response.data['groups'] or 'Árbitro' in response.data['groups'] or 'Jugador' in response.data['groups']:
                try:
                    persona = Personas.objects.get(user=user)

                    if persona.first_login:
                        # Cambiar la contraseña (porque al darlo de alta se guardó el DNI o Número de Identificación como contraseña inicial/temporal)
                        new_password = request.data.get('new_password')
                        if not new_password:
                            return Response({'success': False, 'message': 'Se requiere una nueva contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

                        if len(new_password) < 8:
                            return Response({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

                        user.set_password(new_password) 
                        user.save() 

                        persona.first_login = False
                        persona.save()

                        return Response({'success': True, 'message': 'Contraseña cambiada correctamente. Puede proceder a iniciar sesión.'}, status=status.HTTP_200_OK)

                except ObjectDoesNotExist:
                    return Response({'success': False, 'message': 'No se encontró la persona asociada a este usuario.'}, status=status.HTTP_404_NOT_FOUND)

        return response

    except AuthenticationFailed as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist as e:
        return Response({'success': False, 'message': 'No se pudo encontrar el objeto solicitado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'message': f'Ocurrió un error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
def logout_usuario(request):
    try:
        user_id = request.data.get('id')
        email = request.data.get('email')

        if not user_id or not email:
            return Response({'success': False, 'message': 'Se requieren el id y el email del usuario.'}, status=status.HTTP_400_BAD_REQUEST)

        # Llamar a la función marcar_login con la acción "deslogguear"
        deleted = marcar_login('desloguear', user_id, email)

        if deleted:
            return Response({'success': True, 'message': 'Usuario deslogueado correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'El usuario no estaba logueado.'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'success': False, 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_user_groups(user):
    # Esta función devuelve información del usuario (solo tabla auth_user) y los grupos al que pertenece (en formato lista: groups)
    groups = user.groups.all()
    group_names = [group.name for group in groups]
    
    return Response({
        'success': True,
        'message': 'Sesión iniciada correctamente.',
        'pk': user.pk,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,        
        'groups': group_names
    })

def marcar_login(accion, id, email):
    try:
        if accion == 'loguear':
            # Agregar o verificar existencia de la persona
            persona, creada = LoginPersona.objects.get_or_create(id=id, mail=email)
            return creada  # True si la persona fue creada, False si ya existía

        elif accion == 'desloguear':
            # Intentar eliminar el registro
            deleted, _ = LoginPersona.objects.filter(id=id, mail=email).delete()
            return deleted  # Número de filas eliminadas (1 si se eliminó, 0 si no se encontró)

        else:
            raise ValueError("Acción no válida. Usa 'logguear' o 'deslogguear'.")

    except Exception as e:
        raise RuntimeError(f"Error al realizar la acción {accion}: {str(e)}")



@api_view(['POST'])
def mail_password_reset(request):
    # Esta vista recibe un email del front y  envía un link a ese mail para reestablecer la contraseña (Ha olvidado su contraseña?)
    email = request.data.get("email")
    user = get_object_or_404(User, email=email)
    persona = get_object_or_404(Personas, UserID=user)
    #persona = Personas.objects.get()  

    # Enviar correo de restablecimiento de contraseña
    enviar_email_enlace(usuario=user, persona=persona, tipo='reset', request=request)

    return JsonResponse({
        "message": "Se ha enviado un correo para restablecer la contraseña."
    }, status=200)

def enviar_email_enlace(usuario, persona, tipo, request):
    # Esta vista crea un link y lo envía por mail    
    # Sirve para "activacion" y para "reset"

    #Ej. Carpeta Templates = C:\Users\aleja\OneDrive\Documentos\Ale\SistemaGC\AVITech\Prueba5\SGC\templates
    #current_site = get_current_site(request) está seteado en http://localhost:8000/admin/sites
    
    try:
        email = usuario.email
        uid = urlsafe_base64_encode(force_bytes(usuario.pk))
        
        if tipo == 'activacion':
            token = account_activation_token.make_token(usuario)
            subject = 'Activa tu cuenta en Zeus.com'
            template = 'mail_activacion.html'
        elif tipo == 'reset':
            token = default_token_generator.make_token(usuario)
            subject = 'Restablece tu contraseña'
            template = 'mail_reset.html'
        
        domain = get_current_site(request).domain
        link = f"http://{domain}/{tipo}/{uid}/{token}/"
        
        message = render_to_string(template, {'user': persona, 'link': link})
        
        send_mail(subject, message, 'noreply@zeus.com', [email])
    except Exception as e:
        # Registra el error para depuración
        logger.error(f"Error al enviar el correo: {e}")
        # Opcional: lanza una excepción personalizada para manejarla en la vista
        raise Exception("Error al enviar el enlace por email.") from e

@api_view(['POST'])
def nuevo_pass(request, uidb64, token):
    # Esta vista reestablece la contraseña 
    # debe recibir new_password (ingresado por el usuario), uidb64 y token (contenidos en el link enviado al mail)
    # Ej. link = http://localhost:8000/reset/MTAw/cgp283-4c9040bae0afb89deb10f8734922e823/
    #  uidb64 = MTAw  (corresponde al id 10 de la tabla auth_user)
    #  token  = cgp283-4c9040bae0afb89deb10f8734922e823
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        if default_token_generator.check_token(user, token):
            new_password = request.data.get("new_password")
            user.password = make_password(new_password)
            user.save()
            return JsonResponse({"message": "Contraseña restablecida correctamente."}, status=200)
        else: 
            return JsonResponse({"error": "El enlace de restablecimiento no es válido o ha expirado (token no reconocido)."}, status=400)
    else:
        return JsonResponse({"error": "El enlace de restablecimiento no es válido o ha expirado (usuario incorrecto)."}, status=400)

def verificar_pago(user):
    # Falta la funcionalidad...
    return True


class AltaUsuariosView(View):
    def get(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name__in=["Administrador", "Co Administrador", "Delegado"]).exists():
            return JsonResponse({"error": "No tienes permisos para acceder a esta página."}, status=403)

        rol_alta = request.GET.get('rol', None)
        if rol_alta:
            if rol_alta in ["jugadores", "delegados", "árbitros", "coadministradores"]:
                plantilla = self.generar_plantilla_excel(rol_alta)
                response = HttpResponse(plantilla, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename=plantilla_{rol_alta}.xlsx'
                return response

        return JsonResponse({"message": "Especifica un rol válido para descargar la plantilla."}, status=400)

    def post(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name__in=["Administrador", "Co Administrador", "Delegado"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        archivo = request.FILES.get('archivo')
        if archivo:
            df = pd.read_excel(archivo)
            rol_alta = request.POST.get('rol')

            errores = self.validar_datos(df, rol_alta)
            if errores:
                return JsonResponse({"errores": errores}, status=400)

            try:
                with transaction.atomic():
                    self.crear_usuarios_temporales(df, rol_alta, request)
                return JsonResponse({"message": "Usuarios creados exitosamente."})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"error": "No se cargó ningún archivo."}, status=400)

    def generar_plantilla_excel(self, rol_alta):
        columnas = {
            "jugadores": ["Nombre", "Apellido", "Alias", "Email", "Tipo de Identificación", "Número de Identificación", "Sexo", "Fecha de Nacimiento", "Teléfono"],
            "delegados": ["Nombre", "Apellido", "Alias", "Email", "Tipo de Identificación", "Número de Identificación", "Sexo", "Fecha de Nacimiento", "Teléfono"],
            "árbitros": ["Nombre", "Apellido", "Alias", "Email", "Tipo de Identificación", "Número de Identificación", "Sexo", "Fecha de Nacimiento", "Teléfono"],
            "coadministradores": ["Nombre", "Apellido", "Alias", "Email", "Tipo de Identificación", "Número de Identificación", "Sexo", "Fecha de Nacimiento", "Teléfono"],
        }
        df = pd.DataFrame(columns=columnas.get(rol_alta, []))
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Plantilla")
        output.seek(0)
        return output

    def validar_datos(self, df, rol_alta):
        columnas_requeridas = [
            "Nombre", "Apellido", "Alias", "Email",
            "Tipo de Identificación", "Número de Identificación",
            "Sexo", "Fecha de Nacimiento", "Teléfono"
        ]
        errores = []

        faltantes = [col for col in columnas_requeridas if col not in df.columns]
        if faltantes:
            errores.append(f"Faltan las siguientes columnas: {', '.join(faltantes)}")
            return errores

        for index, row in df.iterrows():
            fila_errores = []

            email = row.get("Email", "").strip()
            if not email:
                fila_errores.append("El email es obligatorio.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                fila_errores.append("El formato del email es inválido.")
            elif User.objects.filter(email=email).exists():
                fila_errores.append("El email ya está en uso.")

            tipo_identificacion = row.get("Tipo de Identificación", "").strip()
            if not tipo_identificacion:
                fila_errores.append("El tipo de identificación es obligatorio.")
            elif not TiposIdentificacion.objects.filter(Codigo=tipo_identificacion).exists():
                fila_errores.append(f"El tipo de identificación '{tipo_identificacion}' no es válido.")

            sexo = row.get("Sexo", "").strip()
            if not sexo:
                fila_errores.append("El sexo es obligatorio.")
            elif not Sexos.objects.filter(SexoId=sexo).exists():
                fila_errores.append(f"El valor '{sexo}' no es un sexo válido.")

            fecha_nacimiento = row.get("Fecha de Nacimiento", "").strip()
            if not fecha_nacimiento:
                fila_errores.append("La fecha de nacimiento es obligatoria.")
            else:
                try:
                    datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
                except ValueError:
                    fila_errores.append(f"La fecha de nacimiento '{fecha_nacimiento}' debe estar en formato DD/MM/YYYY.")

            if fila_errores:
                errores.append(f"Errores en fila {index + 1}: {', '.join(fila_errores)}")

        return errores

    def crear_usuarios_temporales(self, df, rol_alta, request):
        errores = []
        for _, row in df.iterrows():
            try:
                UsuariosTemporales.objects.create(
                    nombre=row.get("Nombre"),
                    apellido=row.get("Apellido"),
                    alias=row.get("Alias"),
                    email=row.get("Email"),
                    tipo_identificacion=row.get("Tipo de Identificación"),
                    numero_identificacion=row.get("Número de Identificación"),
                    sexo=row.get("Sexo"),
                    fecha_nacimiento=row.get("Fecha de Nacimiento"),
                    telefono=row.get("Teléfono"),
                    rol=rol_alta,
                    creado_por=request.user
                )
            except Exception as e:
                errores.append(f"Error en fila {row.name + 1}: {str(e)}")

        if errores:
            raise Exception("Errores al crear usuarios temporales.")

    def confirmar_usuarios(self, request, *args, **kwargs):
        usuarios_temporales = UsuariosTemporales.objects.filter(creado_por=request.user)
        errores = []

        try:
            with transaction.atomic():
                for ut in usuarios_temporales:
                    usuario = User.objects.create_user(
                        username=ut.email,
                        email=ut.email,
                        password=ut.numero_identificacion,
                        first_name=ut.nombre,
                        last_name=ut.apellido,
                        is_active=True
                    )

                    grupo = Group.objects.get(name=ut.rol.capitalize())
                    usuario.groups.add(grupo)

                    tipo_identificacion_obj = TiposIdentificacion.objects.get(Codigo=ut.tipo_identificacion)
                    sexo_obj = Sexos.objects.get(SexoId=ut.sexo)

                    Personas.objects.create(
                        UserID=usuario,
                        Alias=ut.alias,
                        TipoIdentificacionID=tipo_identificacion_obj,
                        NroIdentificacion=ut.numero_identificacion,
                        SexoID=sexo_obj,
                        FechaNacimiento=ut.fecha_nacimiento,
                        Telefono=ut.telefono,
                    )
                UsuariosTemporales.objects.filter(creado_por=request.user).delete()
        except Exception as e:
            errores.append(str(e))

        if errores:
            return JsonResponse({"error": errores}, status=500)
        return JsonResponse({"message": "Usuarios confirmados exitosamente."})

    def cancelar_usuarios(self, request, *args, **kwargs):
        UsuariosTemporales.objects.filter(creado_por=request.user).delete()
        return JsonResponse({"message": "Proceso cancelado y datos eliminados temporalmente."})
    



class AltaequipoView(View):
    def post(self, request, *args, **kwargs):        
        # Verificar permisos
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)
        
        # Obtener datos del equipo desde la solicitud
        try:
            # Obtener datos del equipo desde la solicitud (JSON)
            data = json.loads(request.body)
            nombre = data.get("nombre")
            logo = data.get("logo")
            edicion = data.get("edicion")
            tipo = data.get("tipo")
            fecha_inicio = data.get("fecha_inicio")
            fecha_fin = data.get("fecha_fin")
            tipo_puntuacion = data.get("tipo_puntuacion")
            duracion_partido = data.get("duracion_partido")
            cantidad_tiempos = data.get("cantidad_tiempos")
            duracion_entretiempo = data.get("duracion_entretiempo")
            categoria = data.get("categoria")
            ciudad = data.get("ciudad")
            disciplina = data.get("disciplina")
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Validar datos requeridos
        errores = self.validar_datos(nombre, fecha_inicio, fecha_fin, duracion_partido, duracion_entretiempo, categoria, ciudad, disciplina)

        if errores:
            return JsonResponse({"errores": errores}, status=400)

        # Obtener la instancia de la ciudad
        ciudad = Ciudades.objects.filter(Nombre=ciudad).first()
        if not ciudad:
            return JsonResponse({"error": "La ciudad no existe"}, status=400)

        # Obtener la instancia de la disciplina
        disciplina = Disciplinas.objects.filter(Nombre=disciplina).first()
        if not disciplina:
            return JsonResponse({"error": "La disciplina no existe"}, status=400)

        # Obtener la instancia de la categoría
        categoria = Categorias.objects.filter(Nombre=categoria).first()
        if not categoria:
            return JsonResponse({"error": "La categoría no existe"}, status=400)

        estado_equipo = Estadosequipos.objects.filter(EstadoequipoID=3).first()
        if not estado_equipo:
            return JsonResponse({"error": "El estado del equipo no existe."}, status=400)
                
        if request.user.is_authenticated:
            administrador = request.user
        else:
            return JsonResponse({"error": "Usuario no autenticado"}, status=400)

    
        try:
            with transaction.atomic():
                equipo = equipos.objects.create(
                    Nombre=nombre,
                    CiudadID=ciudad,
                    Logo=logo,
                    Edicion=edicion,
                    DisciplinaID=disciplina,
                    CategoriaID=categoria,
                    Tipo=tipo,
                    FechaInicio=fecha_inicio,
                    FechaFin=fecha_fin,
                    TipoPuntuacion=tipo_puntuacion,
                    DuracionPartido=duracion_partido,
                    CantidadTiempos=cantidad_tiempos,
                    DuracionEntretiempo=duracion_entretiempo,
                    EstadoequipoID=estado_equipo,
                    AdministradorID=administrador
                )
                equipo.save()
            return JsonResponse({"message": "equipo creado exitosamente.", "equipo_id": equipo.equipoID})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def validar_datos(self, nombre, fecha_inicio, fecha_fin, duracion_partido, duracion_entretiempo, categoria, ciudad, disciplina):
        #Agregar validación de imagen para el logo
        #Ver qué es el tipo y tipo_puntuacion
        errores = []
        if not nombre:
            errores.append("El nombre del equipo es obligatorio.")
        if len(nombre) > 50:
            errores.append("El nombre del equipo no puede superar los 50 caracteres.")
        if not fecha_inicio:
            errores.append("La fecha de inicio es obligatoria.")
        if not fecha_fin:
            errores.append("La fecha de finalización es obligatoria.")
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            errores.append("La fecha de inicio no puede ser posterior a la fecha de finalización.")
        if not duracion_partido:
            errores.append("La duración del partido es obligatoria.")
        if not duracion_entretiempo:
            errores.append("La duración del entretiempo es obligatoria.")
        if not categoria:
            errores.append("La categoría es obligatoria.")
        if not ciudad:
            errores.append("La ciudad es obligatoria.")
        if not disciplina:
            errores.append("La disciplina es obligatoria.")
        return errores


class EliminarequipoView(View):
    def post(self, request, *args, **kwargs):
        # Verificar permisos
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        # Obtener el ID del equipo desde la solicitud
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Verificar si el equipo existe
        try:
            equipo = equipos.objects.get(equipoID=equipo_id)
        except equipos.DoesNotExist:
            return JsonResponse({"error": "El equipo no existe."}, status=400)

        # Eliminar el equipo
        try:
            equipo.delete()
            return JsonResponse({"message": "equipo eliminado exitosamente."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class ModificarequipoView(View):
    def post(self, request, *args, **kwargs):
        # Verificar permisos
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        # Obtener el ID del equipo desde la solicitud
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")
            nombre = data.get("nombre")
            logo = data.get("logo")
            edicion = data.get("edicion")
            tipo = data.get("tipo")
            fecha_inicio = data.get("fecha_inicio")
            fecha_fin = data.get("fecha_fin")
            tipo_puntuacion = data.get("tipo_puntuacion")
            duracion_partido = data.get("duracion_partido")
            cantidad_tiempos = data.get("cantidad_tiempos")
            duracion_entretiempo = data.get("duracion_entretiempo")
            categoria = data.get("categoria")
            ciudad = data.get("ciudad")
            disciplina = data.get("disciplina")
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Verificar si el equipo existe
        try:
            equipo = equipos.objects.get(equipoID=equipo_id)
        except equipos.DoesNotExist:
            return JsonResponse({"error": "El equipo no existe."}, status=400)

        # Obtener la instancia de la ciudad
        ciudad = Ciudades.objects.filter(Nombre=ciudad).first()
        if not ciudad:
            return JsonResponse({"error": "La ciudad no existe"}, status=400)

        # Obtener la instancia de la disciplina
        disciplina = Disciplinas.objects.filter(Nombre=disciplina).first()
        if not disciplina:
            return JsonResponse({"error": "La disciplina no existe"}, status=400)

        # Obtener la instancia de la categoría
        categoria = Categorias.objects.filter(Nombre=categoria).first()
        if not categoria:
            return JsonResponse({"error": "La categoría no existe"}, status=400)

        # Actualizar los campos del equipo
        equipo.Nombre = nombre or equipo.Nombre
        equipo.Logo = logo or equipo.Logo
        equipo.Edicion = edicion or equipo.Edicion
        equipo.Tipo = tipo or equipo.Tipo
        equipo.FechaInicio = fecha_inicio or equipo.FechaInicio
        equipo.FechaFin = fecha_fin or equipo.FechaFin
        equipo.TipoPuntuacion = tipo_puntuacion or equipo.TipoPuntuacion
        equipo.DuracionPartido = duracion_partido or equipo.DuracionPartido
        equipo.CantidadTiempos = cantidad_tiempos or equipo.CantidadTiempos
        equipo.DuracionEntretiempo = duracion_entretiempo or equipo.DuracionEntretiempo
        equipo.CategoriaID = categoria or equipo.CategoriaID
        equipo.CiudadID = ciudad or equipo.CiudadID
        equipo.DisciplinaID = disciplina or equipo.DisciplinaID

        # Guardar cambios
        try:
            equipo.save()
            return JsonResponse({"message": "equipo modificado exitosamente.", "equipo_id": equipo.equipoID})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




class AltaEquipoView(View):
    def post(self, request, *args, **kwargs):        
        # Verificar permisos
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador", "Delegado"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)
        
        # Obtener datos del equipo desde la solicitud
        try:
            # Obtener datos del equipo desde la solicitud (JSON)
            data = json.loads(request.body)
            nombre = data.get("nombre")
            logo = data.get("logo")
            categoria = data.get("categoria")
            disciplina = data.get("disciplina")
            division = data.get("division")
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Validar datos requeridos
        errores = self.validar_datos(nombre, categoria, disciplina, division)

        if errores:
            return JsonResponse({"errores": errores}, status=400)


        # Obtener la instancia de la disciplina
        disciplina = Disciplinas.objects.filter(Nombre=disciplina).first()
        if not disciplina:
            return JsonResponse({"error": "La disciplina no existe"}, status=400)

        # Obtener la instancia de la categoría
        categoria = Categorias.objects.filter(Nombre=categoria).first()
        if not categoria:
            return JsonResponse({"error": "La categoría no existe"}, status=400)
        
        division = Divisiones.objects.filter(Nombre=division).first()
        if not division:
            return JsonResponse({"error": "La división no existe"}, status=400)

        estado_equipo = EstadosEquipos.objects.filter(EstadoEquipoID=1).first()
        if not estado_equipo:
            return JsonResponse({"error": "El estado del equipo no existe."}, status=400)
                
        if request.user.is_authenticated:
            persona = request.user
        else:
            return JsonResponse({"error": "Usuario no autenticado"}, status=400)

    
        try:
            with transaction.atomic():
                equipo = Equipos.objects.create(
                    Nombre=nombre,
                    Logo=logo,
                    DisciplinaID=disciplina,
                    CategoriaID=categoria,
                    DivisionID=division,
                    EstadoEquipoID=estado_equipo
                )
                equipo.save()
            return JsonResponse({"message": "Equipo creado exitosamente.", "equipo_id": equipo.EquipoID})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def validar_datos(self, nombre, categoria, disciplina, division):
        #Agregar validación de imagen para el logo
        #Ver qué es el tipo y tipo_puntuacion
        errores = []
        if not nombre:
            errores.append("El nombre del equipo es obligatorio.")
        if len(nombre) > 50:
            errores.append("El nombre del equipo no puede superar los 50 caracteres.")
        if not categoria:
            errores.append("La categoría es obligatoria.")
        if not disciplina:
            errores.append("La disciplina es obligatoria.")
        if not division:
            errores.append("La división es obligatoria.")
        return errores
    

class ModificarEquipoView(View):
    def post(self, request, *args, **kwargs):
        # Verificar permisos
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        # Obtener el ID del equipo desde la solicitud
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")
            nombre = data.get("nombre")
            logo = data.get("logo")
            categoria = data.get("categoria")
            disciplina = data.get("disciplina")
            division = data.get("division")
            estado_equipo = data.get("estadoId")
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Verificar si el equipo existe
        try:
            equipo = Equipos.objects.get(equipoID=equipo_id)
        except Equipos.DoesNotExist:
            return JsonResponse({"error": "El equipo no existe."}, status=400)

        # Obtener la instancia de la ciudad
        ciudad = Ciudades.objects.filter(Nombre=ciudad).first()
        if not ciudad:
            return JsonResponse({"error": "La ciudad no existe"}, status=400)

        # Obtener la instancia de la disciplina
        disciplina = Disciplinas.objects.filter(Nombre=disciplina).first()
        if not disciplina:
            return JsonResponse({"error": "La disciplina no existe"}, status=400)

        # Obtener la instancia de la categoría
        categoria = Categorias.objects.filter(Nombre=categoria).first()
        if not categoria:
            return JsonResponse({"error": "La categoría no existe"}, status=400)
        
        division = Divisiones.objects.filter(Nombre=division).first()
        if not division:
            return JsonResponse({"error": "La división no existe"}, status=400)

        # Actualizar los campos del equipo
        equipo.Nombre = nombre or equipo.Nombre
        equipo.Logo = logo or equipo.Logo
        equipo.CategoriaID = categoria or equipo.CategoriaID
        equipo.CiudadID = ciudad or equipo.CiudadID
        equipo.DisciplinaID = disciplina or equipo.DisciplinaID
        equipo.EstadoEquipoID = estado_equipo or equipo.EstadoEquipoID

        # Guardar cambios
        try:
            equipo.save()
            return JsonResponse({"message": "equipo modificado exitosamente.", "equipo_id": equipo.equipoID})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class EliminarEquipoView(View):
    def post(self, request, *args, **kwargs):
        # Verificar permisos
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador", "Delegado"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        # Obtener el ID del equipo desde la solicitud
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Verificar si el equipo existe
        try:
            equipo = equipos.objects.get(equipoID=equipo_id)
        except equipos.DoesNotExist:
            return JsonResponse({"error": "El equipo no existe."}, status=400)

        # Eliminar el equipo
        try:
            equipo.delete()
            return JsonResponse({"message": "equipo eliminado exitosamente."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        



class AltaJugadoresView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador", "Delegado"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        data = json.loads(request.body)
        cargar_por_excel = data.get("cargar_por_excel", 0)

        if cargar_por_excel == 1:
            if 'archivo_excel' not in request.FILES:
                return JsonResponse({"error": "No se ha enviado el archivo Excel."}, status=400)
            
            archivo_excel = request.FILES['archivo_excel']
            try:
                df = pd.read_excel(archivo_excel)

                columnas_esperadas = [
                    "user_id", "equipo_id", "fecha_incorporacion", "estado_actor_id", "rol_delegado", "rol_jugador_id", "foto"
                ]
                if list(df.columns) != columnas_esperadas:
                    return JsonResponse({"error": "El archivo Excel no tiene el formato esperado."}, status=400)

                df['rol_delegado'] = df['rol_delegado'].apply(lambda x: True if str(x).strip().lower() == "delegado" else False)

                jugadores = df.to_dict(orient="records")

            except Exception as e:
                return JsonResponse({"error": f"Error al procesar el archivo Excel: {str(e)}"}, status=400)

        else:
            try:
                jugadores = data.get("jugadores", [])
            except json.JSONDecodeError:
                return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

            if not jugadores:
                return JsonResponse({"error": "No se proporcionaron jugadores."}, status=400)

        resultados = []
        errores_generales = []

        for idx, jugador_data in enumerate(jugadores):
            user_id = jugador_data.get("user_id")
            equipo_id = jugador_data.get("equipo_id")
            fecha_incorporacion = jugador_data.get("fecha_incorporacion")
            estado_actor_id = jugador_data.get("estado_actor_id")
            rol_delegado = jugador_data.get("rol_delegado", False)
            rol_jugador_id = jugador_data.get("rol_jugador_id")
            foto = jugador_data.get("foto", None)

            errores = self.validar_datos(user_id, equipo_id, fecha_incorporacion, estado_actor_id, rol_delegado, rol_jugador_id)

            if errores:
                errores_generales.append({"jugador": idx, "errores": errores})
                continue

            try:
                with transaction.atomic():
                    jugador = Jugadores.objects.create(
                        UserID_id=user_id,
                        EquipoID_id=equipo_id,
                        FechaIncorporacion=fecha_incorporacion,
                        EstadoActorID_id=estado_actor_id,
                        Rol_id=rol_jugador_id,
                        Foto=foto
                    )

                    if rol_delegado:
                        if Delegados.objects.filter(EquipoID_id=equipo_id).exists():
                            errores_generales.append({
                                "jugador": idx,
                                "errores": [f"Ya existe un delegado para el equipo {equipo_id}."]
                            })
                        else:
                            Delegados.objects.create(
                                UserID_id=user_id,
                                EquipoID_id=equipo_id,
                                FechaIncorporacion=fecha_incorporacion,
                                EstadoActorID_id=estado_actor_id,
                                Foto=foto
                            )

                    resultados.append({
                        "jugador_id": jugador.JugadorID,
                        "user_id": user_id,
                        "delegado": rol_delegado
                    })

            except Exception as e:
                errores_generales.append({"jugador": idx, "error": str(e)})

        return JsonResponse({
            "creados": resultados,
            "errores": errores_generales
        }, status=207 if errores_generales else 201)

    def validar_datos(self, user_id, equipo_id, fecha_incorporacion, estado_actor_id, rol_delegado, rol_jugador_id):
        errores = []
        if not user_id:
            errores.append("El ID de usuario es obligatorio.")
        if not equipo_id:
            errores.append("El ID del equipo es obligatorio.")
        if not fecha_incorporacion:
            errores.append("La fecha de incorporación es obligatoria.")
        if not estado_actor_id:
            errores.append("El estado actor es obligatorio.")
        if not rol_jugador_id:
            errores.append("El ID del rol del jugador es obligatorio.")
        return errores


class ModificarJugadorView(View):
    def put(self, request, jugador_id, *args, **kwargs):
        if not request.user.groups.filter(name__in=["Administrador de equipo", "Coadministrador", "Delegado"]).exists():
            return JsonResponse({"error": "No tienes permisos para realizar esta acción."}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la solicitud no contiene un JSON válido."}, status=400)

        # Buscar jugador
        try:
            jugador = Jugadores.objects.get(pk=jugador_id)
        except Jugadores.DoesNotExist:
            return JsonResponse({"error": "El jugador especificado no existe."}, status=404)

        # Validar y obtener datos del JSON
        equipo_id = data.get("equipo_id")
        estado_actor_id = data.get("estado_actor_id")
        fecha_incorporacion = data.get("fecha_incorporacion")
        rol_delegado = data.get("rol_delegado", False)
        rol_jugador_id = data.get("rol_jugador_id")
        foto = data.get("foto", None)

        errores = []
        if not equipo_id:
            errores.append("El ID del equipo es obligatorio.")
        if not estado_actor_id:
            errores.append("El estado actor es obligatorio.")
        if not fecha_incorporacion:
            errores.append("La fecha de incorporación es obligatoria.")
        if not rol_jugador_id:
            errores.append("El ID del rol del jugador es obligatorio.")

        if errores:
            return JsonResponse({"errores": errores}, status=400)

        try:
            with transaction.atomic():
                jugador.EquipoID_id = equipo_id
                jugador.EstadoActorID_id = estado_actor_id
                jugador.FechaIncorporacion = parse_date(fecha_incorporacion)
                jugador.Rol_id = rol_jugador_id
                if foto:
                    jugador.Foto = foto
                jugador.save()

                # Si se marcó como delegado
                if rol_delegado:
                    if not Delegados.objects.filter(EquipoID_id=equipo_id).exclude(UserID=jugador.UserID).exists():
                        Delegados.objects.update_or_create(
                            UserID=jugador.UserID,
                            defaults={
                                "EquipoID_id": equipo_id,
                                "FechaIncorporacion": jugador.FechaIncorporacion,
                                "EstadoActorID_id": estado_actor_id,
                                "Foto": jugador.Foto
                            }
                        )
                    else:
                        return JsonResponse({"error": f"Ya existe un delegado para el equipo {equipo_id}."}, status=400)
                else:
                    Delegados.objects.filter(UserID=jugador.UserID).delete()

            return JsonResponse({
                "mensaje": "Jugador modificado correctamente.",
                "jugador_id": jugador_id
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Error al modificar el jugador: {str(e)}"}, status=500)