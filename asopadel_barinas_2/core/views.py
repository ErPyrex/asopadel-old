# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from .models import Hero, Noticia, Torneo, Cancha, Usuario, Partido, ReservaCancha
from .forms import HeroForm, NoticiaForm, TorneoForm, CanchaForm, PartidoForm, ReservaCanchaForm
from users.forms import CustomUsuarioCreationForm, CustomUsuarioChangeForm
from .forms import JugadorForm, ArbitroForm
from core.forms import ReservaCanchaForm
from django.utils import timezone

# 🔐 Funciones auxiliares para verificar roles
def is_admin(user):
    return user.is_authenticated and user.es_admin_aso

def is_arbitro(user):
    return user.is_authenticated and user.es_arbitro

def is_jugador(user):
    return user.is_authenticated and user.es_jugador

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
    canchas = Cancha.objects.all()
    return render(request, 'users/panel_admin.html', {
        'total_jugadores': total_jugadores,
        'total_arbitros': total_arbitros,
        'total_canchas': total_canchas,
        'total_torneos': total_torneos,
        'canchas': canchas, 
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

from datetime import date

@login_required
@user_passes_test(is_admin)
def admin_delete_tournament(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)

    # Validación usando propiedad dinámica
    if torneo.estado_actual != 'pendiente':
        messages.error(request, "Solo puedes eliminar torneos que no han iniciado.")
        return redirect('core:admin_torneos_list')

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

def is_jugador(user):
    return user.is_authenticated and user.es_jugador

from core.models import EstadisticaJugador, Torneo

@login_required
@user_passes_test(is_jugador)
def jugador_dashboard(request):
    reservas = ReservaCancha.objects.filter(jugador=request.user)
    partidos = Partido.objects.filter(jugadores=request.user)
    estadisticas = EstadisticaJugador.objects.filter(jugador=request.user).first()
    torneos = Torneo.objects.filter(jugadores_inscritos=request.user)

    return render(request, 'users/panel_jugador.html', {
        'reservas': reservas,
        'partidos': partidos,
        'estadisticas': estadisticas,
        'torneos': torneos,
    })







# ====================================================================================
#torneo
@login_required
@user_passes_test(is_jugador)
def inscribirse_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    torneo.jugadores_inscritos.add(request.user)
    messages.success(request, "Te has inscrito exitosamente en el torneo.")
    return redirect('core:jugador_dashboard') 

@login_required
@user_passes_test(is_jugador)
def desinscribirse_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    if request.user in torneo.jugadores_inscritos.all():
        torneo.jugadores_inscritos.remove(request.user)
        messages.success(request, "Has sido desinscrito del torneo.")
    else:
        messages.warning(request, "No estabas inscrito en este torneo.")
    return redirect('core:jugador_dashboard')

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import ReservaCancha

def is_jugador(user):
    return user.is_authenticated and user.es_jugador

@login_required
@user_passes_test(is_jugador)
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(ReservaCancha, id=reserva_id, jugador=request.user)
    if request.method == 'POST':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.success(request, "Reserva cancelada correctamente.")
        return redirect('core:jugador_dashboard')
    return render(request, 'core/reserva/confirmar_cancelar.html', {'reserva': reserva})







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
        return redirect('core:admin_referee_list')
    return render(request, 'core/arbitros/crear_arbitro.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_edit_referee(request, arbitro_id):
    arbitro = get_object_or_404(Usuario, id=arbitro_id, es_arbitro=True)
    form = ArbitroForm(request.POST or None, request.FILES or None, instance=arbitro)
    if form.is_valid():
        form.save()
        messages.success(request, "Árbitro actualizado exitosamente.")
        return redirect('core:admin_referee_list')
    return render(request, 'core/arbitros/editar_arbitro.html', {'form': form, 'arbitro': arbitro})

@login_required
@user_passes_test(is_admin)
def admin_delete_referee(request, arbitro_id):
    arbitro = get_object_or_404(Usuario, id=arbitro_id, es_arbitro=True)
    if request.method == 'POST':
        arbitro.delete()
        messages.success(request, "Árbitro eliminado exitosamente.")
        return redirect('core:admin_referee_list')
    return render(request, 'core/arbitros/confirmar_eliminar_arbitro.html', {'arbitro': arbitro})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def is_arbitro(user):
    return user.is_authenticated and user.es_arbitro

    
    from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from core.models import Partido, Torneo, Cancha

def is_arbitro(user):
    return user.is_authenticated and user.es_arbitro

@login_required
@user_passes_test(is_arbitro)
def arbitro_dashboard(request):
    hoy = timezone.now().date()

    partidos_proximos = Partido.objects.filter(
        arbitro=request.user,
        fecha__gte=hoy
    ).order_by('fecha')

    partidos_finalizados = Partido.objects.filter(
        arbitro=request.user,
        fecha__lt=hoy,
        marcador=''
    ).order_by('-fecha')

    torneos = Torneo.objects.filter(
        id__in=Partido.objects.filter(arbitro=request.user).values('torneo')
    ).distinct()

    canchas = Cancha.objects.all()

    return render(request, 'users/panel_arbitro.html', {
        'partidos_proximos': partidos_proximos,
        'partidos_finalizados': partidos_finalizados,  # ✅ esta línea es clave
        'torneos': torneos,
        'canchas': canchas,
    })
    
    
    #resultado#########
    
    from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from core.forms import ResultadoForm
from core.models import Partido

@login_required
@user_passes_test(is_arbitro)
def registrar_resultado(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id, arbitro=request.user)

    if partido.fecha > timezone.now().date():
        messages.error(request, "Solo puedes registrar resultados de partidos ya finalizados.")
        return redirect('core:arbitro_dashboard')

    form = ResultadoForm(request.POST or None, instance=partido)
    if form.is_valid():
        partido.estado = 'finalizado'  # ✅ actualiza el estado del partido
        form.save()
        messages.success(request, "Resultado registrado correctamente.")
        return redirect('core:arbitro_dashboard')

    return render(request, 'arbitros/registrar_resultado.html', {
        'form': form,
        'partido': partido
    })
    
    
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

        cancha_id_post = request.POST.get('cancha')
        if cancha_id_post:
            reserva.cancha = get_object_or_404(Cancha, id=cancha_id_post)
        elif cancha:
            reserva.cancha = cancha
        else:
            messages.error(request, "No se seleccionó ninguna cancha.")
            return render(request, 'core/reservas/reservar_cancha.html', {
                'form': form,
                'cancha': None
            })

        reserva.save()
        messages.success(request, "Reserva realizada exitosamente.")
        return redirect('users:perfil')

    return render(request, 'core/reservas/reservar_cancha.html', {
        'form': form,
        'cancha': cancha
    })
    
    from django.shortcuts import get_object_or_404

@login_required
@user_passes_test(lambda u: u.es_jugador)
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(ReservaCancha, id=reserva_id, jugador=request.user)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")
    return redirect('users:perfil')
    
    
    #### from django.core.paginator import Paginator
    
from django.core.paginator import Paginator

@login_required
@user_passes_test(is_admin)
def admin_player_list(request):
    query = request.GET.get('q')
    jugadores = Usuario.objects.filter(es_jugador=True)

    if query:
        jugadores = jugadores.filter(first_name__icontains=query)

    paginator = Paginator(jugadores, 10)  # 10 jugadores por página
    page = request.GET.get('page')
    jugadores_paginados = paginator.get_page(page)

    return render(request, 'core/jugadores/jugadores.html', {
        'jugadores': jugadores_paginados,
        'query': query  # para mantener el valor en el input de búsqueda
    })
      
    
#### hero y noticias  ### 
@login_required
@user_passes_test(is_admin)
def admin_edit_hero(request):
    hero = Hero.objects.filter(activo=True).first()
    form = HeroForm(request.POST or None, request.FILES or None, instance=hero)
    if form.is_valid():
        form.save()
        messages.success(request, "Hero actualizado exitosamente.")
        return redirect('core:admin_dashboard')
    return render(request, 'core/hero/editar_hero.html', {'form': form})

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


@login_required
@user_passes_test(is_admin)
def admin_edit_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    form = NoticiaForm(request.POST or None, request.FILES or None, instance=noticia)
    if form.is_valid():
        form.save()
        messages.success(request, "Noticia actualizada exitosamente.")
        return redirect('core:admin_noticias_list')
    return render(request, 'core/noticias/crear_noticia.html', {'form': form, 'noticia': noticia})

@login_required
@user_passes_test(is_admin)
def admin_delete_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        noticia.delete()
        messages.success(request, "Noticia eliminada exitosamente.")
        return redirect('core:admin_noticias_list')
    return render(request, 'core/noticias/confirmar_eliminar_noticia.html', {'noticia': noticia})



from django.shortcuts import render
from .models import Hero, Noticia, Cancha, Torneo

def home(request):
    hero_activo = Hero.objects.filter(activo=True).first()
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:3]  # solo las 3 más recientes
    canchas = Cancha.objects.all()
    torneos = Torneo.objects.order_by('-fecha_inicio')[:5]  # opcional si quieres mostrar torneos

    context = {
        'hero_activo': hero_activo,
        'noticias': noticias,
        'canchas': canchas,
        'torneos': torneos,
    }
    return render(request, 'home.html', context)

###### arbitro dashboard #########
@login_required
@user_passes_test(is_arbitro)
def detalles_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id, arbitro=request.user)
    return render(request, 'arbitros/detalles_partido.html', {'partido': partido})

@login_required
@user_passes_test(is_arbitro)
def calendario_cancha(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    reservas = ReservaCancha.objects.filter(cancha=cancha).order_by('fecha', 'hora_inicio')
    return render(request, 'arbitros/calendario_cancha.html', {'cancha': cancha, 'reservas': reservas})

@login_required
@user_passes_test(is_arbitro)
def estado_canchas(request):
    canchas = Cancha.objects.all()
    return render(request, 'arbitros/estado_cancha.html', {'canchas': canchas})

@login_required
@user_passes_test(is_arbitro)
def lista_partidos_arbitrados(request):
    partidos = Partido.objects.filter(arbitro=request.user).order_by('-fecha')
    return render(request, 'arbitros/lista_partido.html', {'partidos': partidos})

@login_required
@user_passes_test(is_arbitro)
def torneos_asignados(request):
    torneos = Torneo.objects.filter(arbitro=request.user)
    return render(request, 'arbitros/torneo_asignado.html', {'torneos': torneos})

# calendario cancha estado arbitro
@login_required
@user_passes_test(is_arbitro)
def calendario_cancha(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    reservas = ReservaCancha.objects.filter(cancha=cancha).order_by('fecha', 'hora_inicio')
    return render(request, 'core/arbitros/calendario_cancha.html', {
        'cancha': cancha,
        'reservas': reservas
    })
#calendario cancha estado admin
@login_required
@user_passes_test(is_admin)
def admin_estado_canchas(request):
    canchas = Cancha.objects.all()
    return render(request, 'core/arbitros/estado_cancha.html', {'canchas': canchas})