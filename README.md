# ASOPADEL

Sistema para la Asociación de Pádel de Barinas

## Como instalar el proyecto

### Requerimientos

* **Python** (versión 3.10 o superior recomendada)
* **Git** (para clonar el repositorio)
* **Pip** (para instalar las dependencias)
* **Virtualenv** (para crear un entorno virtual)
* **PostgreSQL** (para la base de datos)

### Instalación

1. **Clonar el repositorio**

    ```bash
    git clone [https://github.com/ErPyrex/asopadel.git](https://github.com/ErPyrex/asopadel.git)
    ```

2. **Entrar al directorio del proyecto**

    ```bash
    cd asopadel
    ```

3. **Crear y activar el entorno virtual**
    * **Windows:**

        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```

        *(Nota: Si recibes un error de permisos en PowerShell, ejecuta primero: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

        Una vez activado:

        ```powershell
        pip install -r requirements.txt
        ```

    * **Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```

4. **Configurar variables de entorno (.env)**

    Genera una clave secreta ejecutando este comando en tu terminal:

    ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que `manage.py`) y pega el siguiente contenido. Asegúrate de reemplazar `pegatuclaveaqui` con la clave que generaste arriba:

    ```env
    SECRET_KEY=pegatuclaveaqui
    DEBUG=True
    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/asopadel_barinas
    ```

    **Nota Importante:**
    * El proyecto usa `dj-database-url` para leer la configuración de la base de datos desde `DATABASE_URL`
    * Para instalación manual, usa `localhost` como host (como se muestra arriba)
    * Para Docker, las variables de entorno se configuran automáticamente en `docker-compose.yml`
    * El formato de `DATABASE_URL` es: `postgresql://usuario:contraseña@host:puerto/nombre_base_datos`

5. **Configurar la Base de Datos**
    Necesitamos crear la base de datos `asopadel_barinas` y asegurar que el usuario `postgres` tenga la contraseña `postgres` para coincidir con el archivo `.env`.

    * **Windows:**
        1. Abre la aplicación **SQL Shell (psql)** desde el menú inicio o ejecuta `psql -U postgres` en tu terminal.
        2. Ingresa la contraseña que definiste al instalar PostgreSQL (no se verá al escribir).
        3. Ejecuta los siguientes comandos SQL:

            ```sql
            CREATE DATABASE asopadel_barinas;
            ALTER USER postgres WITH PASSWORD 'postgres';
            \q
            ```

    * **Linux:**
        Ejecuta en tu terminal:

        ```bash
        sudo -u postgres psql
        ```

        Una vez dentro de la consola de Postgres:

        ```sql
        CREATE DATABASE asopadel_barinas;
        ALTER USER postgres WITH PASSWORD 'postgres';
        \q
        ```

6. **Crear las tablas (Migraciones)**

    ```bash
    python manage.py migrate
    ```

7. **Ejecutar el servidor**

    ```bash
    python manage.py runserver
    ```

## Instalación y ejecución con Docker

Esta es la forma recomendada para levantar el proyecto, ya que simplifica la gestión de la base de datos y las dependencias del sistema.

### Requerimientos de Docker

* **Docker Engine** y **Docker Compose**

#### Instalación de Docker

* **Windows:**
    Se recomienda instalar **Docker Desktop**. Puedes seguir la guía oficial:
    [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)
    Asegúrate de que WSL 2 (Windows Subsystem for Linux 2) esté habilitado.

* **Linux:**
    Sigue la guía de instalación para tu distribución:
  * **Ubuntu:** [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
  * **Debian:** [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)
  * **Fedora:** [https://docs.docker.com/engine/install/fedora/](https://docs.docker.com/engine/install/fedora/)

    Después de instalar, es crucial seguir los pasos de post-instalación para poder ejecutar Docker sin `sudo`:
    [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)

### Pasos para ejecutar el proyecto con Docker

1. **Clonar el repositorio y entrar al directorio**
    (Si ya lo hiciste para la instalación manual, puedes omitir este paso)

    ```bash
    git clone https://github.com/ErPyrex/asopadel.git
    cd asopadel
    ```

2. **Construir y levantar los contenedores**
    Este comando construirá las imágenes y levantará los servicios (la aplicación y la base de datos).

    ```bash
    docker-compose up --build
    ```

    *La opción `--build` solo es necesaria la primera vez o si se hacen cambios en el `Dockerfile` o `requirements.txt`.*

    **Nota:** Las migraciones se aplican automáticamente al iniciar el contenedor gracias al script `entrypoint.sh`. No necesitas ejecutarlas manualmente.

3. **Crear un superusuario (IMPORTANTE)**
    Para acceder al panel de administración y gestionar otros administradores, necesitas crear un superusuario.

    Abre una **nueva terminal** (sin detener los contenedores) y ejecuta:

    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

    El sistema te pedirá la siguiente información:
    * **Cédula:** Tu número de identificación (será tu usuario de login)
    * **Email:** Tu correo electrónico
    * **Nombre:** Tu primer nombre
    * **Apellido:** Tu apellido
    * **Contraseña:** Mínimo 8 caracteres (no se mostrará al escribir)
    * **Confirmar contraseña:** Repite la contraseña

    **Ejemplo:**

    ```
    Cédula: 12345678
    Email: admin@asopadel.com
    Nombre: Juan
    Apellido: Administrador
    Password: ********
    Password (again): ********
    Superuser created successfully.
    ```

    > **Nota:** Solo los superusuarios pueden crear y gestionar otros administradores desde el panel web.

4. **¡Listo!**
    La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

    **Para detener los contenedores:**

    ```bash
    docker-compose down
    ```

    **Para volver a iniciar (sin rebuild):**

    ```bash
    docker-compose up
    ```

5. **Ejecutar Tests (Opcional)**

    El proyecto incluye 43 tests automatizados. Para ejecutarlos desde Docker:

    **En Linux/macOS:**

    ```bash
    # Ejecutar todos los tests
    docker compose exec web python manage.py test users --verbosity=2
    
    # Tests específicos
    docker compose exec web python manage.py test users.test_models
    docker compose exec web python manage.py test users.test_forms
    docker compose exec web python manage.py test users.test_views
    ```

    **En Windows (PowerShell):**

    ```powershell
    # Ejecutar todos los tests
    docker compose exec web python manage.py test users --verbosity=2
    
    # Tests específicos
    docker compose exec web python manage.py test users.test_models
    docker compose exec web python manage.py test users.test_forms
    docker compose exec web python manage.py test users.test_views
    ```

    **En Windows (CMD):**

    ```cmd
    REM Ejecutar todos los tests
    docker compose exec web python manage.py test users --verbosity=2
    
    REM Tests específicos
    docker compose exec web python manage.py test users.test_models
    ```

    **Resultado esperado:**

    ```
    Creating test database...
    test_create_user (users.test_models.UsuarioManagerTestCase) ... ok
    test_register_jugador_success (users.test_views.RegistrationViewTestCase) ... ok
    ...
    ----------------------------------------------------------------------
    Ran 43 tests in 2.345s
    
    OK
    ```

## Obligatorio

* Por favor usen ramas de git para trabajar en el proyecto.

* **No usen el main** para trabajar directamente.
* Sigan el flujo de trabajo de **GitHub Flow**.
* Las ramas deben ser nombradas con el siguiente formato:
  * `feature/nombre-del-feature`
  * `bugfix/nombre-del-bugfix`
  * `release/nombre-del-release`
* Los commits deben ser nombrados con el siguiente formato:
  * `feat: nombre del feature`
  * `fix: nombre del bugfix`
  * `refactor: nombre del refactor`
* Las ramas deben ser creadas desde el `main`.
* Las ramas deben ser borradas después de ser fusionadas.
* Solo serán fusionadas ramas cuando pasen los tests.
