from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('empresas/', views.empresas, name='add'),
    path('empresas/<str:url>', views.empresa, name='add'),
    path('empresas/<str:url>/<str:proyecto>', views.proyecto, name='add'),
    path('registro/', views.registro, name='add'),
]
