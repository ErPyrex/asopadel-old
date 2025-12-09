from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from facilities.models import ReservaCancha
from datetime import datetime

@login_required
def get_court_availability(request):
    """
    Returns a list of booked slots for a specific court and date.
    Params:
        court_id: int
        date: string 'YYYY-MM-DD'
    """
    court_id = request.GET.get('court_id')
    date_str = request.GET.get('date')
    
    if not court_id or not date_str:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        # Validate date format
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
        
    # Get confirmed or pending reservations
    reservations = ReservaCancha.objects.filter(
        cancha_id=court_id,
        fecha=query_date,
        estado__in=['pendiente', 'confirmada']
    ).order_by('hora_inicio')
    
    data = []
    for res in reservations:
        data.append({
            'start': res.hora_inicio.strftime('%H:%M'),
            'end': res.hora_fin.strftime('%H:%M'),
            'status': res.estado,
            'user': res.jugador.get_full_name if request.user.is_staff else "Reservado" # Privacy
        })
        
    return JsonResponse({'occupied_slots': data})
