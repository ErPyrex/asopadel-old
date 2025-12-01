from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    UsuarioViewSet,
    TorneoViewSet,
    PartidoViewSet,
    CanchaViewSet,
    ReservaCanchaViewSet,
    NoticiaViewSet,
    HeroViewSet,
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'torneos', TorneoViewSet, basename='torneo')
router.register(r'partidos', PartidoViewSet, basename='partido')
router.register(r'canchas', CanchaViewSet, basename='cancha')
router.register(r'reservas', ReservaCanchaViewSet, basename='reserva')
router.register(r'noticias', NoticiaViewSet, basename='noticia')
router.register(r'heroes', HeroViewSet, basename='hero')

urlpatterns = [
    # JWT Authentication endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Router URLs (includes all viewsets)
    path('', include(router.urls)),
]
