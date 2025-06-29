import requests
from django.conf import settings
from django.db import transaction  # Para asegurar atomicidad
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token     
from rest_framework.exceptions import ValidationError as DRFValidationError   
from allauth.account.models import EmailAddress        
from .models import Personas, TiposIdentificacion, LoginPersona, Sexos, UsuariosTemporales, Paises                         
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
import logging
import pandas as pd
import re
from io import BytesIO
from datetime import datetime
logger = logging.getLogger(__name__)


def validar_fecha(fecha, mayor_a_hoy, menor_a_hoy):
    # sirve para controlar el formato de cualquier fecha, 
    # si los parámetros mayor a hoy o menor_a_hoy se pasan en verdadero controla con respecto a la fecha actual
    # si se pasan en falso solo controla el formato
    try:
        # Intentar convertir la fecha al formato dd/mm/yyyy
        ##fecha_controlada = datetime.strptime(fecha, '%d/%m/%Y')
        fecha_controlada = datetime.strptime(fecha, '%Y-%m-%d')
        
        # Verificar que la fecha no sea en el futuro
        if mayor_a_hoy == True and fecha_controlada > datetime.now():
            return False, 'La fecha ingresada no puede ser mayor a la actual.'
        
        # Verificar que la fecha no sea en el pasado
        if menor_a_hoy == True and fecha_controlada < datetime.now():
            return False, 'La fecha ingresada no puede ser menor a la actual.'

        return True, None  # La fecha es válida
    except ValueError:
        return False, 'La fecha ingresada no es válida (formato: dd/mm/aaaa).'

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
        pais = Paises.objects.get(Nombre=nombre_pais)
        tipos = TiposIdentificacion.objects.filter(PaisID=pais)
        
        # CORRECCIÓN: Devolver lista de strings con los códigos
        tipos_list = [tipo.Codigo for tipo in tipos]
        
        return Response({'tipos_identificacion': tipos_list}, status=200)
    except Paises.DoesNotExist:
        return Response({'error': 'País no encontrado'}, status=404)
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

        es_valida, mensaje_error = validar_fecha(fecha_nacimiento, False, False)
        if not es_valida:
            return Response({'success': False, 'message': mensaje_error}, status=status.HTTP_400_BAD_REQUEST)

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

        admin_group = Group.objects.get(name="Administrador de torneo")
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
            return Response({'success': False, 'message': 'Nombre de usuario y contraseña son requeridos.'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=username, password=password)

        if user is None:
            raise AuthenticationFailed('Datos incorrectos')
        
        # Generar token de autenticación para agregar como respuesta en el body
        token, _ = Token.objects.get_or_create(user=user)

        try:
            email_address = EmailAddress.objects.get(user=user, email=username)
        except ObjectDoesNotExist:
            return Response({
                'success': False, 
                'message': 'No se encontró una cuenta asociada a este correo.',
                'token': None
            }, status=status.HTTP_404_NOT_FOUND)

        if not email_address.verified:
            return Response({
                'success': False, 
                'message': 'La cuenta no ha sido verificada.',
                'token': None
            }, status=status.HTTP_400_BAD_REQUEST)

        #response = get_user_groups(user) >>> Descartado, ahora se obtiene en user_data

        # Obtener datos básicos del usuario
        user_data = {
            'success': True,
            'message': 'Sesión iniciada correctamente',
            'pk': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': [group.name for group in user.groups.all()],
            'token': token.key  # Incluir el token en la respuesta
        }

        if 'Administrador de torneo' in user_data['groups']:
            try:
                # Se marca como False el campo first_login de la tabla Personas
                persona = Personas.objects.get(UserID=user)
                if persona.first_login == True:
                    persona.first_login = False
                    persona.save()
                
                if not verificar_pago(user):
                    return Response({
                        'success': False, 
                        'message': 'El pago de su cuenta no está completado.',
                        'token': None
                    }, status=status.HTTP_402_PAYMENT_REQUIRED)

                marcar_login('loguear', user_data['pk'], user_data['email'])
                
            except ObjectDoesNotExist:
                return Response({
                    'success': False, 
                    'message': 'No se encontró la persona asociada a este usuario.',
                    'token': None
                }, status=status.HTTP_404_NOT_FOUND)

        else:
            try:
                # if 'Co Administrador' in response.data['groups'] or 'Delegado' in response.data['groups'] or 'Árbitro' in response.data['groups'] or 'Jugador' in response.data['groups']:
                persona = Personas.objects.get(user=user)
                if persona.first_login:
                    # Cambiar la contraseña (porque al darlo de alta se guardó el DNI o Número de Identificación como contraseña inicial/temporal)
                    new_password = request.data.get('new_password')
                    
                    if not new_password or len(new_password) < 8:
                        return Response({
                            'success': False, 
                            'message': 'Se requiere una nueva contraseña válida (mínimo 8 caracteres)',
                            'token': None
                        }, status=status.HTTP_400_BAD_REQUEST)
                        
                    user.set_password(new_password)
                    user.save()
                    persona.first_login = False
                    persona.save()
                    
                    return Response({
                        'success': True,
                        'message': 'Contraseña actualizada. Por favor inicie sesión nuevamente.',
                        'token': None
                    }, status=status.HTTP_200_OK)
                    
            except ObjectDoesNotExist:
                return Response({
                    'success': False, 
                    'message': 'Registro de persona no encontrado',
                    'token': None
                }, status=status.HTTP_404_NOT_FOUND)

        return Response(user_data, status=status.HTTP_200_OK)

    except AuthenticationFailed as e:
        return Response({
            'success': False, 
            'message': str(e),
            'token': None
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.error(f'Error en login: {str(e)}')
        return Response({
            'success': False, 
            'message': f'Error interno del servidor: {str(e)}',
            'token': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

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