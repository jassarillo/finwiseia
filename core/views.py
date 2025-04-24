from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dotenv import load_dotenv
import os
from .forms import RegistroForm, EmailAuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from gtts import gTTS
from pydub import AudioSegment
from django.conf import settings

# Cargar variables de entorno
load_dotenv()

# Logger simplificado
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Cambiar a ERROR para menos ruido
file_handler = logging.FileHandler("error.log")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Vistas básicas
def home(request):
    return render(request, 'core/PP.html')

def home_f(request):
    return render(request, 'core/home_f.html')

def Aviso(request):
    return render(request, 'core/Aviso.html')

def Terms(request):
    return render(request, 'core/Terms.html')

def Mi(request):
    return render(request, 'core/Mi.html')

def Cookies(request):
    return render(request, 'core/Cookies.html')

def BlogF(request):
    return render(request, 'core/BlogF.html')

def CFUNC(request):
    return render(request, 'core/CFUNC.html')

def Beneficioss(request):
    return render(request, 'core/Beneficioss.html')

def Preg_Freqs(request):
    return render(request, 'core/Preg_Freqs.html')

def Soporte(request):
    return render(request, 'core/Soporte.html')

def At_Em(request):
    return render(request, 'core/At_Em.html')

def Contacto(request):
    return render(request, 'core/Contacto.html')

def PFIN(request):
    return render(request, 'core/PFIN.html')

def Reglamento(request):
    return render(request, 'core/Reglamento.html')


def video(request):
    return render(request, 'core/video.html')

def PP(request):
    return render(request, 'core/PP.html')

def mensaje_exito(request):
    return render(request, "core/mensaje_exito.html")


#AVATAR (FINI)

# Configuración del logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log en archivo
file_handler = logging.FileHandler("error.log")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Log en consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

from django.shortcuts import render, redirect
from core.models import ContactoEmpresa  # Asegúrate de importar el modelo
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def contacto_empresa(request):
    if request.method == "POST":
        empresa = request.POST.get("empresa")
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        country_code = request.POST.get("country_code")
        phone_number = request.POST.get("phone_number")
        role = request.POST.get("role")
        employees = request.POST.get("employees")
        mensaje = request.POST.get("mensaje")

        #  Agregar logs para ver si los datos llegan bien
        logger.info(f" Recibido: empresa={empresa}, nombre={nombre}, email={email}, country_code={country_code}, phone_number={phone_number}, role={role}, employees={employees}, mensaje={mensaje}")

        if not empresa:
            logger.error(" Error: El campo 'empresa' está vacío")
            return render(request, 'PP.html', {'error': 'El campo empresa es obligatorio.'})

        # Guardar en la base de datos
        nuevo_contacto = ContactoEmpresa.objects.create(
            empresa=empresa,
            nombre=nombre,
            email=email,
            country_code=country_code,
            phone_number=phone_number,
            role=role,
            employees=employees,
            mensaje=mensaje
        )

        logger.info(f" Contacto guardado con ID: {nuevo_contacto.id}")

        return redirect('mensaje_exito')

    return render(request, 'PP.html')



# Convertir texto a audio
def text_to_speech(text, output_file="response.mp3"):
    try:
        if not text or not isinstance(text, str):
            logger.error(f" Error: El texto para convertir a voz es inválido: {text}")
            return None
        
        # Reemplazar saltos de línea para mejorar la síntesis de voz
        text = text.replace("\n", " ").replace("\r", " ").strip()
        
        tts = gTTS(text, lang="es")
        
        # Asegurar que la carpeta "media" existe
        media_dir = os.path.join(settings.BASE_DIR, "media")
        os.makedirs(media_dir, exist_ok=True)

        media_path = os.path.join(media_dir, output_file)
        tts.save(media_path)

        if not os.path.exists(media_path):
            logger.error(" Error: El archivo de audio no se generó correctamente.")
            return None

        logger.info(f" Audio generado correctamente: {media_path}")
        return media_path
    except Exception as e:
        logger.error(f" Error en text_to_speech: {e}", exc_info=True)
        return None

# Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Directorios para almacenar archivos
DATA_DIR = os.path.join(settings.BASE_DIR, "core", "data")
UPLOAD_DIR = os.path.join(settings.BASE_DIR, "uploads")

# Crear directorios si no existen
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FINI PAGINA PRINCIPAL

import os
import logging
from django.http import JsonResponse
from django.conf import settings

# Configuración de logs
logger = logging.getLogger(__name__)

def generate_audio(request):
    from .views import text_to_speech  # Importar dentro de la función para evitar problemas de importación

    text = request.GET.get("text", "").strip()
    logger.info(f" Texto recibido para conversión: {text}")

    if not text:
        logger.warning(" Error: Texto vacío recibido.")
        return JsonResponse({"error": "Texto vacío"}, status=400)

    output_file = "response.mp3"
    logger.info(f" Generando audio en: {output_file}")

    # Verificar que la función existe
    if not callable(text_to_speech):
        logger.error(" Error: La función text_to_speech no está definida correctamente.")
        return JsonResponse({"error": "La función text_to_speech no está disponible"}, status=500)

    # Intentar generar el audio
    try:
        audio_path = text_to_speech(text, output_file)
        logger.info(f" Ruta de archivo generada: {audio_path}")
    except Exception as e:
        logger.error(f" Error al generar el audio: {e}", exc_info=True)
        return JsonResponse({"error": "Error interno al generar el audio"}, status=500)

    if not audio_path or not os.path.exists(audio_path):
        logger.error(" No se pudo generar el archivo de audio o no se encuentra en el sistema.")
        return JsonResponse({"error": "No se pudo generar el audio"}, status=500)

    # Construir la URL del archivo de audio
    audio_url = f"/media/{output_file}"
    logger.info(f" Audio generado correctamente: {audio_url}")

    return JsonResponse({"audio_url": audio_url})

#hola