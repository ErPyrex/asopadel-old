#!/bin/bash

# Script de configuración para ejecución local (sin Docker)

echo "🔧 Configurando ASOPADEL para ejecución local..."
echo ""

# Paso 1: Verificar PostgreSQL
echo "1️⃣ Verificando PostgreSQL..."
if systemctl is-active --quiet postgresql; then
    echo "✅ PostgreSQL está corriendo"
else
    echo "❌ PostgreSQL no está corriendo"
    echo "   Iniciando PostgreSQL..."
    sudo systemctl start postgresql
    if [ $? -eq 0 ]; then
        echo "✅ PostgreSQL iniciado"
    else
        echo "❌ Error al iniciar PostgreSQL"
        exit 1
    fi
fi
echo ""

# Paso 2: Crear base de datos y usuario
echo "2️⃣ Configurando base de datos..."
echo "   Ejecutando comandos SQL..."

sudo -u postgres psql << EOF
-- Crear base de datos si no existe
SELECT 'CREATE DATABASE asopadel_barinas'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'asopadel_barinas')\gexec

-- Crear usuario si no existe
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'asopadel_user') THEN
        CREATE USER asopadel_user WITH PASSWORD 'postgres';
    END IF;
END
\$\$;

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
ALTER ROLE asopadel_user SET client_encoding TO 'utf8';
ALTER ROLE asopadel_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE asopadel_user SET timezone TO 'America/Caracas';

-- En PostgreSQL 15+, otorgar permisos en el schema public
\c asopadel_barinas
GRANT ALL ON SCHEMA public TO asopadel_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO asopadel_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO asopadel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO asopadel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO asopadel_user;
EOF

if [ $? -eq 0 ]; then
    echo "✅ Base de datos configurada"
else
    echo "❌ Error al configurar base de datos"
    exit 1
fi
echo ""

# Paso 3: Actualizar .env para local
echo "3️⃣ Actualizando archivo .env para ejecución local..."
if [ -f .env ]; then
    # Hacer backup
    cp .env .env.backup
    
    # Actualizar DATABASE_URL para usar localhost
    sed -i 's|@db:|@localhost:|g' .env
    
    echo "✅ Archivo .env actualizado (backup en .env.backup)"
    echo "   DATABASE_URL ahora usa 'localhost' en lugar de 'db'"
else
    echo "❌ Archivo .env no encontrado"
    echo "   Copia .env.example a .env primero"
    exit 1
fi
echo ""

# Paso 4: Crear directorio de logs
echo "4️⃣ Creando directorio de logs..."
mkdir -p logs
echo "✅ Directorio logs/ creado"
echo ""

# Paso 5: Activar entorno virtual e instalar dependencias
echo "5️⃣ Verificando entorno virtual..."
if [ -d "venv" ]; then
    echo "✅ Entorno virtual encontrado"
    echo "   Activando entorno virtual..."
    source venv/bin/activate
    
    echo "   Instalando/actualizando dependencias..."
    pip install -q -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Dependencias instaladas"
    else
        echo "❌ Error al instalar dependencias"
        exit 1
    fi
else
    echo "❌ Entorno virtual no encontrado"
    echo "   Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    echo "✅ Entorno virtual creado y dependencias instaladas"
fi
echo ""

# Paso 6: Aplicar migraciones
echo "6️⃣ Aplicando migraciones..."
python manage.py migrate

if [ $? -eq 0 ]; then
    echo "✅ Migraciones aplicadas"
else
    echo "❌ Error al aplicar migraciones"
    exit 1
fi
echo ""

# Paso 7: Instrucciones finales
echo "✅ ¡Configuración completada!"
echo ""
echo "📝 Próximos pasos:"
echo "   1. Crear superusuario:"
echo "      python manage.py createsuperuser"
echo ""
echo "   2. Ejecutar servidor:"
echo "      python manage.py runserver"
echo ""
echo "   3. Acceder a:"
echo "      http://localhost:8000"
echo ""
echo "💡 Recuerda activar el entorno virtual antes de ejecutar comandos:"
echo "   source venv/bin/activate"
echo ""
