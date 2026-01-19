from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from facilities.models import ReservaCancha
from datetime import datetime, timedelta


@login_required
def get_court_availability(request, cancha_id):
    """
    API para obtener eventos de disponibilidad para FullCalendar.
    Retorna reservas confirmadas, pendientes y PARTIDOS programados como eventos ocupados.
    También entrega las horas de operación de la cancha.
    """
    try:
        from facilities.models import Cancha
        from competitions.models import Partido
        
        cancha = Cancha.objects.get(id=cancha_id)
        start_date_str = request.GET.get("start")
        end_date_str = request.GET.get("end")

        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str.split("T")[0]).date()
        else:
            start_date = datetime.today().date()

        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str.split("T")[0]).date()
        else:
            end_date = start_date + timedelta(days=30)

        # 1. Reservas de jugadores
        reservas = ReservaCancha.objects.filter(
            cancha_id=cancha_id, fecha__range=[start_date, end_date]
        ).exclude(estado="cancelada")

        events = []
        for r in reservas:
            color = "#dc3545" if r.estado == "confirmada" else "#ffc107"
            title = "Reservado" if r.estado == "confirmada" else "Pendiente"
            if r.jugador == request.user:
                title = "Mi Reserva"
                color = "#198754"

            events.append({
                "title": title,
                "start": f"{r.fecha}T{r.hora_inicio}",
                "end": f"{r.fecha}T{r.hora_fin}",
                "color": color,
                "extendedProps": {"type": "reserva"}
            })

        # 2. Partidos programados
        partidos = Partido.objects.filter(
            cancha_id=cancha_id, fecha__range=[start_date, end_date]
        ).exclude(estado="cancelado")

        for p in partidos:
            # Asumimos 2 horas de duración
            dummy_date = datetime.today().date()
            dt_inicio = datetime.combine(dummy_date, p.hora)
            dt_fin = dt_inicio + timedelta(hours=2)
            
            events.append({
                "title": f"Partido: {p.torneo.nombre if p.torneo else 'Casual'}",
                "start": f"{p.fecha}T{p.hora}",
                "end": f"{p.fecha}T{dt_fin.time()}",
                "color": "#6f42c1", # Púrpura para partidos
                "extendedProps": {"type": "partido"}
            })

        return JsonResponse({
            "events": events,
            "businessHours": {
                "start": cancha.horario_apertura.strftime("%H:%M"),
                "end": cancha.horario_cierre.strftime("%H:%M"),
            }
        }, safe=False)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
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

