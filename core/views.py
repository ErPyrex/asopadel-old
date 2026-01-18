# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from blog.models import Noticia
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from users.models import Usuario
from .forms import NoticiaForm, TorneoForm, CanchaForm, PartidoSchedulingForm, PartidoResultForm, ReservaCanchaForm
from users.forms import CustomUsuarioCreationForm
from users.forms_admin import AdminUsuarioChangeForm
from .forms import JugadorForm, ArbitroForm
from .utils import IsAdmin, IsArbitro, IsJugador, IsAdminOrArbitro

# Aliases for backward compatibility with existing code
is_admin = IsAdmin
is_arbitro = IsArbitro
is_jugador = IsJugador
is_admin_or_arbitro = IsAdminOrArbitro

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
# 🌐 Vistas públicas
# ====================================================================================
def public_tournament_list(request):
    torneos = Torneo.objects.all()
    return render(request, 'core/torneos/public_torneos_list.html', {'torneos': torneos})

def public_court_list(request):
    canchas = Cancha.objects.all()
    return render(request, 'core/torneos/public_canchas_list.html', {'canchas': canchas})

def public_court_detail(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    return render(request, 'core/canchas/detalle_cancha.html', {'cancha': cancha})

def public_noticias_list(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'core/noticias/public_noticias_list.html', {'noticias': noticias})

def public_noticia_detail(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(request, 'core/noticias/public_noticia_detail.html', {'noticia': noticia})

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



@login_required
@user_passes_test(is_arbitro)
def arbitro_dashboard(request):
    """
    Dashboard view for referees (arbitros).
    Show assigned tournaments and court status.
    """
    torneos = Torneo.objects.filter(arbitro=request.user)
    canchas = Cancha.objects.all()
    
    return render(request, 'users/panel_arbitro.html', {
        'torneos': torneos,
        'canchas': canchas,
    })


# ====================================================================================
# 🗓️ Crear partido
# ====================================================================================
@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_create_match(request):
    """
    Vista para agendar un partido (sin resultado).
    Estado inicial: 'pendiente'.
    """
    form = PartidoSchedulingForm(request.POST or None)
    if form.is_valid():
        partido = form.save(commit=False)
        partido.estado = 'pendiente'  # Force pending state
        partido.save()
        form.save_m2m() # Save ManyToMany (jugadores)
        messages.success(request, "Partido agendado exitosamente.")
        return redirect('core:admin_partidos_list')
    return render(request, 'core/partidos/crear_partido.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_match_list(request):
    """Lista todos los partidos con filtros opcionales"""
    partidos = Partido.objects.all().select_related('torneo', 'cancha', 'arbitro').prefetch_related('equipo1', 'equipo2')
    
    # Filtros opcionales
    torneo_id = request.GET.get('torneo')
    estado = request.GET.get('estado')
    
    if torneo_id:
        try:
            torneo_id = int(torneo_id)
            partidos = partidos.filter(torneo_id=torneo_id)
        except ValueError:
            torneo_id = None
    
    if estado:
        partidos = partidos.filter(estado=estado)
    
    # Ordenar por fecha y hora
    partidos = partidos.order_by('-fecha', '-hora')
    
    # Obtener torneos para el filtro y marcar el seleccionado
    torneos = Torneo.objects.all()
    torneos_list = []
    for torneo in torneos:
        torneos_list.append({
            'id': torneo.id,
            'nombre': torneo.nombre,
            'selected': torneo_id == torneo.id if torneo_id else False
        })
    
    # Estados disponibles y marcar seleccionado
    estados_choices = Partido._meta.get_field('estado').choices
    estados_list = []
    for value, label in estados_choices:
        estados_list.append({
            'value': value,
            'label': label,
            'selected': estado == value if estado else False
        })
    
    context = {
        'partidos': partidos,
        'torneos': torneos_list,
        'estados': estados_list,
        'torneo_filtro': torneo_id,
        'estado_filtro': estado,
    }
    
    return render(request, 'core/partidos/lista_partidos.html', context)

@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_match_detail(request, partido_id):
    """Muestra los detalles de un partido específico"""
    partido = get_object_or_404(Partido, id=partido_id)
    
    context = {
        'partido': partido,
    }
    
    return render(request, 'core/partidos/detalle_partido.html', context)

@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_edit_match(request, partido_id):
    """Edita los detalles de agenda de un partido existente"""
    partido = get_object_or_404(Partido, id=partido_id)
    
    if request.method == 'POST':
        form = PartidoSchedulingForm(request.POST, instance=partido)
        if form.is_valid():
            form.save()
            messages.success(request, "Detalles del partido actualizados exitosamente.")
            return redirect('core:admin_partidos_list')
    else:
        form = PartidoSchedulingForm(instance=partido)
    
    context = {
        'form': form,
        'partido': partido,
    }
    
    return render(request, 'core/partidos/editar_partido.html', context)


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_pending_results_list(request):
    """
    Lista de partidos pendientes o confirmados que necesitan carga de resultados.
    """
    partidos = Partido.objects.filter(estado__in=['pendiente', 'confirmado']).order_by('fecha', 'hora')
    return render(request, 'core/partidos/lista_pendientes_resultados.html', {'partidos': partidos})


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_record_result(request, partido_id):
    """
    Vista para cargar el resultado de un partido.
    Cambia el estado a 'finalizado'.
    """
    partido = get_object_or_404(Partido, id=partido_id)
    
    if request.method == 'POST':
        form = PartidoResultForm(request.POST, instance=partido)
        if form.is_valid():
            partido = form.save(commit=False)
            partido.estado = 'finalizado'
            partido.save()
            messages.success(request, "Resultado cargado y partido finalizado.")
            return redirect('core:admin_pending_results_list')
    else:
        form = PartidoResultForm(instance=partido)
    
    return render(request, 'core/partidos/cargar_resultado.html', {'form': form, 'partido': partido})

@login_required
@user_passes_test(is_admin)
def admin_delete_match(request, partido_id):
    """Elimina un partido con confirmación"""
    partido = get_object_or_404(Partido, id=partido_id)
    
    if request.method == 'POST':
        partido.delete()
        messages.success(request, "Partido eliminado exitosamente.")
        return redirect('core:admin_partidos_list')
    
    context = {
        'partido': partido,
    }
    
    return render(request, 'core/partidos/confirmar_eliminar_partido.html', context)

# ====================================================================================
# 🧑‍🎾 Reserva de Canchas (Jugador)
# ====================================================================================
@login_required
def player_reserve_court(request):
    """Permite al jugador reservar una cancha con validación visual"""
    cancha_id = request.GET.get('cancha_id')
    cancha = None
    if cancha_id:
        cancha = get_object_or_404(Cancha, id=cancha_id)

    form = ReservaCanchaForm(request.POST or None, initial={'cancha': cancha})

    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.jugador = request.user
        # Si el form trae cancha usala, sino la del GET, sino error
        if not reserva.cancha and cancha:
            reserva.cancha = cancha
            
        reserva.save()
        messages.success(request, "Reserva realizada exitosamente.")
        return redirect('core:player_reservations')

    return render(request, 'core/reservas/reservar_cancha.html', {
        'form': form,
        'cancha': cancha
    })

@login_required
def player_reservation_list(request):
    """Lista el historial de reservas del jugador"""
    # Reservas futuras (pendientes o confirmadas)
    reservas_activas = ReservaCancha.objects.filter(
        jugador=request.user, 
        fecha__gte=datetime.date.today()
    ).exclude(estado='cancelada').order_by('fecha', 'hora_inicio')
    
    # Historial (pasadas o canceladas)
    historial = ReservaCancha.objects.filter(
        jugador=request.user
    ).exclude(id__in=reservas_activas.values_list('id', flat=True)).order_by('-fecha', '-hora_inicio')
    
    return render(request, 'core/reservas/mis_reservas.html', {
        'activas': reservas_activas,
        'historial': historial
    })

@login_required
def player_cancel_reservation(request, reserva_id):
    """Permite cancelar una reserva propia"""
    reserva = get_object_or_404(ReservaCancha, id=reserva_id, jugador=request.user)
    
    if request.method == 'POST':
        # Validar que no sea del pasado
        if reserva.fecha < datetime.date.today():
             messages.error(request, "No puedes cancelar reservas pasadas.")
        else:
            reserva.estado = 'cancelada'
            reserva.save()
            messages.success(request, "Reserva cancelada exitosamente.")
        return redirect('core:player_reservations')
        
    return render(request, 'core/reservas/confirmar_cancelacion.html', {'reserva': reserva})

def ranking(request):
    """Vista pública del ranking de jugadores"""
    categoria_filtro = request.GET.get('categoria')
    
    # Base query: Jugadores activos ordenados por ranking
    jugadores = Usuario.objects.filter(es_jugador=True).prefetch_related('estadisticas').order_by('-ranking')
    
    if categoria_filtro:
        jugadores = jugadores.filter(categoria_jugador=categoria_filtro)
    
    # Inyectar estadística principal
    for jugador in jugadores:
        stats = next((s for s in jugador.estadisticas.all() if str(s.categoria_id) == str(jugador.categoria_jugador)), None)
        if not stats and jugador.estadisticas.exists():
            stats = jugador.estadisticas.first()
        jugador.stats_display = stats
    
    # Obtener opciones de categoría desde el modelo
    categorias = Usuario._meta.get_field('categoria_jugador').choices
    
    context = {
        'jugadores': jugadores,
        'categorias': categorias,
        'filtro_actual': categoria_filtro,
    }
    return render(request, 'core/ranking.html', context)

def player_public_profile(request, player_id):
    """Perfil público con estadísticas detalladas"""
    jugador = get_object_or_404(Usuario, id=player_id, es_jugador=True)
    
    # Estadísticas globales (suma de todas las categorías)
    stats_qs = jugador.estadisticas.all()
    total_victorias = sum(s.victorias for s in stats_qs)
    total_derrotas = sum(s.derrotas for s in stats_qs)
    total_jugados = sum(s.partidos_jugados for s in stats_qs)
    
    # Estadisticas calculadas
    efectividad = round((total_victorias / total_jugados * 100), 1) if total_jugados > 0 else 0
    ratio = round(total_victorias / total_derrotas, 2) if total_derrotas > 0 else total_victorias
    
    # Historial de partidos (donde sea jugador)
    ultimos_partidos = Partido.objects.filter(
        Q(equipo1=jugador) | Q(equipo2=jugador),
        estado='finalizado'
    ).distinct().order_by('-fecha')[:10]
    
    context = {
        'jugador': jugador,
        'total_jugados': total_jugados,
        'total_victorias': total_victorias,
        'total_derrotas': total_derrotas,
        'efectividad': efectividad,
        'ratio': ratio,
        'ultimos_partidos': ultimos_partidos
    }
    return render(request, 'core/jugador_perfil.html', context)
    
    
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
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:1]  # solo la más reciente
    canchas = Cancha.objects.all()
    torneos = Torneo.objects.order_by('-fecha_inicio')[:5]  # opcional si quieres mostrar torneos
    
    # Obtener Top 10 del ranking
    ranking = Usuario.objects.filter(es_jugador=True).order_by('-ranking')[:10]

    # Obtener últimos partidos
    partidos = Partido.objects.all().select_related('torneo', 'cancha').prefetch_related('equipo1', 'equipo2').order_by('-fecha', '-hora')[:10]

    context = {
        'noticias': noticias,
        'canchas': canchas,
        'torneos': torneos,
        'ranking': ranking,
        'partidos': partidos,
    }
    return render(request, 'home.html', context)