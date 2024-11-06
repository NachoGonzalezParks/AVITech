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

@api_view(['POST'])
def email_existe(request):
    # esta vista verificar si el email recibido del front ya existe en BD 
    # (cuando el usuario ingresa el email con el cual se va a registrar)    

    # Recibe el email desde el request
    email = request.data.get('email')

    # Verifica si el email ya está en uso
    email_existe = User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists()

    # Devuelve true si el email existe, false si está disponible
    if email_existe:
        return Response({'existe': True}, status=status.HTTP_200_OK)
    else:
        return Response({'existe': False}, status=status.HTTP_200_OK)



    ''' JSON de ejemplo para probar registro_usuario
    {
    "email": "user@example.com",
    "password1": "password123",
    "password2": "password123",
    "nombre": "Juan",
    "apellido": "Pérez",
    "alias": "jperez",
    "tipo_identificacion": "DNI",
    "numero_identificacion": "12345678",
    "fecha_nacimiento": "1980-12-08",
    "telefono": "543516932000"
    }
    '''



@api_view(['POST'])
@transaction.atomic  # Garantiza que si algo falla, la transacción se deshace (rollback).
def registro_usuario(request):
    # Esta vista inserta un nuevo usuario y envía el mail de verificaciòn 

    '''POSIBLES VALIDACIONES:
      1) Datos no válidos como 
         pass débiles                           >>> OK ("Contraseña débil: This password is too short. It must contain at least 8 characters., This password is too common., This password is entirely numeric.")
         pass distintas                         >>> OK ("Las contraseñas no coinciden.")
         formato de fecha incorrecto            >>> OK ("Error: ['“1980-13-08” value has the correct format (YYYY-MM-DD) but it is an invalid date.']")
                                                     ó ("Error: ['“abc” value has an invalid date format. It must be in YYYY-MM-DD format.']")
         tipo de identificación inexistente     >>> OK ("Error: TiposIdentificacion matching query does not exist.")
         nombre y apellido vacío                >>> OK ("El nombre y el apellido no pueden estar vacíos.")
         usr existente                          >>> OK ("Error: llave duplicada viola restricción de unicidad «auth_user_username_key»\nDETAIL:  Ya existe la llave (username)=(admin3@example.com).\n")
      2) ver si la transacción hace rollback de todas las tablas ante un error  >>> OK
      2) Clasificar posibles mensajes de error a devolver al front
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

       # Validación 1: Verificar que las contraseñas coincidan
        if password1 != password2:
            return Response({'success': False, 'message': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validación 2: Verificar que la contraseña cumpla con los requisitos de seguridad
        try:
            validate_password(password1)
        except ValidationError as password_error:
            return Response({'success': False, 'message': f'Contraseña débil: {", ".join(password_error.messages)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validación 3: Campos requeridos no vacíos
        if not nombre or not apellido:
            return Response({'success': False, 'message': 'El nombre y el apellido no pueden estar vacíos.'}, status=status.HTTP_400_BAD_REQUEST)

        if not numero_identificacion:
            return Response({'success': False, 'message': 'El número de identificación no pueden estar vacío.'}, status=status.HTTP_400_BAD_REQUEST)

        if not fecha_nacimiento:
            return Response({'success': False, 'message': 'La fecha de nacimiento no pueden estar vacía.'}, status=status.HTTP_400_BAD_REQUEST)
        
               # Valida que el email sea un formato válido
        try:
            validate_email(email)
        except ValidationError:
            return Response({'success': False, 'message': 'El formato del email es inválido.'}, status=status.HTTP_400_BAD_REQUEST)
            #raise DRFValidationError("El formato del email es inválido.")            

        # Crea el usuario (tabla auth_user)        
        user = User.objects.create_user(username=email, email=email, password=password1)

        # Crea el registro en tabla auth_accountemailaddress        
        email_address = EmailAddress.objects.create(
            user=user,
            email=email,
            verified=False,  # Para que quede como NO verificado
            primary=True
        )

        # Crear el token del usuario (tabla authtoken_token)        
        token = Token.objects.create(user=user)        

        # Obtiene el tipo de identificaciòn correspondiente al código recibido del front
        tipo_identificacion_obj = TiposIdentificacion.objects.get(Codigo=tipo_identificacion)   #request.data['tipo_identificacion'])
    
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

        # ACA FALTA mandar el correo para verificaciòn del email!!!!!!!
        return Response({'success': True, 'message': 'Registro exitoso. Revisa tu correo para confirmar tu cuenta.'}, status=status.HTTP_201_CREATED)
          

    except Exception as e:
        # Si ocurre algún otro error en cualquier parte del proceso, la transacción se deshace
        transaction.set_rollback(True)
        return Response({'success': False, 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def login_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        email_address = EmailAddress.objects.filter(user=user, email=username).first()
        
        if email_address and email_address.verified:
            login(request, user)
            response = get_user_groups(user)
            return response

        else:
            return Response({'success': False, 'message': 'La cuenta no ha sido verificada.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'success': False, 'message': 'Datos incorrectos'}, status=status.HTTP_400_BAD_REQUEST)




def get_user_groups(user):
    groups = user.groups.all()
    group_names = [group.name for group in groups]
    
    return Response({
        'success': True,
        'message': 'Inicio de sesión exitoso.',
        'pk': user.pk,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'groups': group_names
    })


'''
    CODIGO DESCARTADO

    except TiposIdentificacion.DoesNotExist:
        transaction.set_rollback(True)
        return Response({'success': False, 'message': 'Tipo de Identificación no válido.'}, status=status.HTTP_400_BAD_REQUEST

        # Primero llamamos al registro en /api/auth/registration/
    
        #response = requests.post(f"{settings.BASE_URL}/api/auth/registration/", data=request.data)
        #response = requests.post(f"{settings.BASE_URL}/api/auth/registration/", data={
        #'username': email,
        ##'email': email,
        #'password1': password1,
        #'password2': password2,                
        #})
    
        #user = User.objects.get(email=email),

        #return Response({'success': False, 'message': 'Error: al agregar el usuario.'}, status=status.HTTP_400_BAD_REQUEST)

        #if response.status_code == 201:  # Registro exitoso
            # Convertir el tipo de identificación a su ID

     #return Response({'success': False, 'message': 'Error: Tipo de Identificación no válido.'}, status=status.HTTP_400_BAD_REQUEST)           
        
'''




'''
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Autenticamos utilizando el email
    user = authenticate(username=email, password=password)

    if user is not None:
        # Genera el token JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': [group.name for group in user.groups.all()],
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
'''

'''
from django.shortcuts import render, redirect
from django.views import View
#from .models import TiposIdentificacion
#from .Forms import TipoIdentificacionForm
#from .models import TiposIdentificacion
#from .serializers import TiposIdentificacionSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    usuario = request.data.get('email')  # agregado
    email = request.data.get('email')
    password = request.data.get('password')

    # Autenticamos utilizando el email como username
    # user = authenticate(request, username=email, password=password)
    #user = authenticate(request, username=usuario, email=email, password=password) # Agregado    

    user =  get_user_model()

    try:
        user = user.objects.get(email=email)
    except user.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data

        # Devuelve el token y la información del usuario correctamente estructurada
        return Response({
            'token': token.key,  # El token del usuario
            'first_name': user.first_name,  # Primer nombre
            'last_name': user.last_name,    # Apellido
            'groups': [group.name for group in user.groups.all()]  # Grupos del usuario
        }, status=status.HTTP_200_OK)    
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

###
'''
'''
@api_view(['POST'])
def login_view(request):
    usuario = request.data.get('email')
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(request, username=usuario, email=email, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        
        # Obtener grupos del usuario
        groups = user.groups.values_list('name', flat=True)
        user_data = UserSerializer(user).data
        return Response({
                    'token': token.key,
                    'user': user_data
                }, status=status.HTTP_200_OK)
        
        #return Response({
        #    'token': token.key,
        #    'user_id': user.pk,
        #    'email': user.email,
        #    'first_name': user.first_name,
        #    'last_name': user.last_name,
        #    'groups': list(groups)
        #}, status=status.HTTP_200_OK)
        
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
   ''' 
'''
class TipoIdentificacionViewSet(viewsets.ModelViewSet):
    queryset = TiposIdentificacion.objects.all()
    serializer_class = TiposIdentificacionSerializer


# Create your views here.
# Function-based view para home y Pagina2

def home(request):
    return render(request, 'Pagina1.html')

def pagina2(request):    
    return render(request, 'Pagina2.html')

# Class-based view para Pagina3
class Pagina3View(View):
    def get(self, request):
        return render(request, 'Pagina3.html')
    


# Vista para Pagina4.html
def pagina4(request):
    tipos_identificacion = TiposIdentificacion.objects.all()
    return render(request, 'pagina4.html', {'tipos_identificacion': tipos_identificacion})

# Vista para Pagina5.html
def pagina5(request):
    if request.method == 'POST':
        form = TipoIdentificacionForm(request.POST)
        if form.is_valid():
            form.save()            
            return redirect('pagina4')
    else:
        form = TipoIdentificacionForm()
    return render(request, 'pagina5.html', {'form': form})    
    

def modificar_tipo(request, pk):
    tipo = get_object_or_404(TiposIdentificacion, pk=pk)
    if request.method == 'POST':
        form = TipoIdentificacionForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('pagina4')
    else:
        form = TipoIdentificacionForm(instance=tipo)
    return render(request, 'Pagina6.html', {'form': form})

def eliminar_tipo(request, pk):
    tipo = get_object_or_404(TiposIdentificacion, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        return redirect('pagina4')
    

Resumen de diferencias entre Function (Pagina1) views y Class-based views (Pagina2)
------------------------------------------------------------------------------------
Las Class-Based Views (CBVs) en Django proporcionan una forma más estructurada y orientada a objetos para manejar vistas, 
en comparación con las Function-Based Views (FBVs). 
CBVs permiten reutilizar código y seguir patrones de diseño como la herencia y la encapsulación, 
lo cual facilita la extensión y personalización de la funcionalidad de las vistas.

Diferencias clave y consideraciones
Modularidad y Reutilización:
CBVs: Facilitan la reutilización de código mediante herencia de clases y mixins. 
      Puedes crear clases base con funcionalidad común y especializar vistas para casos específicos.
FBVs: El código es más explícito y a menudo está todo en una sola función, lo que puede llevar a duplicación de código 
      si se requieren comportamientos similares en diferentes vistas.

Organización del Código:
CBVs: Organizan el código en métodos de una clase, lo que puede hacer que las vistas sean más fáciles de mantener y entender, 
      especialmente en aplicaciones grandes. Métodos como get(), post(), get_context_data(), y form_valid() se utilizan 
      para manejar lógica específica de la vista.
FBVs: Tienen una estructura más simple, siendo una función que maneja la solicitud y devuelve una respuesta. 
      Toda la lógica está contenida dentro de la misma función.

Extensibilidad:
CBVs: Son fácilmente extensibles. Puedes crear mixins para añadir funcionalidad específica y reutilizable en múltiples vistas. 
      Por ejemplo, un mixin de autenticación que garantice que solo los usuarios autenticados pueden acceder a ciertas vistas.
FBVs: Requieren escribir la lógica directamente en la función o utilizar decoradores para agregar funcionalidad adicional.

Simplicidad vs. Abstracción:
CBVs: Pueden tener una curva de aprendizaje más pronunciada debido a su mayor nivel de abstracción. 
      Sin embargo, una vez comprendidos, pueden hacer que el desarrollo sea más eficiente.
FBVs: Son más directas y fáciles de entender para los desarrolladores nuevos en Django, ya que se ajustan al paradigma tradicional de las funciones.
'''
