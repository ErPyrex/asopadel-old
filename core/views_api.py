from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from facilities.models import ReservaCancha
from datetime import datetime, timedelta


@login_required
def get_court_availability(request, cancha_id):
    """
    API para obtener eventos de disponibilidad para FullCalendar.
    Retorna reservas confirmadas y pendientes como eventos ocupados.
    """
    try:
        start_date_str = request.GET.get("start")
        end_date_str = request.GET.get("end")

        # FullCalendar envía ISO string (YYYY-MM-DD)
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str.split("T")[0]).date()
        else:
            start_date = datetime.today().date()

        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str.split("T")[0]).date()
        else:
            end_date = start_date + timedelta(days=30)

        reservas = ReservaCancha.objects.filter(
            cancha_id=cancha_id, fecha__range=[start_date, end_date]
        ).exclude(estado="cancelada")

        events = []
        for r in reservas:
            # Color coding: Pendiente (Naranja), Confirmada (Red)
            color = "#dc3545" if r.estado == "confirmada" else "#ffc107"
            title = "Reservado" if r.estado == "confirmada" else "Pendiente"

            # Si es el propio usuario, mostrar "Mi Reserva"
            if r.jugador == request.user:
                title = "Mi Reserva"
                color = "#198754"  # Verde

            events.append(
                {
                    "title": title,
                    "start": f"{r.fecha}T{r.hora_inicio}",
                    "end": f"{r.fecha}T{r.hora_fin}",
                    "color": color,
                    "card_id": r.id,
                }
            )

        return JsonResponse(events, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def get_players_by_category(request):
    """
    API para obtener jugadores filtrados por la categoría del torneo.
    Mapea la categoría del torneo (Juvenil/Adulto/Senior) a la categoría del jugador.
    """
    from users.models import Usuario
    from competitions.models import Categoria
    
    try:
        categoria_id = request.GET.get("categoria_id")
        search = request.GET.get("search", "").strip()
        
        # Obtener todos los jugadores activos
        jugadores = Usuario.objects.filter(es_jugador=True, is_active=True)
        
        # Si hay una categoría seleccionada, filtrar por ella
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=categoria_id)
                categoria_nombre = categoria.nombre.lower()
                jugadores = jugadores.filter(categoria_jugador__iexact=categoria_nombre)
            except Categoria.DoesNotExist:
                pass
        
        # Si hay búsqueda, filtrar por nombre o cédula
        if search:
            from django.db.models import Q
            jugadores = jugadores.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(cedula__icontains=search)
            )
        
        # Limitar resultados
        jugadores = jugadores[:50]
        
        data = [
            {
                "id": j.id,
                "nombre": f"{j.first_name} {j.last_name}",
                "cedula": j.cedula,
                "categoria": j.categoria_jugador or "Sin categoría",
            }
            for j in jugadores
        ]
        
        return JsonResponse({"jugadores": data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

