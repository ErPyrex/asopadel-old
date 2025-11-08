from django import forms
# Importa Usuario porque Torneo, Partido y ReservaCancha referencian a Usuario
from .models import Usuario, Torneo, Cancha, Partido, ReservaCancha, Hero, Noticia
from core.models import ReservaCancha

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'categoria', 'premios', 'arbitro', 'jugadores_inscritos']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'jugadores_inscritos': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegúrate de que solo los usuarios que son árbitros puedan ser seleccionados
        self.fields['arbitro'].queryset = Usuario.objects.filter(es_arbitro=True)
        # Asegúrate de que solo los usuarios que son jugadores puedan ser seleccionados
        self.fields['jugadores_inscritos'].queryset = Usuario.objects.filter(es_jugador=True)


class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['nombre', 'ubicacion', 'tipo', 'estado', 'imagen']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }
 #partido form
class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['torneo', 'cancha', 'fecha', 'hora', 'jugadores', 'arbitro', 'marcador', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'jugadores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jugadores'].queryset = Usuario.objects.filter(es_jugador=True)
        self.fields['arbitro'].queryset = Usuario.objects.filter(es_arbitro=True)



from django import forms
from core.models import ReservaCancha

class ReservaCanchaForm(forms.ModelForm):
    class Meta:
        model = ReservaCancha
        fields = ['cancha', 'fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'cancha': forms.HiddenInput(),  # se muestra como oculto si viene desde URL
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cancha'].queryset = Cancha.objects.filter(estado='disponible')

        
        
        
        
        
# core/forms.py  crear formularios de registro para árbitros y jugadores

from django import forms
from .models import Usuario

class ArbitroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Usuario
        fields = ['cedula', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.es_arbitro = True
        if commit:
            user.save()
        return user
    
class JugadorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Usuario
        fields = [
            'cedula', 'first_name', 'last_name', 'email',
            'telefono', 'categoria_jugador', 'ranking', 'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.es_jugador = True
        if commit:
            user.save()
        return user
    
class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['titulo', 'subtitulo', 'imagen', 'activo']

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'cuerpo', 'imagen']

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['marcador', 'observaciones']
        widgets = {
            'marcador': forms.TextInput(attrs={
                'placeholder': 'Ej. 6-4, 3-6, 7-5',
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Observaciones del partido (opcional)',
                'class': 'form-control'
            }),
        }