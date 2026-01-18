from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def ValidateImageSize(Image):
    """
    Validator function to check if uploaded image size is within limits.
    Maximum allowed size is 5MB.
    
    Args:
        Image: The uploaded image file
        
    Raises:
        ValidationError: If image size exceeds 5MB
    """
    MaxSizeMb = 5
    MaxSizeBytes = MaxSizeMb * 1024 * 1024  # Convert MB to bytes
    
    if Image.size > MaxSizeBytes:
        raise ValidationError(f'El tamaño máximo permitido es {MaxSizeMb}MB. Tu archivo tiene {Image.size / (1024 * 1024):.2f}MB')


# Manager personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        """
        Create and save a regular user with the given cedula and password.
        
        Args:
            cedula: Venezuelan ID number
            password: User password
            **extra_fields: Additional fields for the user
            
        Returns:
            Usuario: The created user instance
        """
        if not cedula:
            raise ValueError("La cédula es obligatoria")
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password=None, **extra_fields):
        """
        Create and save a superuser with the given cedula and password.
        
        Args:
            cedula: Venezuelan ID number
            password: User password
            **extra_fields: Additional fields for the user
            
        Returns:
            Usuario: The created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('es_admin_aso', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(cedula, password, **extra_fields)

# Modelo de usuario personalizado
class Usuario(AbstractUser):
    username = None  # Eliminamos el campo username heredado
    cedula = models.CharField(max_length=12, unique=True)

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)

    # Roles
    es_admin_aso = models.BooleanField(default=False)
    es_arbitro = models.BooleanField(default=False)
    es_jugador = models.BooleanField(default=False)

    # Datos adicionales
    telefono = models.CharField(max_length=20, blank=True, null=True)
    categoria_jugador = models.CharField(
        max_length=50,
        choices=[
            ('juvenil', 'Juvenil'),
            ('adulto', 'Adulto'),
            ('senior', 'Senior'),
        ],
        blank=True,
        null=True
    )
    ranking = models.IntegerField(default=0, blank=True, null=True)
    
    # Foto de perfil con validación de seguridad
    foto = models.ImageField(
        upload_to='perfiles/', 
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp'],
                message='Solo se permiten archivos de imagen (jpg, jpeg, png, webp)'
            ),
            ValidateImageSize
        ]
    )
    
    biografia = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UsuarioManager()

    def __str__(self):
        return self.cedula

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_short_name(self):
        return self.first_name