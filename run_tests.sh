#!/bin/bash
# Script para ejecutar todos los tests del proyecto

echo "🧪 Ejecutando tests del proyecto ASOPADEL..."
echo "=============================================="
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "✓ Activando entorno virtual..."
    source venv/bin/activate
fi

# Ejecutar tests de modelos
echo ""
echo "📦 Tests de Modelos..."
python manage.py test users.test_models --verbosity=2

# Ejecutar tests de formularios
echo ""
echo "📝 Tests de Formularios..."
python manage.py test users.test_forms --verbosity=2

# Ejecutar tests de vistas
echo ""
echo "🌐 Tests de Vistas..."
python manage.py test users.test_views --verbosity=2

# Ejecutar todos los tests de users
echo ""
echo "🎯 Ejecutando TODOS los tests de users..."
python manage.py test users --verbosity=2

echo ""
echo "=============================================="
echo "✅ Tests completados!"
