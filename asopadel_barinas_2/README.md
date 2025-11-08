ASOPADAL BARINAS 

ENTORNO VIRTUAL
python -m venv venv

Activar
.\venv\Scripts\activate

Instalar dependencias
pip install Django Pillow

Migrar
python manage.py makemigrations users core  
python manage.py migrate

Crear superusuario (admin)
python manage.py createsuperuser
**uno de los datos del super usuari eso cedula este es el que se esta usando para iniciar sesio**

Correr el servidor
python manage.py runserver


