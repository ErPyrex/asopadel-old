"""
Comando de Django para recalcular estadísticas de todos los partidos finalizados.
Uso: python manage.py recalculate_stats
"""

from django.core.management.base import BaseCommand
from competitions.models import Partido, EstadisticaJugador
from users.models import Usuario


class Command(BaseCommand):
    help = "Recalcula las estadísticas de todos los jugadores basado en partidos finalizados"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando recálculo de estadísticas...")

        # Resetear todas las estadísticas
        EstadisticaJugador.objects.all().delete()
        self.stdout.write("Estadísticas anteriores eliminadas.")

        # Resetear rankings de todos los jugadores
        Usuario.objects.filter(es_jugador=True).update(ranking=0)
        self.stdout.write("Rankings reseteados a 0.")

        # Obtener todos los partidos finalizados ordenados por fecha
        partidos = Partido.objects.filter(
            estado="finalizado", equipo_ganador__isnull=False
        ).order_by("fecha", "hora")

        total = partidos.count()
        self.stdout.write(f"Procesando {total} partidos finalizados...")

        elo_base = 25

        for i, partido in enumerate(partidos, 1):
            # Obtener jugadores de cada equipo
            equipo1_jugadores = list(partido.equipo1.all())
            equipo2_jugadores = list(partido.equipo2.all())

            if partido.equipo_ganador == 1:
                ganadores = equipo1_jugadores
                perdedores = equipo2_jugadores
            else:
                ganadores = equipo2_jugadores
                perdedores = equipo1_jugadores

            # Actualizar estadísticas de ganadores
            for jugador in ganadores:
                stat, _ = EstadisticaJugador.objects.get_or_create(
                    jugador=jugador, categoria=None
                )
                stat.partidos_jugados += 1
                stat.victorias += 1
                stat.save()

                jugador.ranking = (jugador.ranking or 0) + elo_base
                jugador.save(update_fields=["ranking"])

            # Actualizar estadísticas de perdedores
            for jugador in perdedores:
                stat, _ = EstadisticaJugador.objects.get_or_create(
                    jugador=jugador, categoria=None
                )
                stat.partidos_jugados += 1
                stat.derrotas += 1
                stat.save()

                nuevo_ranking = (jugador.ranking or 0) - (elo_base // 2)
                jugador.ranking = max(0, nuevo_ranking)
                jugador.save(update_fields=["ranking"])

            if i % 10 == 0 or i == total:
                self.stdout.write(f"  Procesados {i}/{total} partidos...")

        self.stdout.write(
            self.style.SUCCESS(f"✓ Estadísticas recalculadas para {total} partidos.")
        )
