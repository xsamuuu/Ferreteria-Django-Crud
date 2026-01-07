Guía rápida de despliegue (Linux - Debian/Ubuntu)

1) Preparar el servidor
- Actualizar y crear virtualenv
  python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt

2) Variables de entorno
- Copiar `.env.example` a `.env` y ajustar valores.

3) Migraciones y archivos estáticos
- python manage.py migrate
- python manage.py collectstatic --noinput

4) Probar gunicorn localmente
- gunicorn ferreteria.wsgi:application --bind 0.0.0.0:8000 --workers 3

5) Configurar systemd y nginx
- Copiar `deploy/gunicorn.service` a `/etc/systemd/system/gunicorn.service`
- systemctl daemon-reload; systemctl enable --now gunicorn
- Copiar `deploy/nginx.conf` a `/etc/nginx/sites-available/ferreteria` y enlazar
- systemctl restart nginx

Notas:
- Gunicorn no funciona en Windows; usa WSL o un servidor Linux para despliegue.
- psycopg2-binary es conveniente en Windows, pero en producción se recomienda psycopg2 compilado.
- Usa variables de entorno para secretos (no subir .env real a git).

