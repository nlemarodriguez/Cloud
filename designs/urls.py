from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('empresas/', views.empresas, name='add'),
    path('empresas/<str:url>', views.empresa, name='add'),
    path('empresas/<str:url>/nuevo_proyecto/', views.nuevo_proyecto, name='add'),
    path('empresas/<str:url>/<int:idproyecto>', views.proyecto, name='add'),
    path('empresas/<str:url>/<int:idproyecto>/eliminar', views.eliminar_proyecto, name='add'),
    path('empresas/<str:url>/<int:idproyecto>/nuevo_design', views.nuevo_design, name='add'),
    path('registro/', views.registro, name='add'),

]
