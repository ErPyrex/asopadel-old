from django.db import models
from users.models import Usuario  # Asegúrate de que este sea el modelo correcto

# -------------------------------
# 🏆 TORNEOS
# -------------------------------
class Torneo(models.Model):
    arbitro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='torneos_asignados')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    categoria = models.CharField(max_length=50, choices=[
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Hombre Menor', 'Hombre Menor'),
        ('Mujer Menor', 'Mujer Menor'),
    ])
    premios = models.TextField(blank=True, null=True)
    jugadores_inscritos = models.ManyToManyField(Usuario, blank=True, related_name='torneos_inscritos')

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name_plural = "Torneos"

# -------------------------------
# 🏟️ CANCHAS
# -------------------------------
class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=[
        ('padel', 'Padel'),
        ('tenis', 'Tenis'),
    ])
    estado = models.CharField(max_length=50, choices=[
        ('disponible', 'Disponible'),
        ('reservada', 'Reservada'),
        ('mantenimiento', 'Mantenimiento'),
    ])
    imagen = models.ImageField(upload_to='canchas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.estado})"

    class Meta:
        verbose_name_plural = "Canchas"

# -------------------------------
# 📊 ESTADÍSTICAS
# -------------------------------
class EstadisticaJugador(models.Model):
    jugador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='estadisticas')
    categoria = models.CharField(max_length=50)
    partidos_jugados = models.PositiveIntegerField(default=0)
    victorias = models.PositiveIntegerField(default=0)

    @property
    def promedio_victorias(self):
        if self.partidos_jugados == 0:
            return 0
        return round((self.victorias / self.partidos_jugados) * 100, 2)

    def __str__(self):
        return f"{self.jugador.cedula} - {self.promedio_victorias}%"  # ← corregido

    class Meta:
        verbose_name = "Estadística de Jugador"
        verbose_name_plural = "Estadísticas de Jugadores"

# -------------------------------
# 🛒 PRODUCTOS
# -------------------------------
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-disponible', 'nombre']
        verbose_name_plural = "Productos"

# -------------------------------
# ⚽ PARTIDOS
# -------------------------------
class Partido(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidos')
    cancha = models.ForeignKey(Cancha, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    jugadores = models.ManyToManyField(Usuario, related_name='partidos_jugados')
    arbitro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='partidos_arbitrados')
    marcador = models.CharField(max_length=100, blank=True)  # Ej: "6-4 / 3-6 / 7-5"
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

# -------------------------------
# 🗓️ RESERVA CANCHA
# -------------------------------
class ReservaCancha(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ], default='pendiente')

    def __str__(self):
        return f"{self.cancha.nombre} - {self.fecha} {self.hora_inicio}-{self.hora_fin}"

    class Meta:
        ordering = ['fecha', 'hora_inicio']
        verbose_name_plural = "Reservas de Canchas"
        
        
# hero y noticias 
class Hero(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='hero/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo