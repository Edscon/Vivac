from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import logging
import time
from django.conf import settings

from order.models import Order

# Define si el usuario es un superuser
def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required, login_url='/admin/login/')
def dashboard(request):

    orders = Order.objects.all()

    context = {
        'orders': orders,
    }

    return render(request, 'dashboard/dashboard.html', context)

logger = logging.getLogger(__name__)

def complete_form(request):
    if request.method == 'POST':
        try:           
            service = Service(executable_path=ChromeDriverManager().install())
            
            # Configurar las opciones del navegador
            options = Options()

            # Inicializar el controlador de Chrome con el servicio y las opciones
            driver = webdriver.Chrome(service=service, options=options)

            # Navegar a la página de inicio de sesión
            driver.get('https://www.nacex.es/login.do')

            time.sleep(1)  # Ajusta el tiempo si es necesario
            try:
                # Intentar aceptar las cookies
                accept_cookies_button = driver.find_element(By.ID, 'accept')
                accept_cookies_button.click()
                logger.info("Cookies aceptadas")
            except Exception as e:
                logger.warning("No se encontró el aviso de cookies: %s", e)

            try:
                # Encontrar y llenar los campos de usuario y contraseña
                username_field = driver.find_element(By.ID, 'usuario') 
                password_field = driver.find_element(By.ID, 'clave') 
                login_button = driver.find_element(By.XPATH, '//button[@type="button"]')

                username_field.send_keys(settings.NACEX_USER)
                password_field.send_keys(settings.NACEX_PASSWORD)
                login_button.click()
            except Exception as e:
                logger.warning("No se encontró login es posible que ya se esté logueado: %s", e)
            
            time.sleep(2)

            driver.get('https://www.nacex.es/irRecogida.do')

            while True:
                time.sleep(300)
            # No rellenar el formulario, solo dejar el navegador abierto
            return JsonResponse({'status': 'success', 'message': 'Chrome abierto y navegando a la URL especificada'})
        except WebDriverException as e:
            logger.error("Error al abrir Chrome: %s", e)
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)
        except Exception as e:
            logger.error("Error inesperado: %s", e)
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'failed', 'message': 'Método no permitido'}, status=405)