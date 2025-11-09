# ASOPADEL
Sistema para la Asociación de Pádel de Barinas

## Como instalar el proyecto

### Requerimientos

* **Python** (usen la ultima versión disponible)
* **Git** (para clonar el repositorio)
* **Pip** (para instalar las dependencias)
* **Virtualenv** (para crear un entorno virtual)

### Instalación

1. Clonar el repositorio
    ```
    git clone https://github.com/ErPyrex/asopadel.git
    ```
2. Entrar al directorio del proyecto
3. Crear un entorno virtual:
    - Windows:
        ```
        python -m venv venv

        .\venv\Scripts\activate

        pip install -r requirements.txt
        ```
    - Linux:
        ```
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
4. Genera tu SECRET_KEY
        ```
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        ```
    Copia la clave, crea un archivo .env en la raíz del proyecto con el siguiente contenido:
    ```
    SECRET_KEY=tu_clave
    DEBUG=True
    ```
5. Crear la base de datos
    ```
    python manage.py migrate
    ```
6. Ejecutar el servidor
    ```
    python manage.py runserver
    ```
    
## Obligatorio
    - Por favor usen ramas de git para trabajar en el proyecto.
    - Por favor, no uses el main para trabajar en el proyecto.
    - Sigan el flujo de trabajo de GitHub Flow.
    - Las ramas deben ser nombradas con el siguiente formato:
        * feature/nombre-del-feature
        * bugfix/nombre-del-bugfix
        * release/nombre-del-release
    - Los commits deben ser nombrados con el siguiente formato:
        * feat: nombre del feature
        * fix: nombre del bugfix
        * refactor: nombre del refactor
    - Las ramas deben ser creadas desde el main.
    - Las ramas deben ser borradas despues de ser fusionadas.
    - Solo seran fusionadas ramas cuando pasen los tests. 
