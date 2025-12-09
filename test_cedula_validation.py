# Script de prueba para validaciones de cédula
# Este script verifica que las validaciones implementadas funcionen correctamente

from django.test import TestCase
from core.forms import ArbitroForm, JugadorForm
from users.forms import CustomUsuarioCreationForm
from users.models import Usuario

class CedulaValidationTest(TestCase):
    """Pruebas para la validación del campo cédula"""
    
    def setUp(self):
        """Crear un usuario de prueba para verificar duplicados"""
        self.usuario_existente = Usuario.objects.create_user(
            cedula='12345678',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='TestPassword123!'
        )
    
    def test_cedula_solo_numeros(self):
        """Verificar que solo se acepten números"""
        # ArbitroForm
        form = ArbitroForm(data={
            'cedula': '12345ABC',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@example.com',
            'password': 'Password123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('solo debe contener números', str(form.errors['cedula']))
    
    def test_cedula_longitud_minima(self):
        """Verificar longitud mínima de 7 dígitos"""
        form = ArbitroForm(data={
            'cedula': '123456',  # Solo 6 dígitos
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@example.com',
            'password': 'Password123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('entre 7 y 10 dígitos', str(form.errors['cedula']))
    
    def test_cedula_longitud_maxima(self):
        """Verificar longitud máxima de 10 dígitos"""
        form = ArbitroForm(data={
            'cedula': '12345678901',  # 11 dígitos
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@example.com',
            'password': 'Password123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('entre 7 y 10 dígitos', str(form.errors['cedula']))
    
    def test_cedula_no_comienza_con_cero(self):
        """Verificar que no comience con 0"""
        form = ArbitroForm(data={
            'cedula': '01234567',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@example.com',
            'password': 'Password123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('no puede comenzar con 0', str(form.errors['cedula']))
    
    def test_cedula_duplicada(self):
        """Verificar que no se permitan cédulas duplicadas"""
        form = ArbitroForm(data={
            'cedula': '12345678',  # Ya existe en setUp
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan2@example.com',
            'password': 'Password123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('ya está registrada', str(form.errors['cedula']))
    
    def test_cedula_valida(self):
        """Verificar que una cédula válida sea aceptada"""
        form = ArbitroForm(data={
            'cedula': '27654321',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@example.com',
            'password': 'Password123!'
        })
        # Nota: Puede fallar por otras validaciones (email, password, etc.)
        # pero no debe fallar por la cédula
        if not form.is_valid():
            self.assertNotIn('cedula', form.errors)
    
    def test_jugador_form_cedula_validation(self):
        """Verificar que JugadorForm también valide correctamente"""
        form = JugadorForm(data={
            'cedula': 'ABC123',
            'first_name': 'María',
            'last_name': 'González',
            'email': 'maria@example.com',
            'telefono': '0414-1234567',
            'categoria_jugador': 'adulto',
            'ranking': 100,
            'password': 'Password123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
    
    def test_custom_usuario_creation_form_cedula_validation(self):
        """Verificar que CustomUsuarioCreationForm también valide correctamente"""
        form = CustomUsuarioCreationForm(data={
            'cedula': '0123456',
            'email': 'nuevo@example.com',
            'first_name': 'Pedro',
            'last_name': 'Martínez',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'role': 'es_jugador'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('no puede comenzar con 0', str(form.errors['cedula']))


# Casos de prueba manual para verificar en el navegador:
"""
CASOS DE PRUEBA MANUAL:

1. Cédula con letras:
   - Ingresar: "12345ABC"
   - Resultado esperado: Error "La cédula solo debe contener números"

2. Cédula muy corta:
   - Ingresar: "12345"
   - Resultado esperado: Error "La cédula debe tener entre 7 y 10 dígitos"

3. Cédula muy larga:
   - Ingresar: "12345678901"
   - Resultado esperado: Error "La cédula debe tener entre 7 y 10 dígitos"

4. Cédula que comienza con 0:
   - Ingresar: "01234567"
   - Resultado esperado: Error "La cédula no puede comenzar con 0"

5. Cédula duplicada:
   - Ingresar una cédula que ya existe en el sistema
   - Resultado esperado: Error "Esta cédula ya está registrada"

6. Cédula válida:
   - Ingresar: "27654321"
   - Resultado esperado: Validación exitosa (sin errores de cédula)

FORMULARIOS A PROBAR:
- Registro de Árbitro (ArbitroForm)
- Registro de Jugador (JugadorForm)
- Registro de Usuario (CustomUsuarioCreationForm)
"""
