from django import forms
import re
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import Usuario

# 🟢 Login personalizado por cédula
class LoginCedulaForm(AuthenticationForm):
    """Formulario para el login usando Cédula en lugar de username."""
    username = forms.CharField(
        label='Cédula',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Cédula'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.request = request

    def clean(self):
        username = self.cleaned_data.get('username')  # Aquí llega la cédula
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError("Cédula o contraseña incorrecta.")
            self.confirm_login_allowed(user)

        return self.cleaned_data

# 🟢 Registro de usuario
class CustomUsuarioCreationForm(UserCreationForm):
    """Formulario para la creación de un nuevo usuario."""
    ROLE_CHOICES = (
        ('es_jugador', 'Jugador'),
        ('es_arbitro', 'Árbitro'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Tipo de usuario",
        required=True
    )

    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'pattern': '(0414|0424|0412|0416|0426|02[0-9]{2})[0-9]{7}',
            'maxlength': '11',
            'title': 'Debe ser un número válido de Venezuela (Ej: 0414, 0424, 0412, 0416, 0426 o fijos 02xx) seguido de 7 dígitos',
            'placeholder': 'Ej: 04141234567',
            'oninput': "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 11);"
        }),
        label="Teléfono",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password_attrs = {
            'pattern': '(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@#$%^&+=!]).{8,}',
            'title': 'Mínimo 8 caracteres, debe incluir: mayúscula, minúscula, número y símbolo (@#$%^&+=!)',
            'placeholder': 'Ej: MiClave123!'
        }
        # Aplicar a todos los campos de contraseña (password y confirmación)
        for field_name in self.fields:
            if 'password' in field_name:
                self.fields[field_name].widget.attrs.update(password_attrs)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            'cedula', 'email', 'first_name', 'last_name', 'telefono',
        )
        widgets = {
            'cedula': forms.TextInput(attrs={
                'pattern': '[1-9][0-9]{6,9}',
                'title': 'Completa este campo solo usando números, sin , / .* - ni ningún otro símbolo',
                'placeholder': 'Ej: 12345678'
            }),
            'first_name': forms.TextInput(attrs={
                'pattern': '[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,50}',
                'title': 'El nombre solo debe contener letras (mínimo 2 caracteres)',
                'placeholder': 'Ej: Juan'
            }),
            'last_name': forms.TextInput(attrs={
                'pattern': '[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,50}',
                'title': 'El apellido solo debe contener letras (mínimo 2 caracteres)',
                'placeholder': 'Ej: Pérez'
            }),
            'telefono': forms.TextInput(attrs={
                'pattern': '(0414|0424|0412|0416|0426|02[0-9]{2})[0-9]{7}',
                'maxlength': '11',
                'title': 'Debe ser un número válido de Venezuela (Ej: 0414, 0424, 0412, 0416, 0426 o fijos 02xx) seguido de 7 dígitos',
                'placeholder': 'Ej: 04141234567'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'correo@ejemplo.com'
            }),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        
        # Solo números
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números")
        
        # Longitud válida
        if len(cedula) < 7 or len(cedula) > 10:
            raise forms.ValidationError("La cédula debe tener entre 7 y 10 dígitos")
        
        # No puede comenzar con 0
        if cedula.startswith('0'):
            raise forms.ValidationError("La cédula no puede comenzar con 0")
        
        # Verificar que no exista
        if Usuario.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("Esta cédula ya está registrada")
        
        return cedula

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        
        # Verificar que no exista
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado")
        
        # Dominios no permitidos (emails temporales)
        dominios_bloqueados = [
            'tempmail.com', 'guerrillamail.com', '10minutemail.com',
            'throwaway.email', 'mailinator.com', 'maildrop.cc',
            'temp-mail.org', 'getnada.com', 'trashmail.com'
        ]
        dominio = email.split('@')[1]
        if dominio in dominios_bloqueados:
            raise forms.ValidationError("No se permiten emails temporales o desechables")
        
        return email

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name').strip()
        
        # Solo letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo debe contener letras")
        
        # Longitud mínima
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres")
        
        # Capitalizar primera letra
        return nombre.title()

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name').strip()
        
        # Solo letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido):
            raise forms.ValidationError("El apellido solo debe contener letras")
        
        # Longitud mínima
        if len(apellido) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres")
        
        return apellido.title()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            return telefono
            
        # Solo números
        if not telefono.isdigit():
             raise forms.ValidationError("El teléfono solo debe contener números")
             
        # Longitud exacta 11 dígitos
        if len(telefono) != 11:
            raise forms.ValidationError("El teléfono debe tener exactamente 11 dígitos")
            
        # Validar códigos de área permitidos
        prefijos_validos = ['0414', '0424', '0412', '0416', '0426']
        es_movil = any(telefono.startswith(prefijo) for prefijo in prefijos_validos)
        es_fijo = telefono.startswith('02') and len(telefono) == 11
        
        if not (es_movil or es_fijo):
            raise forms.ValidationError("El código de área no es válido. Use 0414, 0424, 0412, 0416, 0426 o fijos (02xx)")
            
        return telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'es_jugador':
            user.es_jugador = True
        elif role == 'es_arbitro':
            user.es_arbitro = True
        # Removed es_admin_aso option - admins can only be created via createsuperuser or admin panel
        if commit:
            user.save()
        return user

# 🟢 Edición de perfil de usuario (SEGURO - sin campos privilegiados)
class UsuarioPerfilForm(forms.ModelForm):
    """
    Safe form for users to edit their own profile.
    Does NOT include role fields or admin permissions to prevent privilege escalation.
    """
    
    class Meta:
        model = Usuario
        fields = (
            'first_name', 'last_name', 'telefono', 
            'foto', 'biografia'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biografía'}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom styling.
        """
        super().__init__(*args, **kwargs)
        # Make cedula and email read-only in the template
        # Users should not be able to change these critical fields
