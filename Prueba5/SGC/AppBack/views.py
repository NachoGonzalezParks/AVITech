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
from .models import Personas, TiposIdentificacion      
'''Agregados para envío y verif. de mail al registrarse'''          
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .Tokens import account_activation_token    # Crear un token personalizado para verificación
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed


# Esta vista verificar si el email recibido del front ya existe en BD
# (cuando el usuario ingresa el email con el cual se va a registrar) 
@api_view(['POST'])
def email_existe(request):   

    # Recibe el email desde el front
    email = request.data.get('email')

    # Verifica si el email ya está en uso
    email_existe = User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists()

    # Devuelve true si el email existe, false si está disponible
    if email_existe:
        return Response({'existe': True}, status=status.HTTP_200_OK)
    else:
        return Response({'existe': False}, status=status.HTTP_200_OK)


# Esta vista inserta un nuevo usuario y envía el mail de verificaciòn 
@api_view(['POST'])
@transaction.atomic  
def registro_usuario(request):    

    '''DEVOLUCIONES AL FRONT:
      1) Datos no válidos como 
         pass débiles                           >>> ("Contraseña débil: This password is too short. It must contain at least 8 characters., This password is too common., This password is entirely numeric.")
         pass distintas                         >>> ("Las contraseñas no coinciden.")
         formato de fecha incorrecto            >>> ("Error: ['“1980-13-08” value has the correct format (YYYY-MM-DD) but it is an invalid date.']")
                                                  ó ("Error: ['“abc” value has an invalid date format. It must be in YYYY-MM-DD format.']")
         tipo de identificación inexistente     >>> ("Error: TiposIdentificacion matching query does not exist.")
         nombre y apellido vacío                >>> ("El nombre y el apellido no pueden estar vacíos.")
         usrusuario existente                   >>> ("Error: llave duplicada viola restricción de unicidad «auth_user_username_key»\nDETAIL:  Ya existe la llave (username)=(admin3@example.com).\n")
         envío de mail                          >>> ("Error: account/acc_active_email.html"})
      2) Ante un error luego e las validaciones hace rollback de todas las tablas y devuleve el msg (varía de acuerdo al error que lo provocó)      
    '''

    # Datos recibidos desde el front
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

        admin_group = Group.objects.get(name="Administrador")
        user.groups.add(admin_group)

        # Enviar email para requerir verificación de la cuenta
        # Ej . Carpeta Templates = C:\Users\aleja\OneDrive\Documentos\Ale\SistemaGC\AVITech\Prueba5\SGC\templates
        current_site = get_current_site(request)   # seteado en http://localhost:8000/admin/sites
        mail_subject = 'Activa tu cuenta en Zeus.com'                       
        message = render_to_string('mail_activacion.html', {
            'user': persona,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, 'noreply@zeus.com', [email])    
        
        return Response({'success': True, 'message': f'Registro exitoso. Revisa tu correo para confirmar tu cuenta. {message}'}, status=status.HTTP_201_CREATED)
          
    except Exception as e:
        transaction.set_rollback(True)
        return Response({'success': False, 'message': f'Error esto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Esta vista recibe la url de verificación, accedida desde el mail del usuario, y si el link es válido activa la cuenta (EmailAddress.verified = True)
@api_view(['GET'])
def activacion(request, uidb64, token):
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


# Esta vista recibe el mail y la contraseña, y si los datos son correctos logguea al usuario
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
        return response


    except AuthenticationFailed as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist as e:
        return Response({'success': False, 'message': 'No se pudo encontrar el objeto solicitado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'message': f'Ocurrió un error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Esta función devuelve la información del usuario
def get_user_groups(user):
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


