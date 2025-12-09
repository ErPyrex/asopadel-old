from django.test import TestCase, Client
from django.urls import reverse
from users.models import Usuario


class RegistrationViewTestCase(TestCase):
    """Tests for the registration view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.register_url = reverse('users:register')

    def test_register_page_loads(self):
        """Test that registration page loads successfully"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_jugador_success(self):
        """Test successful registration as jugador"""
        response = self.client.post(self.register_url, {
            'cedula': '12345678',
            'email': 'jugador@test.com',
            'first_name': 'Test',
            'last_name': 'Jugador',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'es_jugador',
            'telefono': '04141234567'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Usuario.objects.filter(cedula='12345678').exists())
        user = Usuario.objects.get(cedula='12345678')
        self.assertTrue(user.es_jugador)
        self.assertFalse(user.es_admin_aso)

    def test_register_arbitro_success(self):
        """Test successful registration as arbitro"""
        response = self.client.post(self.register_url, {
            'cedula': '87654321',
            'email': 'arbitro@test.com',
            'first_name': 'Test',
            'last_name': 'Árbitro',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'es_arbitro',
            'telefono': '04127654321'
        })
        self.assertEqual(response.status_code, 302)
        user = Usuario.objects.get(cedula='87654321')
        self.assertTrue(user.es_arbitro)
        self.assertFalse(user.es_admin_aso)

    def test_cannot_register_as_admin(self):
        """Test that users cannot register as admin through the form"""
        # Try to register with admin role (should fail)
        response = self.client.post(self.register_url, {
            'cedula': '99999999',
            'email': 'admin@test.com',
            'first_name': 'Test',
            'last_name': 'Admin',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'role': 'es_admin_aso',  # This should not be a valid choice
            'telefono': '04169876543'
        })
        # Form should be invalid
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertFalse(Usuario.objects.filter(cedula='99999999').exists())


class LoginViewTestCase(TestCase):
    """Tests for the login view"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.login_url = reverse('users:login')
        self.user = Usuario.objects.create_user(
            cedula='11111111',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_with_cedula(self):
        """Test login using cedula"""
        response = self.client.post(self.login_url, {
            'username': '11111111',  # Cedula
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_wrong_password(self):
        """Test login with wrong password"""
        response = self.client.post(self.login_url, {
            'username': '11111111',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class AdminManagementViewTestCase(TestCase):
    """Tests for admin management views"""

    def setUp(self):
        """Set up test client and users"""
        self.client = Client()
        
        # Create superuser
        self.superuser = Usuario.objects.create_superuser(
            cedula='00000000',
            password='superpass123',
            email='super@example.com',
            first_name='Super',
            last_name='User'
        )
        
        # Create regular admin
        self.admin = Usuario.objects.create_user(
            cedula='11111111',
            password='adminpass123',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        self.admin.es_admin_aso = True
        self.admin.is_staff = True
        self.admin.save()
        
        # Create regular user
        self.regular_user = Usuario.objects.create_user(
            cedula='22222222',
            password='userpass123',
            email='user@example.com',
            first_name='Regular',
            last_name='User',
            es_jugador=True
        )
        
        self.admin_management_url = reverse('users:admin_management')

    def test_admin_management_requires_login(self):
        """Test that admin management requires authentication"""
        response = self.client.get(self.admin_management_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_admin_management_requires_superuser(self):
        """Test that only superusers can access admin management"""
        # Login as regular admin (not superuser)
        self.client.login(username='11111111', password='adminpass123')
        response = self.client.get(self.admin_management_url)
        self.assertEqual(response.status_code, 302)  # Redirect away
        
        # Logout and login as superuser
        self.client.logout()
        self.client.login(username='00000000', password='superpass123')
        response = self.client.get(self.admin_management_url)
        self.assertEqual(response.status_code, 200)  # Success

    def test_superuser_can_view_admin_list(self):
        """Test that superuser can view list of admins"""
        self.client.login(username='00000000', password='superpass123')
        response = self.client.get(self.admin_management_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin User')  # Regular admin should be listed

    def test_promote_user_to_admin(self):
        """Test promoting a regular user to admin"""
        self.client.login(username='00000000', password='superpass123')
        promote_url = reverse('users:promote_to_admin', args=[self.regular_user.id])
        
        # User should not be admin initially
        self.assertFalse(self.regular_user.es_admin_aso)
        
        # Promote user
        response = self.client.post(promote_url)
        self.assertEqual(response.status_code, 302)  # Redirect back
        
        # Check user is now admin
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.es_admin_aso)
        self.assertTrue(self.regular_user.is_staff)
        self.assertFalse(self.regular_user.is_superuser)  # Should NOT be superuser

    def test_demote_admin_to_regular_user(self):
        """Test demoting an admin to regular user"""
        self.client.login(username='00000000', password='superpass123')
        demote_url = reverse('users:demote_from_admin', args=[self.admin.id])
        
        # User should be admin initially
        self.assertTrue(self.admin.es_admin_aso)
        
        # Demote user
        response = self.client.post(demote_url)
        self.assertEqual(response.status_code, 302)  # Redirect back
        
        # Check user is no longer admin
        self.admin.refresh_from_db()
        self.assertFalse(self.admin.es_admin_aso)
        self.assertFalse(self.admin.is_staff)

    def test_cannot_demote_superuser(self):
        """Test that superusers cannot be demoted through the interface"""
        self.client.login(username='00000000', password='superpass123')
        
        # Create another superuser
        another_super = Usuario.objects.create_superuser(
            cedula='99999999',
            password='super2pass123',
            email='super2@example.com',
            first_name='Another',
            last_name='Super'
        )
        
        demote_url = reverse('users:demote_from_admin', args=[another_super.id])
        response = self.client.post(demote_url)
        
        # Superuser should still be superuser
        another_super.refresh_from_db()
        self.assertTrue(another_super.is_superuser)
        self.assertTrue(another_super.es_admin_aso)

    def test_regular_user_cannot_promote(self):
        """Test that regular users cannot promote others"""
        self.client.login(username='22222222', password='userpass123')
        promote_url = reverse('users:promote_to_admin', args=[self.regular_user.id])
        response = self.client.post(promote_url)
        self.assertEqual(response.status_code, 302)  # Redirect away
        
        # User should not be promoted
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.es_admin_aso)


class PerfilViewTestCase(TestCase):
    """Tests for the user profile view"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = Usuario.objects.create_user(
            cedula='33333333',
            password='testpass123',
            email='profile@example.com',
            first_name='Profile',
            last_name='User'
        )
        self.perfil_url = reverse('users:perfil')

    def test_perfil_requires_login(self):
        """Test that profile view requires authentication"""
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_perfil_loads_for_authenticated_user(self):
        """Test that authenticated users can view their profile"""
        self.client.login(username='33333333', password='testpass123')
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/perfil.html')
