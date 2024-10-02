"""
URL configuration for SGC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
#from .views import TipoIdentificacionViewSet
#from AppBack.views import TipoIdentificacionViewSet
from django.views.generic import TemplateView
#from AppBack.views import login_view #, ProtectedView, welcome_view   ### Agregar tablas (models)
from AppBack.views import get_user_groups

router = DefaultRouter()
#router.register(r'tipos-identificacion', TipoIdentificacionViewSet, basename='tipoidentificacion')
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('AppBack.urls')),  # Incluimos las URLs de AppBack
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/',include('dj_rest_auth.registration.urls')),
    #path('api/welcome/', welcome_view, name='welcome'),
    #path('', TemplateView.as_view(template_name='index.html')),
    #path('api/', include(router.urls)),   
    path('', TemplateView.as_view(template_name='flutter_web/index.html')),
    #path('api/auth/login/', login_view, name='login'), 
    path('api/auth/user/groups/', get_user_groups, name='get_user_groups'),
]



