from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from users.models import Usuario
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from blog.models import Noticia, Hero

from .serializers import (
    UsuarioSerializer, UsuarioCreateSerializer,
    TorneoListSerializer, TorneoDetailSerializer,
    PartidoSerializer, CanchaSerializer, ReservaCanchaSerializer,
    NoticiaSerializer, HeroSerializer
)


# ============================================================================
# AUTHENTICATION
# ============================================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to use cedula instead of username.
    """
    username_field = 'cedula'
    
    def validate(self, attrs):
        # Use cedula as username
        credentials = {
            'cedula': attrs.get('cedula'),
            'password': attrs.get('password')
        }
        
        # Get user by cedula
        try:
            user = Usuario.objects.get(cedula=attrs.get('cedula'))
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Cédula o contraseña incorrecta')
        
        # Check password
        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError('Cédula o contraseña incorrecta')
        
        # Generate tokens
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UsuarioSerializer(user).data
        }
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view using cedula instead of username.
    """
    serializer_class = CustomTokenObtainPairSerializer


# ============================================================================
# USER VIEWSETS
# ============================================================================

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Usuario model.
    Provides CRUD operations for users.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Regular users can only see themselves, admins can see all.
        """
        if self.request.user.es_admin_aso or self.request.user.is_staff:
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user information.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Register a new user.
        """
        serializer = UsuarioCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UsuarioSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# TOURNAMENT VIEWSETS
# ============================================================================

class TorneoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Torneo model.
    List uses lightweight serializer, detail uses full serializer.
    """
    queryset = Torneo.objects.all().order_by('-fecha_inicio')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TorneoListSerializer
        return TorneoDetailSerializer
    
    def get_permissions(self):
        """
        Only admins can create, update, or delete tournaments.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]


# ============================================================================
# MATCH VIEWSETS
# ============================================================================

class PartidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Partido model.
    """
    queryset = Partido.objects.all().order_by('-fecha')
    serializer_class = PartidoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Optionally filter by tournament.
        """
        queryset = super().get_queryset()
        torneo_id = self.request.query_params.get('torneo', None)
        if torneo_id:
            queryset = queryset.filter(torneo_id=torneo_id)
        return queryset


# ============================================================================
# COURT VIEWSETS
# ============================================================================

class CanchaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Cancha model.
    """
    queryset = Cancha.objects.all()
    serializer_class = CanchaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReservaCanchaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ReservaCancha model.
    """
    queryset = ReservaCancha.objects.all().order_by('-fecha', '-hora_inicio')
    serializer_class = ReservaCanchaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Users can only see their own reservations unless they're admin.
        """
        if self.request.user.es_admin_aso or self.request.user.is_staff:
            return ReservaCancha.objects.all()
        return ReservaCancha.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically set the current user as the reservation owner.
        """
        serializer.save(usuario=self.request.user)


# ============================================================================
# BLOG/NEWS VIEWSETS
# ============================================================================

class NoticiaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Noticia model.
    """
    queryset = Noticia.objects.all().order_by('-fecha_publicacion')
    serializer_class = NoticiaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HeroViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hero model (homepage hero sections).
    """
    queryset = Hero.objects.filter(activo=True)
    serializer_class = HeroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ============================================================================
# CUSTOM PERMISSIONS
# ============================================================================

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.es_admin_aso or request.user.is_staff)
