"""
Revisa la URL de logout con reverse('logout') y simula login+logout con el test client.
Ejecutar con: .\venv\Scripts\python.exe tools\check_logout_flow.py
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ferreteria.settings')
import django
django.setup()
from django.urls import reverse, resolve
from django.test import Client
from django.contrib.auth import get_user_model

try:
    path = reverse('logout')
except Exception as e:
    path = f'REVERSE_ERROR: {e}'

print('REVERSE_LOGOUT:', path)

# listar patrones básicos (intentar resolver the path)
if not path.startswith('REVERSE_ERROR'):
    try:
        match = resolve(path)
        print('RESOLVED_VIEW:', match.view_name, match.func)
    except Exception as e:
        print('RESOLVE_ERROR:', e)

# probar login + logout
User = get_user_model()
user, created = User.objects.update_or_create(username='admin', defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True})
user.set_password('admin')
user.save()

client = Client()
login_ok = client.login(username='admin', password='admin')
print('LOGIN_OK:', login_ok)
# status before
r = client.get('/')
print('AUTH_BEFORE:', getattr(r.wsgi_request, 'user', None) and r.wsgi_request.user.is_authenticated)
# perform POST logout
if not path.startswith('REVERSE_ERROR'):
    r2 = client.post(path, follow=True)
    print('LOGOUT_POST_STATUS:', r2.status_code)
    r3 = client.get('/')
    print('AUTH_AFTER:', getattr(r3.wsgi_request, 'user', None) and r3.wsgi_request.user.is_authenticated)
else:
    print('NO_LOGOUT_PATH')

