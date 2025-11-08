from django.urls import path
from . import views
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
    
    # Eliminadas:
    # - path('panel/jugador/', views.panel_jugador, name='panel_jugador'),
    # - path('panel/arbitro/', views.panel_arbitro, name='panel_arbitro'),
    # - path('panel/admin/', views.panel_admin, name='panel_admin'),
    #   -> Estas vistas de dashboards están en core/urls.py.
    # - path('admin/arbitros/', views.gestion_arbitros, name='arbitros'),
    # - path('admin/arbitros/crear/', views.crear_arbitro, name='crear_arbitro'),
    #   -> Estas vistas de gestión de árbitros están en core/urls.py.
    # - path('test/', test_ruta),
    #   -> Eliminado, era solo una ruta de prueba.
]