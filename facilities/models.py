from django.db import models
from users.models import Usuario

class TipoCancha(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Cancha"
        verbose_name_plural = "Tipos de Cancha"

class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoCancha, on_delete=models.SET_NULL, null=True)
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
