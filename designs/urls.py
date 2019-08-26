from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('empresas/', views.empresas, name='empresas'),
    path('empresas/<str:url>', views.empresa, name='empresa'),
    path('empresas/<str:url>/nuevo_proyecto/', views.nuevo_proyecto, name='add_project'),
    path('empresas/<str:url>/<int:idproyecto>', views.proyecto, name='view_project'),
    path('empresas/<str:url>/<int:idproyecto>/eliminar', views.eliminar_proyecto, name='delete_project'),
    path('empresas/<str:url>/<int:idproyecto>/nuevo_design', views.nuevo_design, name='add_design'),
    path('registro/', views.registro, name='register'),
    path('salir/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('login/', views.custom_login, name='login'),
    path('dowload_image/<str:tipo>/<int:id>', views.dowload_image, name='login'),
    path('disenos/', views.get_designs, name='disenos'),
    path('diseno-act/', views.put_designs, name='diseno-act'),
]
