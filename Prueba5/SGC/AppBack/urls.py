from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página de inicio o /pagina1
    path('pagina1/', views.home, name='home'),  # Página de inicio o /pagina1
    path('pagina2/', views.pagina2, name='pagina2'),  # Function-based view
    path('pagina3/', views.Pagina3View.as_view(), name='pagina3'),  # Class-based view
]