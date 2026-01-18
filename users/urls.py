from django.urls import path
from . import views
from . import admin_management
from django.contrib.auth.views import LogoutView


# Ya no necesitamos importar HttpResponse o login_personalizado aquí,
# porque la lógica de autenticación está en views.py

app_name = 'users' # ¡Crucial para que LOGIN_URL = 'users:login' funcione en settings.py!

urlpatterns = [
    # URLs de Autenticación
    # Esta es tu vista de login personalizada (CustomLoginView)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Esta es tu vista de registro de usuarios
    path('register/', views.register_user, name='register'),
    
    # URL para perfil de usuario (si la gestionas aquí, no en core)
    # Si 'perfil_usuario' es una vista en users/views.py para que un usuario vea/edite su propio perfil.
    path('perfil/', views.perfil_usuario, name='perfil'),
    
    # Admin Management (only for superusers)
    path('admin-management/', admin_management.admin_management, name='admin_management'),
    path('admin-management/promote/<int:user_id>/', admin_management.promote_to_admin, name='promote_to_admin'),
    path('admin-management/demote/<int:user_id>/', admin_management.demote_from_admin, name='demote_from_admin'),
    
]