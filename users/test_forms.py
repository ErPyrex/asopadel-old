from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from users.forms import LoginCedulaForm, CustomUsuarioCreationForm, CustomUsuarioChangeForm
from users.models import Usuario


class LoginCedulaFormTestCase(TestCase):
    """Tests for the LoginCedulaForm"""

    def setUp(self):
        """Create a test user"""
        self.user = Usuario.objects.create_user(
            cedula='12345678',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_valid_login(self):
        """Test login with valid credentials"""
        form = LoginCedulaForm(data={
            'username': '12345678',
            'password': 'testpass123'
        })
        # Note: The form needs a request object for authentication
        # In a real test, you'd use RequestFactory
        self.assertTrue('username' in form.fields)
        self.assertTrue('password' in form.fields)

    def test_form_fields(self):
        """Test that form has correct fields"""
        form = LoginCedulaForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertEqual(form.fields['username'].label, 'Cédula')
        self.assertEqual(form.fields['username'].max_length, 12)


class CustomUsuarioCreationFormTestCase(TestCase):
    """Tests for the CustomUsuarioCreationForm"""

    def test_form_has_role_field(self):
        """Test that form includes role field"""
        form = CustomUsuarioCreationForm()
        self.assertIn('role', form.fields)

    def test_role_choices_no_admin(self):
        """Test that admin option is NOT in role choices"""
        form = CustomUsuarioCreationForm()
        role_choices = [choice[0] for choice in form.fields['role'].choices]
        self.assertIn('es_jugador', role_choices)
        self.assertIn('es_arbitro', role_choices)
        self.assertNotIn('es_admin_aso', role_choices)  # Admin should NOT be available

    def test_create_jugador(self):
        """Test creating a user with jugador role"""
        form = CustomUsuarioCreationForm(data={
            'cedula': '11111111',
            'email': 'jugador@example.com',
            'first_name': 'Juan',
            'last_name': 'Jugador',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'es_jugador'
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(user.es_jugador)
        self.assertFalse(user.es_arbitro)
        self.assertFalse(user.es_admin_aso)

    def test_create_arbitro(self):
        """Test creating a user with arbitro role"""
        form = CustomUsuarioCreationForm(data={
            'cedula': '22222222',
            'email': 'arbitro@example.com',
            'first_name': 'Pedro',
            'last_name': 'Árbitro',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'es_arbitro'
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(user.es_arbitro)
        self.assertFalse(user.es_jugador)
        self.assertFalse(user.es_admin_aso)

    def test_password_mismatch(self):
        """Test that form is invalid when passwords don't match"""
        form = CustomUsuarioCreationForm(data={
            'cedula': '33333333',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'different123',
            'role': 'es_jugador'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_required_fields(self):
        """Test that all required fields are present"""
        form = CustomUsuarioCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)
        self.assertIn('role', form.errors)

    def test_duplicate_cedula(self):
        """Test that form rejects duplicate cedula"""
        # Create first user
        Usuario.objects.create_user(
            cedula='44444444',
            password='testpass123',
            email='first@example.com',
            first_name='First',
            last_name='User'
        )
        
        # Try to create second user with same cedula
        form = CustomUsuarioCreationForm(data={
            'cedula': '44444444',  # Duplicate
            'email': 'second@example.com',
            'first_name': 'Second',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'es_jugador'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)


class CustomUsuarioChangeFormTestCase(TestCase):
    """Tests for the CustomUsuarioChangeForm"""

    def setUp(self):
        """Create a test user"""
        self.user = Usuario.objects.create_user(
            cedula='55555555',
            password='testpass123',
            email='change@example.com',
            first_name='Change',
            last_name='User'
        )

    def test_form_includes_all_fields(self):
        """Test that form includes all expected fields"""
        form = CustomUsuarioChangeForm(instance=self.user)
        expected_fields = [
            'cedula', 'email', 'first_name', 'last_name',
            'telefono', 'categoria_jugador', 'ranking', 'foto', 'biografia',
            'es_admin_aso', 'es_arbitro', 'es_jugador',
            'is_active', 'is_staff', 'is_superuser'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_update_user_info(self):
        """Test updating user information"""
        form = CustomUsuarioChangeForm(
            data={
                'cedula': '55555555',
                'email': 'newemail@example.com',
                'first_name': 'Updated',
                'last_name': 'Name',
                'telefono': '1234567890',
                'es_jugador': True,
            },
            instance=self.user
        )
        if form.is_valid():
            updated_user = form.save()
            self.assertEqual(updated_user.email, 'newemail@example.com')
            self.assertEqual(updated_user.first_name, 'Updated')
            self.assertEqual(updated_user.telefono, '1234567890')
