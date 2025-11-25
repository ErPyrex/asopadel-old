from django.test import TestCase
from users.models import Usuario, UsuarioManager


class UsuarioManagerTestCase(TestCase):
    """Tests for the custom Usuario Manager"""

    def test_create_user(self):
        """Test creating a regular user"""
        user = Usuario.objects.create_user(
            cedula='12345678',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.cedula, '12345678')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.es_admin_aso)

    def test_create_user_without_cedula(self):
        """Test that creating a user without cedula raises ValueError"""
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(
                cedula='',
                password='testpass123'
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = Usuario.objects.create_superuser(
            cedula='87654321',
            password='adminpass123',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        self.assertEqual(admin.cedula, '87654321')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.es_admin_aso)

    def test_create_superuser_with_wrong_flags(self):
        """Test that creating superuser with is_staff=False raises ValueError"""
        with self.assertRaises(ValueError):
            Usuario.objects.create_superuser(
                cedula='99999999',
                password='testpass123',
                is_staff=False
            )


class UsuarioModelTestCase(TestCase):
    """Tests for the Usuario model"""

    def setUp(self):
        """Set up test data"""
        self.user = Usuario.objects.create_user(
            cedula='11111111',
            password='testpass123',
            email='player@example.com',
            first_name='Juan',
            last_name='Pérez'
        )

    def test_str_method(self):
        """Test the __str__ method returns cedula"""
        self.assertEqual(str(self.user), '11111111')

    def test_get_full_name(self):
        """Test get_full_name property"""
        self.assertEqual(self.user.get_full_name, 'Juan Pérez')

    def test_get_short_name(self):
        """Test get_short_name property"""
        self.assertEqual(self.user.get_short_name, 'Juan')

    def test_jugador_role(self):
        """Test setting jugador role"""
        self.user.es_jugador = True
        self.user.save()
        self.assertTrue(self.user.es_jugador)
        self.assertFalse(self.user.es_arbitro)
        self.assertFalse(self.user.es_admin_aso)

    def test_arbitro_role(self):
        """Test setting arbitro role"""
        self.user.es_arbitro = True
        self.user.save()
        self.assertTrue(self.user.es_arbitro)
        self.assertFalse(self.user.es_jugador)
        self.assertFalse(self.user.es_admin_aso)

    def test_admin_role(self):
        """Test setting admin role"""
        self.user.es_admin_aso = True
        self.user.is_staff = True
        self.user.save()
        self.assertTrue(self.user.es_admin_aso)
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_multiple_roles(self):
        """Test that a user can have multiple roles"""
        self.user.es_jugador = True
        self.user.es_arbitro = True
        self.user.save()
        self.assertTrue(self.user.es_jugador)
        self.assertTrue(self.user.es_arbitro)

    def test_categoria_jugador_choices(self):
        """Test categoria_jugador field choices"""
        self.user.categoria_jugador = 'juvenil'
        self.user.save()
        self.assertEqual(self.user.categoria_jugador, 'juvenil')

        self.user.categoria_jugador = 'adulto'
        self.user.save()
        self.assertEqual(self.user.categoria_jugador, 'adulto')

        self.user.categoria_jugador = 'senior'
        self.user.save()
        self.assertEqual(self.user.categoria_jugador, 'senior')

    def test_ranking_default(self):
        """Test that ranking defaults to 0"""
        self.assertEqual(self.user.ranking, 0)

    def test_unique_cedula(self):
        """Test that cedula must be unique"""
        with self.assertRaises(Exception):
            Usuario.objects.create_user(
                cedula='11111111',  # Same as self.user
                password='testpass123',
                email='another@example.com',
                first_name='Another',
                last_name='User'
            )

    def test_unique_email(self):
        """Test that email must be unique"""
        with self.assertRaises(Exception):
            Usuario.objects.create_user(
                cedula='22222222',
                password='testpass123',
                email='player@example.com',  # Same as self.user
                first_name='Another',
                last_name='User'
            )
