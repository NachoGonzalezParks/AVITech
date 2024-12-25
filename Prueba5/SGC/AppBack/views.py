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
from .models import Personas, TiposIdentificacion, LoginPersona              
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
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import logging
logger = logging.getLogger(__name__)


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
    # Debe recibir: email, password1, password2, nombre, apellido, tipo_identificacion, numero_identificacion, fecha_nacimiento
    #   opcionales: alias, telefono       
    username = request.data.get('email')
    email = request.data.get('email')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    nombre = request.data.get('nombre')
    apellido = request.data.get('apellido')
    alias = request.data.get('alias')
    tipo_identificacion = request.data.get('tipo_identificacion')
    numero_identificacion = request.data.get('numero_identificacion')
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
       
      
        user = User.objects.create_user(username=email, email=email, password=password1)
      
        email_address = EmailAddress.objects.create(
            user=user,
            email=email,
            verified=False,
            primary=True
        )
     
        token = Token.objects.create(user=user)        
        tipo_identificacion_obj = TiposIdentificacion.objects.get(Codigo=tipo_identificacion)   
    
        persona = Personas.objects.create(
            UserID=user,
            Nombre=request.data['nombre'],
            Apellido=request.data['apellido'],
            Alias=request.data['alias'],
            TipoIdentificacionID=tipo_identificacion_obj,
            NroIdentificacion=request.data['numero_identificacion'],
            FechaNacimiento=request.data['fecha_nacimiento'],
            Telefono=request.data['telefono']
        )

        admin_group = Group.objects.get(name="Administrador_de_torneo")
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
    # Esta vista recibe el mail y la contraseña, y si los datos son correctos loguea al usuario
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

        # Obtén la respuesta de los grupos de usuario
        response = get_user_groups(user)
        
        if 'Administrador' in response.data['groups']:
            if verificar_pago(user):
                try:
                    # Loguear usuario
                    marcar_login('logguear', response.data['pk'], response.data['email'])
                except RuntimeError as e:
                    return Response({'success': False, 'message': f'Error al loguear: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response({'success': False, 'message': 'El pago de su cuenta no está completado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Independientemente de que esté logueado o no, siempre se devuelve la respuesta
        return response

    except AuthenticationFailed as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist as e:
        return Response({'success': False, 'message': 'No se pudo encontrar el objeto solicitado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'message': f'Ocurrió un error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        if accion == 'logguear':
            # Agregar o verificar existencia de la persona
            persona, creada = LoginPersona.objects.get_or_create(id=id, mail=email)
            return creada  # True si la persona fue creada, False si ya existía

        elif accion == 'deslogguear':
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
