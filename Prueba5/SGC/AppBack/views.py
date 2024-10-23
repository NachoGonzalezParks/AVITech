import requests
from django.conf import settings
from django.db import transaction  # Para asegurar atomicidad
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



def controlar_usuario(request):
    return True  # Aca hay que controlar si el email a dar de alta ya existe (es para cuando el usuario ingresa el email con qel cual se va a registrar)


    # llamar al end point http://127.0.0.1:8000/api/auth/registration/ pasando username, email , pass1 y pass2

    # si la respuesta de api/auth/registration es correcta dar de alta el resto de la info
        # si la inserción del resto es correcta enviar mensaje de éxito al front con aviso que se envió mail para verificar
        # si la inserción del resto es incorrecta devolver borrar el usuario dado de alta y devolver mensaje al front

    # si la respuesta de api/auth/registration es incorrecta devolver info al front



@api_view(['POST'])
@transaction.atomic  # Garantiza que si algo falla, la transacción se deshace (rollback).
def registro_usuario(request):
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
        # Primero llamamos al registro en /api/auth/registration/
    
        #response = requests.post(f"{settings.BASE_URL}/api/auth/registration/", data=request.data)
        response = requests.post(f"{settings.BASE_URL}/api/auth/registration/", data={
        'username': email,
        'email': email,
        'password1': password1,
        'password2': password2,                
        })
    
        #return Response({'success': False, 'message': 'Error: al agregar el usuario.'}, status=status.HTTP_400_BAD_REQUEST)

        if response.status_code == 201:  # Registro exitoso
            # Convertir el tipo de identificación a su ID
            from .models import Personas, TiposIdentificacion
            from django.contrib.auth.models import User
            user = User.objects.get(email=email),
                    
            tipo_identificacion_obj = TiposIdentificacion.objects.get(Codigo=tipo_identificacion)   #request.data['tipo_identificacion'])
        
            #return Response({'success': False, 'message': 'Error: Tipo de Identificación no válido.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Registrar la persona solo si el registro del usuario fue exitoso
            persona = Personas.objects.create(
                UserID=user[0],
                Nombre=request.data['nombre'],
                Apellido=request.data['apellido'],
                Alias=request.data['alias'],
                TipoIdentificacionID=tipo_identificacion_obj,
                NroIdentificacion=request.data['numero_identificacion'],
                FechaNacimiento=request.data['fecha_nacimiento'],
                Telefono=request.data['telefono']
            )

            return Response({'success': True, 'message': 'Registro exitoso. Revisa tu correo para confirmar tu cuenta.'}, status=status.HTTP_201_CREATED)
            
            #return Response({'success': False, 'message': 'Error en el registro de datos personales.'}, status=status.HTTP_400_BAD_REQUEST)
  
        else:
            # Si falla el registro del usuario
            return Response({'success': False, 'message': 'Error general en el registro de usuario (status < > a 201).'}, status=response.status_code)

    except Exception as e:
        # Si ocurre algún otro error en cualquier parte del proceso, la transacción se deshace
        transaction.set_rollback(True)
        return Response({'success': False, 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

'''
    except TiposIdentificacion.DoesNotExist:
        transaction.set_rollback(True)
        return Response({'success': False, 'message': 'Tipo de Identificación no válido.'}, status=status.HTTP_400_BAD_REQUEST
'''



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_groups(request):
    user = request.user
    groups = user.groups.all()  # Obtener los grupos a los que pertenece el usuario
    group_names = [group.name for group in groups]
    
    return Response({
        'pk': user.pk,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'groups': group_names  # Agregar los nombres de los grupos
    })


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
