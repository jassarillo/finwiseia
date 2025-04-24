from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm  # Importamos el nuevo formulario
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import generate_audio  # Importar la función de views.py
from .views import contacto_empresa , mensaje_exito
from django.urls import path
from django.shortcuts import render


urlpatterns = [
    path('', views.home, name='home'),
    path("contacto-empresa/", contacto_empresa, name="contacto_empresa"),
    path("mensaje-exito/", mensaje_exito, name="mensaje_exito"),
    path('home_f', views.home_f, name='home_f'),
    path('generate-audio/', generate_audio, name='generate_audio'),
    path('Terms/', views.Terms, name='Terms'),
    path('Aviso/', views.Aviso, name='Aviso'),
    path('Mi/', views.Mi, name='Mi'),
    path('Cookies/', views.Cookies, name='Cookies'),
    path('Reglamento/', views.Reglamento, name='Reglamento'),
    path('BlogF/', views.BlogF, name='BlogF'),
    path('PFIN/', views.PFIN, name='PFIN'),
    path('CFUNC/', views.CFUNC, name='CFUNC'),
    path('Soporte/', views.Soporte, name='Soporte'),
    path('At_Em/',views.At_Em, name='At_Em'),
    path('Contacto/', views.Contacto, name='Contacto'),
    path('Beneficioss/', views.Beneficioss, name='Beneficioss'),
    path('Preg_Freqs/', views.Preg_Freqs, name='Preg_Freqs'),
    path('PP/', views.PP, name='PP'),
]

# Solo añade esta parte si estás en modo DEBUG (desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    