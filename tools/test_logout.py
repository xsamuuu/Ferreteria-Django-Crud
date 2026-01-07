"""
Script de prueba para verificar logout vía POST.
Ejecutar con: .\venv\Scripts\python.exe tools\test_logout.py
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ferreteria.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
# Crear o actualizar admin
u, created = User.objects.update_or_create(username='admin', defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True})
u.set_password('admin')
u.save()
print('ADMIN_CREATED' if created else 'ADMIN_UPDATED')

c = Client()
# intentar login usando client.login (usa backend de auth)
ok = c.login(username='admin', password='admin')
print('CLIENT_LOGIN', ok)
# comprobar user autenticado antes
r = c.get('/')
print('AUTH_BEFORE:', getattr(r.wsgi_request, 'user', None) and r.wsgi_request.user.is_authenticated)
# realizar logout vía POST a la URL de logout integrada en auth
path = reverse('custom_logout')
print('LOGOUT_PATH', path)
r2 = c.post(path, follow=True)
print('LOGOUT_POST_STATUS:', r2.status_code)
# comprobar user después
r3 = c.get('/')
print('AUTH_AFTER:', getattr(r3.wsgi_request, 'user', None) and r3.wsgi_request.user.is_authenticated)
print('SESSION_KEYS:', list(c.session.keys()))
