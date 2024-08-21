from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Página de inicio o /pagina1
    path('pagina1/', views.home, name='home'),  # Página de inicio o /pagina1
    path('pagina2/', views.pagina2, name='pagina2'),  # Function-based view
    path('pagina3/', views.Pagina3View.as_view(), name='pagina3'),  # Class-based view
    path('pagina4/', views.pagina4, name='pagina4'),  # Function-based view
    path('pagina5/', views.pagina5, name='pagina5'),  # Function-based view
    path('modificar/<int:pk>/', views.modificar_tipo, name='modificar_tipo'),
    path('eliminar/<int:pk>/', views.eliminar_tipo, name='eliminar_tipo'),     
]