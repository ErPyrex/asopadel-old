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

4. Ejecutar el servidor
    ```
    python3 manage.py runserver
    ```
