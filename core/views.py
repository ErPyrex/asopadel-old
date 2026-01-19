# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from blog.models import Noticia
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from users.models import Usuario
from .forms import (
    NoticiaForm,
    TorneoForm,
    CanchaForm,
    PartidoSchedulingForm,
    PartidoResultForm,
    ReservaCanchaForm,
)
from .forms import JugadorForm, ArbitroForm
from django.utils import timezone
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
        return redirect("core:admin_dashboard")
    elif is_arbitro(request.user):
        return redirect("core:arbitro_dashboard")
    elif is_jugador(request.user):
        return redirect("core:jugador_dashboard")
    return redirect("core:home")


# ====================================================================================
# 🌐 Vistas públicas
# ====================================================================================
def public_tournament_list(request):
    torneos = Torneo.objects.all()
    return render(
        request, "core/torneos/public_torneos_list.html", {"torneos": torneos}
    )


def public_court_list(request):
    canchas = Cancha.objects.all()
    return render(
        request, "core/torneos/public_canchas_list.html", {"canchas": canchas}
    )


def public_court_detail(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    return render(request, "core/canchas/detalle_cancha.html", {"cancha": cancha})


def public_noticias_list(request):
    noticias = Noticia.objects.order_by("-fecha_publicacion")
    return render(
        request, "core/noticias/public_noticias_list.html", {"noticias": noticias}
    )


def public_noticia_detail(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(
        request, "core/noticias/public_noticia_detail.html", {"noticia": noticia}
    )


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
    return render(
        request,
        "users/panel_admin.html",
        {
            "total_jugadores": total_jugadores,
            "total_arbitros": total_arbitros,
            "total_canchas": total_canchas,
            "total_torneos": total_torneos,
            "form": CanchaForm(prefix="court"),
            "noticia_form": NoticiaForm(prefix="news"),
        },
    )


# ====================================================================================
# 🏆 Gestión de Torneos (Admin)
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_tournament_list(request):
    tipo_seleccionado = request.GET.get("tipo", "")
    estado_seleccionado = request.GET.get("activo", "")

    torneos = Torneo.objects.all()

    # Nota: El modelo Torneo no tiene campo 'tipo' o 'activo' actualmente.
    # Si se desea filtrar por tipo (que podría ser categoría) o estado:
    if tipo_seleccionado:
        # Asumiendo que 'tipo' se refiere a la categoría para este ejemplo
        torneos = torneos.filter(categoria__nombre__icontains=tipo_seleccionado)

    if estado_seleccionado == "1":
        # Activo si la fecha_fin >= hoy
        torneos = torneos.filter(fecha_fin__gte=timezone.now().date())
    elif estado_seleccionado == "0":
        # Inactivo si la fecha_fin < hoy
        torneos = torneos.filter(fecha_fin__lt=timezone.now().date())

    # Datos para el modal de creación
    from competitions.models import Categoria

    categorias = Categoria.objects.all()
    arbitros = Usuario.objects.filter(es_arbitro=True, is_active=True)

    return render(
        request,
        "core/torneos/torneos.html",
        {
            "torneos": torneos,
            "tipo_seleccionado": tipo_seleccionado,
            "estado_seleccionado": estado_seleccionado,
            "categorias": categorias,
            "arbitros": arbitros,
        },
    )


@login_required
@user_passes_test(is_admin)
def admin_create_tournament(request):
    form = TorneoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Torneo creado exitosamente.")
        return redirect("core:admin_torneos_list")
    return render(request, "core/torneos/crear_torneo.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def admin_edit_tournament(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    form = TorneoForm(request.POST or None, instance=torneo)
    if form.is_valid():
        form.save()
        messages.success(request, "Torneo actualizado exitosamente.")
        return redirect("core:admin_torneos_list")
    return render(
        request, "core/torneos/crear_torneo.html", {"form": form, "torneo": torneo}
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_tournament(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)
    if request.method == "POST":
        torneo.cancelado = True
        torneo.save()
        messages.success(request, f"Torneo '{torneo.nombre}' cancelado exitosamente.")
        return redirect("core:admin_torneos_list")
    return redirect("core:admin_torneos_list")


# ====================================================================================
# 🏟️ Gestión de Canchas (Admin)
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_court_list(request):
    canchas = Cancha.objects.all()
    form = CanchaForm(prefix="court")
    return render(
        request, "core/canchas/lista_canchas.html", {"canchas": canchas, "form": form}
    )


@login_required
@user_passes_test(is_admin)
def admin_create_court(request):
    form = CanchaForm(request.POST or None, request.FILES or None, prefix="court")
    if form.is_valid():
        form.save()
        messages.success(request, "Cancha creada exitosamente.")
        return redirect("core:admin_canchas_list")
    return render(request, "core/canchas/crear_cancha.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def admin_edit_court(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    if request.method == "POST":
        # Manejar datos del modal o del formulario
        cancha.nombre = request.POST.get("nombre", cancha.nombre)
        cancha.estado = request.POST.get("estado", cancha.estado)
        cancha.ubicacion = request.POST.get("ubicacion", cancha.ubicacion)
        cancha.descripcion = request.POST.get("descripcion", cancha.descripcion)

        # Precio
        precio = request.POST.get("precio_hora")
        if precio:
            cancha.precio_hora = float(precio)

        # Horarios
        apertura = request.POST.get("horario_apertura")
        cierre = request.POST.get("horario_cierre")
        if apertura:
            cancha.horario_apertura = apertura
        if cierre:
            cancha.horario_cierre = cierre

        # Imagen
        if request.FILES.get("imagen"):
            cancha.imagen = request.FILES.get("imagen")

        cancha.save()
        messages.success(request, "Cancha actualizada exitosamente.")
        return redirect("core:admin_canchas_list")

    form = CanchaForm(instance=cancha)
    return render(
        request, "core/canchas/crear_cancha.html", {"form": form, "cancha": cancha}
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_court(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    if request.method == "POST":
        cancha.delete()
        messages.success(request, "Cancha eliminada exitosamente.")
        return redirect("core:admin_canchas_list")
    return render(
        request, "core/canchas/confirmar_eliminar_cancha.html", {"cancha": cancha}
    )


# ====================================================================================
# 🎾 Gestión de Jugadores (Admin)
# ====================================================================================


@login_required
@user_passes_test(is_admin)
def admin_player_list(request):
    jugadores = Usuario.objects.filter(es_jugador=True)
    categorias = Usuario._meta.get_field("categoria_jugador").choices
    return render(
        request,
        "core/jugadores/jugadores.html",
        {"jugadores": jugadores, "categorias": categorias},
    )


@login_required
@user_passes_test(is_admin)
def admin_create_player(request):
    form = JugadorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Jugador creado exitosamente.")
        return redirect("core:admin_player_list")
    return render(request, "core/jugadores/crear_jugador.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def admin_edit_player(request, jugador_id):
    jugador = get_object_or_404(Usuario, id=jugador_id, es_jugador=True)
    form = JugadorForm(request.POST or None, request.FILES or None, instance=jugador)
    if form.is_valid():
        form.save()
        messages.success(request, "Jugador actualizado exitosamente.")
        return redirect("core:admin_player_list")
    return render(
        request, "core/jugadores/crear_jugador.html", {"form": form, "jugador": jugador}
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_player(request, jugador_id):
    jugador = get_object_or_404(Usuario, id=jugador_id, es_jugador=True)
    if request.method == "POST":
        jugador.delete()
        messages.success(request, "Jugador eliminado exitosamente.")
        return redirect("core:admin_player_list")
    return render(
        request, "core/jugadores/confirmar_eliminar_jugador.html", {"jugador": jugador}
    )


@login_required
@user_passes_test(is_admin)
def admin_update_player_category(request, jugador_id):
    """Actualiza la categoría de un jugador desde la lista"""
    if request.method == "POST":
        jugador = get_object_or_404(Usuario, id=jugador_id, es_jugador=True)
        nueva_categoria = request.POST.get("categoria")

        # Validar que la categoría sea válida
        categorias_validas = [
            choice[0] for choice in Usuario._meta.get_field("categoria_jugador").choices
        ]

        if nueva_categoria in categorias_validas:
            jugador.categoria_jugador = nueva_categoria
            jugador.save()
            messages.success(
                request,
                f"Categoría de {jugador.get_full_name()} actualizada a {jugador.get_categoria_jugador_display()}.",
            )
        else:
            messages.error(request, "Categoría no válida.")

    return redirect("core:admin_player_list")


@login_required
@user_passes_test(is_jugador)
def jugador_dashboard(request):
    """
    Dashboard view for players (jugadores).
    Shows their reservations and matches.
    """
    user = request.user
    reservas = ReservaCancha.objects.filter(jugador=user)
    partidos = Partido.objects.filter(Q(equipo1=user) | Q(equipo2=user)).distinct()
    torneos = Torneo.objects.filter(jugadores_inscritos=user)

    from competitions.models import EstadisticaJugador

    estadisticas = EstadisticaJugador.objects.filter(jugador=user).first()

    # Pre-calculate display values to avoid template tag breaking
    display_name = user.first_name if user.first_name else user.username
    full_name = user.get_full_name() if user.get_full_name() else user.username
    categoria = (
        user.get_categoria_jugador_display()
        if hasattr(user, "get_categoria_jugador_display") and user.categoria_jugador
        else "Sin categoría"
    )
    ranking_pts = user.ranking if hasattr(user, "ranking") and user.ranking else 0
    partidos_count = estadisticas.partidos_jugados if estadisticas else 0
    victorias_count = estadisticas.victorias if estadisticas else 0

    return render(
        request,
        "users/panel_jugador.html",
        {
            "reservas": reservas,
            "partidos": partidos,
            "torneos": torneos,
            "estadisticas": estadisticas,
            "display_name": display_name,
            "full_name": full_name,
            "cat": categoria,
            "ranking_pts": ranking_pts,
            "partidos_count": partidos_count,
            "victorias_count": victorias_count,
        },
    )


# ====================================================================================
# 🧑‍⚖️ Gestión de Árbitros (Admin)
# ====================================================================================
@login_required
@user_passes_test(is_admin)
def admin_referee_list(request):
    arbitros = Usuario.objects.filter(es_arbitro=True)
    return render(request, "core/arbitros/lista_arbitro.html", {"arbitros": arbitros})


@login_required
@user_passes_test(is_admin)
def admin_create_referee(request):
    form = ArbitroForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Árbitro creado exitosamente.")
        return redirect("core:admin_arbitros_list")
    return render(request, "core/arbitros/crear_arbitro.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def admin_edit_referee(request, arbitro_id):
    arbitro = get_object_or_404(Usuario, id=arbitro_id, es_arbitro=True)
    form = ArbitroForm(request.POST or None, request.FILES or None, instance=arbitro)
    if form.is_valid():
        form.save()
        messages.success(request, "Árbitro actualizado exitosamente.")
        return redirect("core:admin_arbitros_list")
    return render(
        request, "core/arbitros/editar_arbitro.html", {"form": form, "arbitro": arbitro}
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_referee(request, arbitro_id):
    arbitro = get_object_or_404(Usuario, id=arbitro_id, es_arbitro=True)
    if request.method == "POST":
        arbitro.delete()
        messages.success(request, "Árbitro eliminado exitosamente.")
        return redirect("core:admin_arbitros_list")
    return render(
        request, "core/arbitros/confirmar_eliminar_arbitro.html", {"arbitro": arbitro}
    )


@login_required
@user_passes_test(is_arbitro)
def arbitro_dashboard(request):
    """
    Dashboard view for referees (arbitros).
    Show assigned tournaments and court status.
    """
    torneos = Torneo.objects.filter(arbitro=request.user)
    canchas = Cancha.objects.all()

    return render(
        request,
        "users/panel_arbitro.html",
        {
            "torneos": torneos,
            "canchas": canchas,
        },
    )


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
        partido.estado = "pendiente"  # Force pending state
        partido.save()
        form.save_m2m()  # Save ManyToMany (jugadores)
        messages.success(request, "Partido agendado exitosamente.")
        return redirect("core:admin_partidos_list")
    return render(request, "core/partidos/crear_partido.html", {"form": form})


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_match_list(request):
    """Lista todos los partidos con filtros opcionales"""
    partidos = (
        Partido.objects.all()
        .select_related("torneo", "cancha", "arbitro")
        .prefetch_related("equipo1", "equipo2")
    )

    # Filtros opcionales
    torneo_id = request.GET.get("torneo")
    estado = request.GET.get("estado")

    if torneo_id:
        try:
            torneo_id = int(torneo_id)
            partidos = partidos.filter(torneo_id=torneo_id)
        except ValueError:
            torneo_id = None

    if estado:
        partidos = partidos.filter(estado=estado)

    # Ordenar por fecha y hora
    partidos = partidos.order_by("-fecha", "-hora")

    # Obtener torneos para el filtro y marcar el seleccionado
    torneos = Torneo.objects.all()
    torneos_list = []
    for torneo in torneos:
        torneos_list.append(
            {
                "id": torneo.id,
                "nombre": torneo.nombre,
                "selected": torneo_id == torneo.id if torneo_id else False,
            }
        )

    # Estados disponibles y marcar seleccionado
    estados_choices = Partido._meta.get_field("estado").choices
    estados_list = []
    for value, label in estados_choices:
        estados_list.append(
            {
                "value": value,
                "label": label,
                "selected": estado == value if estado else False,
            }
        )

    # Datos para el modal de creación
    canchas = Cancha.objects.filter(estado="disponible")
    jugadores = Usuario.objects.filter(es_jugador=True).order_by(
        "first_name", "last_name"
    )
    arbitros = Usuario.objects.filter(es_arbitro=True).order_by(
        "first_name", "last_name"
    )
    torneos_modal = Torneo.objects.all()

    # Horarios disponibles
    horarios = [
        ("08:00", "08:00 AM - 10:00 AM"),
        ("10:00", "10:00 AM - 12:00 PM"),
        ("12:00", "12:00 PM - 02:00 PM"),
        ("14:00", "02:00 PM - 04:00 PM"),
        ("16:00", "04:00 PM - 06:00 PM"),
        ("18:00", "06:00 PM - 08:00 PM"),
        ("20:00", "08:00 PM - 10:00 PM"),
    ]

    context = {
        "partidos": partidos,
        "torneos": torneos_list,
        "estados": estados_list,
        "torneo_filtro": torneo_id,
        "estado_filtro": estado,
        # Datos para el modal
        "canchas": canchas,
        "jugadores": jugadores,
        "arbitros": arbitros,
        "torneos_modal": torneos_modal,
        "horarios": horarios,
    }

    return render(request, "core/partidos/lista_partidos.html", context)


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_match_detail(request, partido_id):
    """Muestra los detalles de un partido específico"""
    partido = get_object_or_404(Partido, id=partido_id)

    context = {
        "partido": partido,
    }

    return render(request, "core/partidos/detalle_partido.html", context)


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_edit_match(request, partido_id):
    """Edita los detalles de agenda de un partido existente"""
    partido = get_object_or_404(Partido, id=partido_id)

    if request.method == "POST":
        form = PartidoSchedulingForm(request.POST, instance=partido)
        if form.is_valid():
            form.save()
            messages.success(request, "Detalles del partido actualizados exitosamente.")
            return redirect("core:admin_partidos_list")
    else:
        form = PartidoSchedulingForm(instance=partido)

    context = {
        "form": form,
        "partido": partido,
    }

    return render(request, "core/partidos/editar_partido.html", context)


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_pending_results_list(request):
    """
    Lista de partidos pendientes o confirmados que necesitan carga de resultados.
    """
    partidos = Partido.objects.filter(estado__in=["pendiente", "confirmado"]).order_by(
        "fecha", "hora"
    )
    return render(
        request,
        "core/partidos/lista_pendientes_resultados.html",
        {"partidos": partidos},
    )


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_record_result(request, partido_id):
    """
    Vista para cargar el resultado de un partido.
    Cambia el estado a 'finalizado'.
    """
    partido = get_object_or_404(Partido, id=partido_id)

    if request.method == "POST":
        form = PartidoResultForm(request.POST, instance=partido)
        if form.is_valid():
            partido = form.save(commit=False)
            partido.estado = "finalizado"
            partido.save()
            messages.success(request, "Resultado cargado y partido finalizado.")
            return redirect("core:admin_pending_results_list")
    else:
        form = PartidoResultForm(instance=partido)

    return render(
        request,
        "core/partidos/cargar_resultado.html",
        {"form": form, "partido": partido},
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_match(request, partido_id):
    """Elimina un partido con confirmación"""
    partido = get_object_or_404(Partido, id=partido_id)

    if request.method == "POST":
        partido.delete()
        messages.success(request, "Partido eliminado exitosamente.")
        return redirect("core:admin_partidos_list")

    context = {
        "partido": partido,
    }

    return render(request, "core/partidos/confirmar_eliminar_partido.html", context)


@login_required
@user_passes_test(is_admin)
def admin_cancel_match(request, partido_id):
    """Cancela un partido que no se ha efectuado (solo pendiente/confirmado)"""
    partido = get_object_or_404(Partido, id=partido_id)

    if request.method == "POST":
        # Solo se pueden cancelar partidos que no se han jugado
        if partido.estado in ["pendiente", "confirmado"]:
            partido.estado = "cancelado"
            partido.save()
            messages.success(request, "El partido ha sido cancelado exitosamente.")
        else:
            messages.error(
                request, "No se puede cancelar un partido que ya fue finalizado."
            )
        return redirect("core:admin_partidos_list")

    return redirect("core:admin_partidos_list")


@login_required
@user_passes_test(is_admin_or_arbitro)
def admin_edit_result(request, partido_id):
    """
    Edita el resultado de un partido ya finalizado.
    Árbitros: máximo 2 ediciones por partido.
    Admins/Superadmin: sin límite.
    """
    partido = get_object_or_404(Partido, id=partido_id)
    user = request.user

    # Verificar límite para árbitros (no admins)
    is_admin_user = user.is_staff or user.is_superuser
    max_ediciones_arbitro = 2

    if not is_admin_user and partido.ediciones_resultado >= max_ediciones_arbitro:
        messages.error(
            request,
            f"Has alcanzado el límite de {max_ediciones_arbitro} correcciones para este partido. Contacta a un administrador.",
        )
        return redirect("core:admin_partidos_list")

    if request.method == "POST":
        marcador = request.POST.get("marcador")
        equipo_ganador = request.POST.get("equipo_ganador")

        if marcador:
            partido.marcador = marcador

        # Determinar ganador basado en selección
        if equipo_ganador == "1":
            partido.equipo_ganador = 1
        elif equipo_ganador == "2":
            partido.equipo_ganador = 2

        # Incrementar contador de ediciones (solo si ya estaba finalizado)
        if partido.estado == "finalizado":
            partido.ediciones_resultado += 1

        partido.estado = "finalizado"
        partido.save()

        ediciones_restantes = max_ediciones_arbitro - partido.ediciones_resultado
        if not is_admin_user and ediciones_restantes > 0:
            messages.success(
                request,
                f"Resultado actualizado. Te quedan {ediciones_restantes} corrección(es) disponible(s).",
            )
        else:
            messages.success(request, "Resultado actualizado exitosamente.")

        return redirect("core:admin_partidos_list")

    return redirect("core:admin_partidos_list")


# ====================================================================================
# 🧑‍🎾 Reserva de Canchas (Jugador)
# ====================================================================================
@login_required
def player_reserve_court(request):
    """Permite al jugador reservar una cancha con validación visual"""
    cancha_id = request.GET.get("cancha_id")
    cancha = None
    if cancha_id:
        cancha = get_object_or_404(Cancha, id=cancha_id)

    form = ReservaCanchaForm(request.POST or None, initial={"cancha": cancha})

    if form.is_valid():
        reserva = form.save(commit=False)
        reserva.jugador = request.user
        # Si el form trae cancha usala, sino la del GET, sino error
        if not reserva.cancha and cancha:
            reserva.cancha = cancha

        reserva.save()
        messages.success(request, "Reserva realizada exitosamente.")
        return redirect("core:player_reservations")

    return render(
        request, "core/reservas/reservar_cancha.html", {"form": form, "cancha": cancha}
    )


@login_required
def player_reservation_list(request):
    """Lista el historial de reservas del jugador"""
    # Reservas futuras (pendientes o confirmadas)
    reservas_activas = (
        ReservaCancha.objects.filter(
            jugador=request.user, fecha__gte=datetime.date.today()
        )
        .exclude(estado="cancelada")
        .order_by("fecha", "hora_inicio")
    )

    # Historial (pasadas o canceladas)
    historial = (
        ReservaCancha.objects.filter(jugador=request.user)
        .exclude(id__in=reservas_activas.values_list("id", flat=True))
        .order_by("-fecha", "-hora_inicio")
    )

    return render(
        request,
        "core/reservas/mis_reservas.html",
        {"activas": reservas_activas, "historial": historial},
    )


@login_required
def player_cancel_reservation(request, reserva_id):
    """Permite cancelar una reserva propia"""
    reserva = get_object_or_404(ReservaCancha, id=reserva_id, jugador=request.user)

    if request.method == "POST":
        # Validar que no sea del pasado
        if reserva.fecha < datetime.date.today():
            messages.error(request, "No puedes cancelar reservas pasadas.")
        else:
            reserva.estado = "cancelada"
            reserva.save()
            messages.success(request, "Reserva cancelada exitosamente.")
        return redirect("core:player_reservations")

    return render(
        request, "core/reservas/confirmar_cancelacion.html", {"reserva": reserva}
    )


def ranking(request):
    """Vista pública del ranking de jugadores"""
    categoria_filtro = request.GET.get("categoria")

    # Base query: Jugadores activos ordenados por ranking
    jugadores = (
        Usuario.objects.filter(es_jugador=True)
        .prefetch_related("estadisticas")
        .order_by("-ranking")
    )

    if categoria_filtro:
        jugadores = jugadores.filter(categoria_jugador=categoria_filtro)

    # Inyectar estadística principal
    for jugador in jugadores:
        stats = next(
            (
                s
                for s in jugador.estadisticas.all()
                if str(s.categoria_id) == str(jugador.categoria_jugador)
            ),
            None,
        )
        if not stats and jugador.estadisticas.exists():
            stats = jugador.estadisticas.first()
        jugador.stats_display = stats

    # Obtener opciones de categoría desde el modelo
    categorias = Usuario._meta.get_field("categoria_jugador").choices

    context = {
        "jugadores": jugadores,
        "categorias": categorias,
        "filtro_actual": categoria_filtro,
    }
    return render(request, "core/ranking.html", context)


def player_public_profile(request, player_id):
    """Perfil público con estadísticas detalladas"""
    jugador = get_object_or_404(Usuario, id=player_id, es_jugador=True)

    # Estadísticas globales (suma de todas las categorías)
    stats_qs = jugador.estadisticas.all()
    total_victorias = sum(s.victorias for s in stats_qs)
    total_derrotas = sum(s.derrotas for s in stats_qs)
    total_jugados = sum(s.partidos_jugados for s in stats_qs)

    # Estadisticas calculadas
    efectividad = (
        round((total_victorias / total_jugados * 100), 1) if total_jugados > 0 else 0
    )
    ratio = (
        round(total_victorias / total_derrotas, 2)
        if total_derrotas > 0
        else total_victorias
    )

    # Historial de partidos (donde sea jugador)
    ultimos_partidos = (
        Partido.objects.filter(
            Q(equipo1=jugador) | Q(equipo2=jugador), estado="finalizado"
        )
        .distinct()
        .order_by("-fecha")[:10]
    )

    context = {
        "jugador": jugador,
        "total_jugados": total_jugados,
        "total_victorias": total_victorias,
        "total_derrotas": total_derrotas,
        "efectividad": efectividad,
        "ratio": ratio,
        "ultimos_partidos": ultimos_partidos,
    }
    return render(request, "core/jugador_perfil.html", context)


# Note: admin_player_list is defined above with pagination and search

# noticias


@login_required
@user_passes_test(is_admin)
def admin_noticias_list(request):
    noticias = Noticia.objects.order_by("-fecha_publicacion")
    form = NoticiaForm(prefix="news")
    return render(
        request,
        "core/noticias/lista_noticias.html",
        {"noticias": noticias, "form": form},
    )


@login_required
@user_passes_test(is_admin)
def admin_create_noticia(request):
    if request.method == "POST":
        # Intentar con prefijo primero, luego sin prefijo (del modal)
        titulo = request.POST.get("news-titulo") or request.POST.get("titulo")
        cuerpo = request.POST.get("news-cuerpo") or request.POST.get("cuerpo")
        imagen = request.FILES.get("news-imagen") or request.FILES.get("imagen")
        pos_x = (
            request.POST.get("news-imagen_pos_x")
            or request.POST.get("imagen_pos_x")
            or 50
        )
        pos_y = (
            request.POST.get("news-imagen_pos_y")
            or request.POST.get("imagen_pos_y")
            or 50
        )

        if titulo and cuerpo:
            noticia = Noticia(
                titulo=titulo,
                cuerpo=cuerpo,
                imagen=imagen,
                imagen_pos_x=int(pos_x),
                imagen_pos_y=int(pos_y),
                autor=request.user,
            )
            noticia.save()
            messages.success(request, "Noticia publicada exitosamente.")
            return redirect("core:admin_noticias_list")

    form = NoticiaForm(prefix="news")
    return render(request, "core/noticias/crear_noticia.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def admin_edit_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == "POST":
        noticia.titulo = request.POST.get("titulo", noticia.titulo)
        noticia.cuerpo = request.POST.get("cuerpo", noticia.cuerpo)

        # Manejar posición de imagen
        if request.POST.get("imagen_pos_x"):
            noticia.imagen_pos_x = int(request.POST.get("imagen_pos_x", 50))
        if request.POST.get("imagen_pos_y"):
            noticia.imagen_pos_y = int(request.POST.get("imagen_pos_y", 50))

        # Manejar imagen
        if request.FILES.get("imagen"):
            noticia.imagen = request.FILES.get("imagen")

        noticia.save()
        messages.success(request, "Noticia actualizada exitosamente.")
        return redirect("core:admin_noticias_list")

    form = NoticiaForm(instance=noticia)
    return render(
        request, "core/noticias/crear_noticia.html", {"form": form, "noticia": noticia}
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == "POST":
        noticia.delete()
        messages.success(request, "Noticia eliminada exitosamente.")
        return redirect("core:admin_noticias_list")
    return render(
        request, "core/noticias/confirmar_eliminar_noticia.html", {"noticia": noticia}
    )


def home(request):
    noticias = Noticia.objects.order_by("-fecha_publicacion", "-id")[
        :1
    ]  # la más reciente
    canchas = Cancha.objects.all()
    torneos = Torneo.objects.order_by("-fecha_inicio")[
        :5
    ]  # opcional si quieres mostrar torneos

    # Obtener Top 10 del ranking
    ranking = Usuario.objects.filter(es_jugador=True).order_by("-ranking")[:10]

    # Obtener últimos partidos
    partidos = (
        Partido.objects.all()
        .select_related("torneo", "cancha")
        .prefetch_related("equipo1", "equipo2")
        .order_by("-fecha", "-hora")[:10]
    )

    context = {
        "noticias": noticias,
        "canchas": canchas,
        "torneos": torneos,
        "ranking": ranking,
        "partidos": partidos,
    }
    return render(request, "home.html", context)
