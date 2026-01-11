from django.db import models
from users.models import Usuario

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Torneo(models.Model):
    arbitro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='torneos_asignados')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='torneos')
    premios = models.TextField(blank=True, null=True)
    jugadores_inscritos = models.ManyToManyField(Usuario, blank=True, related_name='torneos_inscritos')

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name_plural = "Torneos"

class Partido(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidos')
    # Cancha will be imported from facilities app, but to avoid circular imports we might use string reference if possible or just import.
    # Since facilities depends on nothing, we can import it. But wait, Partido depends on Cancha.
    cancha = models.ForeignKey('facilities.Cancha', on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    jugadores = models.ManyToManyField(Usuario, related_name='partidos_jugados')
    arbitro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='partidos_arbitrados')
    marcador = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ], default='pendiente')

    def __str__(self):
        return f"{self.torneo.nombre} - {self.fecha} {self.hora}"

    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name_plural = "Partidos"

class EstadisticaJugador(models.Model):
    jugador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='estadisticas')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    partidos_jugados = models.PositiveIntegerField(default=0)
    victorias = models.PositiveIntegerField(default=0)
    derrotas = models.PositiveIntegerField(default=0)

    @property
    def promedio_victorias(self):
        if self.partidos_jugados == 0:
            return 0
        return round((self.victorias / self.partidos_jugados) * 100, 2)
    
    @property
    def ratio_victorias(self):
        """Calcula el ratio victorias/derrotas"""
        if self.derrotas == 0:
            return self.victorias if self.victorias > 0 else 0
        return round(self.victorias / self.derrotas, 2)

    def __str__(self):
        return f"{self.jugador.cedula} - {self.promedio_victorias}%"

    class Meta:
        verbose_name = "Estadística de Jugador"
        verbose_name_plural = "Estadísticas de Jugadores"
