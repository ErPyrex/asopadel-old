from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Partido, EstadisticaJugador


@receiver(post_save, sender=Partido)
def actualizar_ranking_tras_partido(sender, instance, created, **kwargs):
    """
    Señal que se ejecuta cuando se guarda un Partido.
    Actualiza las estadísticas y el ranking de los jugadores cuando el partido finaliza.
    
    Prioriza el campo 'equipo_ganador' (1 o 2) para partidos por equipos.
    Fallback: usa campo 'ganador' individual o parsea el marcador para compatibilidad.
    """
    # Solo procesar si el partido está finalizado
    if instance.estado != 'finalizado':
        return
    
    # Obtener jugadores de cada equipo
    equipo1_jugadores = list(instance.equipo1.all())
    equipo2_jugadores = list(instance.equipo2.all())
    
    # Determinar ganadoresganadores = []
    perdedores = []
    
    # OPCIÓN 1: Usar equipo_ganador (sistema de equipos nuevo)
    if instance.equipo_ganador:
        if instance.equipo_ganador == 1:
            ganadores = equipo1_jugadores
            perdedores = equipo2_jugadores
        elif instance.equipo_ganador == 2:
            ganadores = equipo2_jugadores
            perdedores = equipo1_jugadores
    
    # OPCIÓN 2: Fallback para compatibilidad con partidos antiguos
    if not ganadores:
        # Intentar con campo ganador individual (legacy)
        if instance.ganador:
            jugadores_legacy = list(instance.jugadores.all())
            if len(jugadores_legacy) == 2 and instance.ganador in jugadores_legacy:
                ganadores = [instance.ganador]
                perdedores = [j for j in jugadores_legacy if j != instance.ganador]
        
        # Último recurso: parsear marcador
        elif instance.marcador and instance.marcador.strip():
            jugadores_legacy = list(instance.jugadores.all())
            if len(jugadores_legacy) == 2:
                try:
                    marcador_limpio = instance.marcador.strip().replace(' ', '')
                    partes = marcador_limpio.split('-')
                    
                    if len(partes) == 2:
                        sets_jugador1 = int(partes[0])
                        sets_jugador2 = int(partes[1])
                        
                        if sets_jugador1 > sets_jugador2:
                            ganadores = [jugadores_legacy[0]]
                            perdedores = [jugadores_legacy[1]]
                        elif sets_jugador2 > sets_jugador1:
                            ganadores = [jugadores_legacy[1]]
                            perdedores = [jugadores_legacy[0]]
                except (ValueError, IndexError):
                    pass
    
    # Si no pudimos determinar ganadores, salir
    if not ganadores or not perdedores:
        return
    
    # Actualizar estadísticas para CADA jugador ganador
    for ganador in ganadores:
        estadistica_ganador, _ = EstadisticaJugador.objects.get_or_create(
            jugador=ganador,
            categoria=instance.torneo.categoria if instance.torneo else None,
            defaults={
                'partidos_jugados': 0,
                'victorias': 0,
                'derrotas': 0
            }
        )
        estadistica_ganador.partidos_jugados += 1
        estadistica_ganador.victorias += 1
        estadistica_ganador.save()
    
    # Actualizar estadísticas para CADA jugador perdedor
    for perdedor in perdedores:
        estadistica_perdedor, _ = EstadisticaJugador.objects.get_or_create(
            jugador=perdedor,
            categoria=instance.torneo.categoria if instance.torneo else None,
            defaults={
                'partidos_jugados': 0,
                'victorias': 0,
                'derrotas': 0
            }
        )
        estadistica_perdedor.partidos_jugados += 1
        estadistica_perdedor.derrotas += 1
        estadistica_perdedor.save()
    
    # Actualizar puntos de ranking usando ELO (promedio de equipo)
    from utils.elo import calcular_probabilidad, nuevo_rating
    
    # Calcular rating promedio de cada equipo
    rating_ganadores = sum([g.ranking if g.ranking and g.ranking > 0 else 1200 for g in ganadores]) / len(ganadores)
    rating_perdedores = sum([p.ranking if p.ranking and p.ranking > 0 else 1200 for p in perdedores]) / len(perdedores)
    
    # Calcular probabilidad de victoria del equipo ganador
    probabilidad_ganadores = calcular_probabilidad(rating_ganadores, rating_perdedores)
    
    # Calcular nuevos ratings (S=1 para ganadores, S=0 para perdedores)
    # K-factor 32 es estándar para amateurs/clubes
    nuevo_rating_ganadores = nuevo_rating(rating_ganadores, 1, probabilidad_ganadores, k_factor=32)
    nuevo_rating_perdedores = nuevo_rating(rating_perdedores, 0, 1 - probabilidad_ganadores, k_factor=32)
    
    # Calcular delta de rating
    delta_ganadores = nuevo_rating_ganadores - rating_ganadores
    delta_perdedores = nuevo_rating_perdedores - rating_perdedores
    
    # Aplicar delta a cada jugador del equipo ganador
    for ganador in ganadores:
        rating_actual = ganador.ranking if ganador.ranking and ganador.ranking > 0 else 1200
        ganador.ranking = max(0, rating_actual + delta_ganadores)
        ganador.save(update_fields=['ranking'])
    
    # Aplicar delta a cada jugador del equipo perdedor
    for perdedor in perdedores:
        rating_actual = perdedor.ranking if perdedor.ranking and perdedor.ranking > 0 else 1200
        perdedor.ranking = max(0, rating_actual + delta_perdedores)
        perdedor.save(update_fields=['ranking'])
