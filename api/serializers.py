from rest_framework import serializers
from users.models import Usuario
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from blog.models import Noticia, Hero


# ============================================================================
# USER SERIALIZERS
# ============================================================================

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer for Usuario model.
    Excludes sensitive fields and provides read-only access to role fields.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'cedula', 'email', 'first_name', 'last_name', 'full_name',
            'telefono', 'foto', 'biografia',
            'es_admin_aso', 'es_arbitro', 'es_jugador',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'es_admin_aso', 'es_arbitro', 'es_jugador', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users (registration).
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ['cedula', 'email', 'first_name', 'last_name', 'telefono', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(**validated_data, password=password)
        return user


# ============================================================================
# TOURNAMENT SERIALIZERS
# ============================================================================

class TorneoListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for tournament lists.
    """
    total_partidos = serializers.SerializerMethodField()
    
    class Meta:
        model = Torneo
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'total_partidos']
    
    def get_total_partidos(self, obj):
        return obj.partidos.count() if hasattr(obj, 'partidos') else 0


class TorneoDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for tournament detail view.
    """
    partidos = serializers.SerializerMethodField()
    
    class Meta:
        model = Torneo
        fields = '__all__'
    
    def get_partidos(self, obj):
        partidos = obj.partidos.all()[:10]  # Limit to 10 most recent
        return PartidoSerializer(partidos, many=True).data


# ============================================================================
# MATCH SERIALIZERS
# ============================================================================

class PartidoSerializer(serializers.ModelSerializer):
    """
    Serializer for Partido (match) model.
    """
    torneo_nombre = serializers.CharField(source='torneo.nombre', read_only=True)
    cancha_nombre = serializers.CharField(source='cancha.nombre', read_only=True)
    
    class Meta:
        model = Partido
        fields = '__all__'


# ============================================================================
# COURT SERIALIZERS
# ============================================================================

class CanchaSerializer(serializers.ModelSerializer):
    """
    Serializer for Cancha (court) model.
    """
    reservas_activas = serializers.SerializerMethodField()
    
    class Meta:
        model = Cancha
        fields = '__all__'
    
    def get_reservas_activas(self, obj):
        from django.utils import timezone
        return obj.reservas.filter(fecha__gte=timezone.now().date()).count()


class ReservaCanchaSerializer(serializers.ModelSerializer):
    """
    Serializer for ReservaCancha (court reservation) model.
    """
    cancha_nombre = serializers.CharField(source='cancha.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = ReservaCancha
        fields = '__all__'


# ============================================================================
# BLOG/NEWS SERIALIZERS
# ============================================================================

class NoticiaSerializer(serializers.ModelSerializer):
    """
    Serializer for Noticia (news) model.
    """
    autor_nombre = serializers.CharField(source='autor.get_full_name', read_only=True)
    
    class Meta:
        model = Noticia
        fields = '__all__'


class HeroSerializer(serializers.ModelSerializer):
    """
    Serializer for Hero (homepage hero section) model.
    """
    class Meta:
        model = Hero
        fields = '__all__'
