from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Partido, EstadisticaJugador


@receiver(post_save, sender=Partido)
def actualizar_ranking_tras_partido(sender, instance, created, **kwargs):
    """
    Señal que se ejecuta cuando se guarda un Partido.
    Actualiza las estadísticas y el ranking de los jugadores cuando el partido finaliza.
    
    Formato esperado del marcador: "2-1" (sets ganados por jugador1 - sets ganados por jugador2)
    """
    # Solo procesar si el partido está finalizado
    if instance.estado != 'finalizado':
        return
    
    # Solo procesar si hay exactamente 2 jugadores
    jugadores = list(instance.jugadores.all())
    if len(jugadores) != 2:
        return
    
    # Solo procesar si hay un marcador válido
    if not instance.marcador or not instance.marcador.strip():
        return
    
    # Parsear el marcador (formato: "2-1" o "2 - 1")
    try:
        marcador_limpio = instance.marcador.strip().replace(' ', '')
        partes = marcador_limpio.split('-')
        
        if len(partes) != 2:
            return
        
        sets_jugador1 = int(partes[0])
        sets_jugador2 = int(partes[1])
        
    except (ValueError, IndexError):
        # Si el marcador no es válido, no hacer nada
        return
    
    # Determinar ganador y perdedor
    if sets_jugador1 > sets_jugador2:
        ganador = jugadores[0]
        perdedor = jugadores[1]
    elif sets_jugador2 > sets_jugador1:
        ganador = jugadores[1]
        perdedor = jugadores[0]
    else:
        # Empate - no actualizar ranking
        return
    
    # Actualizar estadísticas del ganador
    estadistica_ganador, _ = EstadisticaJugador.objects.get_or_create(
        jugador=ganador,
        categoria=instance.torneo.categoria,
        defaults={
            'partidos_jugados': 0,
            'victorias': 0,
            'derrotas': 0
        }
    )
    estadistica_ganador.partidos_jugados += 1
    estadistica_ganador.victorias += 1
    estadistica_ganador.save()
    
    # Actualizar estadísticas del perdedor
    estadistica_perdedor, _ = EstadisticaJugador.objects.get_or_create(
        jugador=perdedor,
        categoria=instance.torneo.categoria,
        defaults={
            'partidos_jugados': 0,
            'victorias': 0,
            'derrotas': 0
        }
    )
    estadistica_perdedor.partidos_jugados += 1
    estadistica_perdedor.derrotas += 1
    estadistica_perdedor.save()
    
    # Actualizar puntos de ranking usando ELO
    from utils.elo import calcular_probabilidad, nuevo_rating
    
    # Rating actual o inicial (1200 por defecto)
    rating_ganador = ganador.ranking if ganador.ranking and ganador.ranking > 0 else 1200
    rating_perdedor = perdedor.ranking if perdedor.ranking and perdedor.ranking > 0 else 1200
    
    # Calcular probabilidad de victoria del ganador vs perdedor
    probabilidad_ganador = calcular_probabilidad(rating_ganador, rating_perdedor)
    
    # Calcular nuevos ratings (S=1 para ganador, S=0 para perdedor)
    # K-factor 32 es estándar para amateurs/clubes
    nuevo_rating_ganador = nuevo_rating(rating_ganador, 1, probabilidad_ganador, k_factor=32)
    nuevo_rating_perdedor = nuevo_rating(rating_perdedor, 0, 1 - probabilidad_ganador, k_factor=32)
    
    # Guardar cambios
    ganador.ranking = max(0, nuevo_rating_ganador)
    ganador.save(update_fields=['ranking'])
    
    perdedor.ranking = max(0, nuevo_rating_perdedor)
    perdedor.save(update_fields=['ranking'])
