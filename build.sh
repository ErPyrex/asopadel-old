#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Create superuser if environment variables are set
if [ "$DJANGO_SUPERUSER_CEDULA" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Configuring superuser (Cedula: $DJANGO_SUPERUSER_CEDULA)..."
    python manage.py shell <<EOF
from users.models import Usuario
import os

cedula = os.environ.get('DJANGO_SUPERUSER_CEDULA')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
first_name = os.environ.get('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
last_name = os.environ.get('DJANGO_SUPERUSER_LAST_NAME', 'Asopadel')

user, created = Usuario.objects.get_or_create(
    cedula=cedula,
    defaults={
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'is_staff': True,
        'is_superuser': True,
        'es_admin_aso': True
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f"✅ Superusuario {cedula} creado exitosamente.")
else:
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.es_admin_aso = True
    user.save()
    print(f"ℹ️ El superusuario {cedula} ya existía. Se ha actualizado su contraseña y permisos.")
EOF
fi