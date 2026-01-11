from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from facilities.models import ReservaCancha, Cancha
from datetime import datetime, timedelta

@login_required
def get_court_availability(request, cancha_id):
    """
    API para obtener eventos de disponibilidad para FullCalendar.
    Retorna reservas confirmadas y pendientes como eventos ocupados.
    """
    try:
        start_date_str = request.GET.get('start')
        end_date_str = request.GET.get('end')
        
        # FullCalendar envía ISO string (YYYY-MM-DD)
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str.split('T')[0]).date()
        else:
            start_date = datetime.today().date()
            
        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str.split('T')[0]).date()
        else:
            end_date = start_date + timedelta(days=30)

        reservas = ReservaCancha.objects.filter(
            cancha_id=cancha_id,
            fecha__range=[start_date, end_date]
        ).exclude(estado='cancelada')

        events = []
        for r in reservas:
            # Color coding: Pendiente (Naranja), Confirmada (Red)
            color = '#dc3545' if r.estado == 'confirmada' else '#ffc107'
            title = 'Reservado' if r.estado == 'confirmada' else 'Pendiente'
            
            # Si es el propio usuario, mostrar "Mi Reserva"
            if r.jugador == request.user:
                title = "Mi Reserva"
                color = '#198754' # Verde

            events.append({
                'title': title,
                'start': f"{r.fecha}T{r.hora_inicio}",
                'end': f"{r.fecha}T{r.hora_fin}",
                'color': color,
                'card_id': r.id,
            })

        return JsonResponse(events, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
