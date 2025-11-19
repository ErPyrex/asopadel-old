from django import forms
# Importa Usuario porque Torneo, Partido y ReservaCancha referencian a Usuario
from users.models import Usuario
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from blog.models import Hero, Noticia

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


class ReservaCanchaForm(forms.ModelForm):
    class Meta:
        model = ReservaCancha
        fields = ['cancha', 'fecha', 'hora_inicio', 'hora_fin', 'jugador']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jugador'].queryset = Usuario.objects.filter(es_jugador=True) # Solo jugadores pueden reservar
        # Si quieres que el campo jugador se auto-rellene para el usuario logueado
        # puedes hacer:
        # if 'request' in self.initial and self.initial['request'].user.is_authenticated:
        #     self.fields['jugador'].initial = self.initial['request'].user
        #     self.fields['jugador'].widget = forms.HiddenInput() # Ocultarlo si es un jugador haciendo su propia reserva
        
        
# core/forms.py  crear formularios de registro para árbitros y jugadores

from django import forms
# from .models import Usuario (Removed)

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