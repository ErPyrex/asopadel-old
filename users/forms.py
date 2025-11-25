from django import forms
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

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            'cedula', 'email', 'first_name', 'last_name',
        )

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

# 🟢 Edición de perfil de usuario
class CustomUsuarioChangeForm(UserChangeForm):
    """Formulario para la edición de un usuario existente."""
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = (
            'cedula', 'email', 'first_name', 'last_name',
            'telefono', 'categoria_jugador', 'ranking', 'foto', 'biografia',
            'es_admin_aso', 'es_arbitro', 'es_jugador',
            'is_active', 'is_staff', 'is_superuser'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['es_admin_aso', 'es_arbitro', 'es_jugador']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-check-input'})