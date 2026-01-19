from django.db import models
from users.models import Usuario


class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=50,
        choices=[
            ("disponible", "Disponible"),
            ("reservada", "Reservada"),
            ("mantenimiento", "Mantenimiento"),
        ],
    )
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    horario_apertura = models.TimeField(default="08:00")
    horario_cierre = models.TimeField(default="22:00")
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="canchas/", blank=True, null=True)

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
    estado = models.CharField(
        max_length=50,
        choices=[
            ("pendiente", "Pendiente"),
            ("confirmada", "Confirmada"),
            ("cancelada", "Cancelada"),
        ],
        default="pendiente",
    )

    def __str__(self):
        return f"{self.cancha.nombre} - {self.fecha} {self.hora_inicio}-{self.hora_fin}"

    class Meta:
        ordering = ["fecha", "hora_inicio"]
        verbose_name_plural = "Reservas de Canchas"
