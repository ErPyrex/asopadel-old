# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from blog.models import Noticia
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from users.models import Usuario
from .forms import NoticiaForm, TorneoForm, CanchaForm, PartidoForm, ReservaCanchaForm
from users.forms import CustomUsuarioCreationForm
from users.forms_admin import AdminUsuarioChangeForm
from .forms import JugadorForm, ArbitroForm
from .utils import IsAdmin, IsArbitro, IsJugador

# Aliases for backward compatibility with existing code
is_admin = IsAdmin
is_arbitro = IsArbitro
is_jugador = IsJugador

# 🧭 Redirección por rol
@login_required
def dashboard_by_role(request):
    if is_admin(request.user):
        return redirect('core:admin_dashboard')
    elif is_arbitro(request.user):
        return redirect('core:arbitro_dashboard')
    elif is_jugador(request.user):
        return redirect('core:jugador_dashboard')
    return redirect('core:home')


# ====================================================================================
# 🏠 Vista pública del home
# ====================================================================================
def home_page(request):
    canchas = Cancha.objects.all()
    return render(request, 'home.html', {'canchas': canchas})

# ====================================================================================
# 🌐 Vistas públicas
# ====================================================================================
def public_tournament_list(request):
    torneos = Torneo.objects.all()
    return render(request, 'core/torneos/public_torneos_list.html', {'torneos': torneos})

def public_court_list(request):
    canchas = Cancha.objects.all()
    return render(request, 'core/torneos/public_canchas_list.html', {'canchas': canchas})

def public_ranking_list(request):
    return render(request, 'core/torneos/public_ranking_list.html', {})  # Agrega datos reales cuando estén listos

# ====================================================================================
# 🧑‍💼 Dashboards por rol
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_jugadores = Usuario.objects.filter(es_jugador=True).count()
    total_arbitros = Usuario.objects.filter(es_arbitro=True).count()
    total_canchas = Cancha.objects.count()
    total_torneos = Torneo.objects.count()
    return render(request, 'users/panel_admin.html', {
        'total_jugadores': total_jugadores,
        'total_arbitros': total_arbitros,
        'total_canchas': total_canchas,
        'total_torneos': total_torneos,
    })



# ====================================================================================
# 🏆 Gestión de Torneos (Admin)
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_tournament_list(request):
    torneos = Torneo.objects.all()
    return render(request, 'core/torneos/torneos.html', {'torneos': torneos})

@login_required
@user_passes_test(is_admin)
def admin_create_tournament(request):
    form = TorneoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Torneo creado exitosamente.")
        return redirect('core:admin_torneos_list')
    return render(request, 'core/torneos/crear_torneo.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_edit_tournament(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    form = TorneoForm(request.POST or None, instance=torneo)
    if form.is_valid():
        form.save()
        messages.success(request, "Torneo actualizado exitosamente.")
        return redirect('core:admin_torneos_list')
    return render(request, 'core/torneos/crear_torneo.html', {'form': form, 'torneo': torneo})

@login_required
@user_passes_test(is_admin)
def admin_delete_tournament(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    if request.method == 'POST':
        torneo.delete()
        messages.success(request, "Torneo eliminado exitosamente.")
        return redirect('core:admin_torneos_list')
    return render(request, 'core/torneos/confirmar_eliminar_torneo.html', {'torneo': torneo})

# ====================================================================================
# 🏟️ Gestión de Canchas (Admin)
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_court_list(request):
    canchas = Cancha.objects.all()
    return render(request, 'core/canchas/lista_canchas.html', {'canchas': canchas})

@login_required
@user_passes_test(is_admin)
def admin_create_court(request):
    form = CanchaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Cancha creada exitosamente.")
        return redirect('core:admin_canchas_list')
    return render(request, 'core/canchas/crear_cancha.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_edit_court(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    form = CanchaForm(request.POST or None, request.FILES or None, instance=cancha)
    if form.is_valid():
        form.save()
        messages.success(request, "Cancha actualizada exitosamente.")
        return redirect('core:admin_canchas_list')
    return render(request, 'core/canchas/crear_cancha.html', {'form': form, 'cancha': cancha})

@login_required
@user_passes_test(is_admin)
def admin_delete_court(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    if request.method == 'POST':
        cancha.delete()
        messages.success(request, "Cancha eliminada exitosamente.")
        return redirect('core:admin_canchas_list')
    return render(request, 'core/canchas/confirmar_eliminar_cancha.html', {'cancha': cancha})

# ====================================================================================
# 🎾 Gestión de Jugadores (Admin)
# ====================================================================================

@login_required
@user_passes_test(is_admin)
def admin_player_list(request):
    jugadores = Usuario.objects.filter(es_jugador=True)
    return render(request, 'core/jugadores/jugadores.html', {'jugadores': jugadores})

@login_required
@user_passes_test(is_admin)
def admin_create_player(request):
    form = JugadorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Jugador creado exitosamente.")
        return redirect('core:admin_player_list')
    return render(request, 'core/jugadores/crear_jugador.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_edit_player(request, jugador_id):
    jugador = get_object_or_404(Usuario, id=jugador_id, es_jugador=True)
    form = JugadorForm(request.POST or None, request.FILES or None, instance=jugador)
    if form.is_valid():
        form.save()
        messages.success(request, "Jugador actualizado exitosamente.")
        return redirect('core:admin_player_list')
    return render(request, 'core/jugadores/crear_jugador.html', {'form': form, 'jugador': jugador})

@login_required
@user_passes_test(is_admin)
def admin_delete_player(request, jugador_id):
    jugador = get_object_or_404(Usuario, id=jugador_id, es_jugador=True)
    if request.method == 'POST':
        jugador.delete()
        messages.success(request, "Jugador eliminado exitosamente.")
        return redirect('core:admin_player_list')
    return render(request, 'core/jugadores/confirmar_eliminar_jugador.html', {'jugador': jugador})

@login_required
@user_passes_test(is_jugador)
def jugador_dashboard(request):
    """
    Dashboard view for players (jugadores).
    Shows their reservations and matches.
    """
    reservas = ReservaCancha.objects.filter(jugador=request.user)
    partidos = Partido.objects.filter(jugadores=request.user)
    return render(request, 'users/panel_jugador.html', {
        'reservas': reservas,
        'partidos': partidos,
    })

# ====================================================================================
# 🧑‍⚖️ Gestión de Árbitros (Admin)
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_referee_list(request):
    arbitros = Usuario.objects.filter(es_arbitro=True)
    return render(request, 'core/arbitros/lista_arbitro.html', {'arbitros': arbitros})

@login_required
@user_passes_test(is_admin)
def admin_create_referee(request):
    form = ArbitroForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Árbitro creado exitosamente.")
        return redirect('core:admin_arbitros_list')
    return render(request, 'core/arbitros/crear_arbitro.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_edit_referee(request, arbitro_id):
    arbitro = get_object_or_404(Usuario, id=arbitro_id, es_arbitro=True)
    form = ArbitroForm(request.POST or None, request.FILES or None, instance=arbitro)
    if form.is_valid():
        form.save()
        messages.success(request, "Árbitro actualizado exitosamente.")
        return redirect('core:admin_arbitros_list')
    return render(request, 'core/arbitros/editar_arbitro.html', {'form': form, 'arbitro': arbitro})

@login_required
@user_passes_test(is_admin)
def admin_delete_referee(request, arbitro_id):
    arbitro = get_object_or_404(Usuario, id=arbitro_id, es_arbitro=True)
    if request.method == 'POST':
        arbitro.delete()
        messages.success(request, "Árbitro eliminado exitosamente.")
        return redirect('core:admin_arbitros_list')
    return render(request, 'core/arbitros/confirmar_eliminar_arbitro.html', {'arbitro': arbitro})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

@login_required
@user_passes_test(is_arbitro)
def arbitro_dashboard(request):
    """
    Dashboard view for referees (arbitros).
    """
    return render(request, 'users/panel_arbitro.html')


# ====================================================================================
# 🗓️ Crear partido
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_create_match(request):
    form = PartidoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Partido registrado exitosamente.")
        return redirect('core:admin_dashboard')
    return render(request, 'core/partidos/crear_partido.html', {'form': form})

# ====================================================================================
# 🧑‍🎾 Reserva de Canchas (Jugador)
# ====================================================================================
@login_required
@user_passes_test(lambda u: u.es_jugador)
def player_reserve_court(request):
    cancha_id = request.GET.get('cancha_id')
    cancha = None
    if cancha_id:
        cancha = get_object_or_404(Cancha, id=cancha_id)

    form = ReservaCanchaForm(request.POST or None, initial={'cancha': cancha})

    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.jugador = request.user
        reserva.cancha = cancha  # ← asignar cancha si no viene del formulario
        reserva.save()
        messages.success(request, "Reserva realizada exitosamente.")
        return redirect('users:perfil')

    return render(request, 'core/reservas/reservar_cancha.html', {
        'form': form,
        'cancha': cancha
    })
    
    
# Note: admin_player_list is defined above with pagination and search
    
# noticias 

@login_required
@user_passes_test(is_admin)
def admin_noticias_list(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'core/noticias/lista_noticias.html', {'noticias': noticias})

@login_required
@user_passes_test(is_admin)
def admin_create_noticia(request):
    form = NoticiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        noticia = form.save(commit=False)
        noticia.autor = request.user
        noticia.save()
        messages.success(request, "Noticia publicada exitosamente.")
        return redirect('core:admin_noticias_list')
    return render(request, 'core/noticias/crear_noticia.html', {'form': form})

from django.shortcuts import render
from blog.models import Noticia
from facilities.models import Cancha
from competitions.models import Torneo

def home(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:3]  # solo las 3 más recientes
    canchas = Cancha.objects.all()
    torneos = Torneo.objects.order_by('-fecha_inicio')[:5]  # opcional si quieres mostrar torneos

    context = {
        'noticias': noticias,
        'canchas': canchas,
        'torneos': torneos,
    }
    return render(request, 'home.html', context)