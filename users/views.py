from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required # Necesitamos este decorador
from .forms import LoginCedulaForm, CustomUsuarioCreationForm, UsuarioPerfilForm # Importa UsuarioPerfilForm
from .models import Usuario # Importa el modelo Usuario

# Vista de Login Personalizada (usando cédula)
class CustomLoginView(LoginView):
    template_name = 'users/login.html' # Asegúrate de tener este template
    form_class = LoginCedulaForm # Usamos nuestro formulario de login con cédula
    redirect_authenticated_user = True

    def form_valid(self, form):
        cedula = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=cedula, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form) # Redirige a LOGIN_REDIRECT_URL
        else:
            messages.error(self.request, "Cédula o contraseña incorrecta.")
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirige al dashboard apropiado según el rol del usuario
        return reverse_lazy('core:dashboard_by_role')

# Vista de Registro de Usuario
def register_user(request):
    if request.user.is_authenticated:
        return redirect('core:home') # No permitir registro si ya está logueado

    if request.method == 'POST':
        form = CustomUsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Por favor, inicia sesión.')
            return redirect('users:login')
    else:
        form = CustomUsuarioCreationForm()
    return render(request, 'users/register.html', {'form': form})

# NUEVA VISTA: Perfil de Usuario
@login_required # Solo usuarios autenticados pueden ver su perfil
def perfil_usuario(request):
    """
    View for users to edit their own profile.
    Uses UsuarioPerfilForm which only allows editing safe fields.
    Prevents privilege escalation by not exposing role or permission fields.
    """
    usuario = request.user # El usuario actualmente logueado
    if request.method == 'POST':
        form = UsuarioPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:perfil') # Redirige de nuevo a la página de perfil
    else:
        form = UsuarioPerfilForm(instance=usuario)
    
    return render(request, 'users/perfil.html', {'form': form, 'usuario': usuario}) # Asegúrate de tener este template