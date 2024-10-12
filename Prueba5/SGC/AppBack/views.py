from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

def controlar_usuario(request):
    return True  # Aca hay que controlar si el email a dar de alta ya existe (es para cuando el usuario ingresa el email con qel cual se va a registrar)


@api_view(['POST'])
def registro_usuario(request):
    username =request.email 
    email = request.email
    password1 = request.password1
    password2 = request.password2
    nombre = request.nombre
    apellido = request.apellido
    alias = request.alias
    tipo_identificacion = request.tipo_identificacion
    numero_identificacion = request.numero_identificacion
    fecha_nacimiento = request.fecha_nacimiento
    telefono = request.telefono

    # llamar al end point http://127.0.0.1:8000/api/auth/registration/ pasando username, email , pass1 y pass2

    # si la respuesta de api/auth/registration es correcta dar de alta el resto de la info
        # si la inserción del resto es correcta enviar mensaje de éxito al front con aviso que se envió mail para verificar
        # si la inserción del resto es incorrecta devolver borrar el usuario dado de alta y devolver mensaje al front

    # si la respuesta de api/auth/registration es incorrecta devolver info al front





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
