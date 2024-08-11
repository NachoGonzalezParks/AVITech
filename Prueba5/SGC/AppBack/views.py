from django.shortcuts import render, redirect
from django.views import View
from .models import TiposIdentificacion
from .Forms import TipoIdentificacionForm
from django.shortcuts import get_object_or_404

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
    
'''
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
