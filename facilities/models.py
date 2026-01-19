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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_actual()})"

    def get_estado_actual(self):
        """
        Determina el estado de la cancha en tiempo real.
        Si está en mantenimiento, se respeta.
        Si tiene una reserva o partido en este momento, se marca como reservada.
        """
        if self.estado == "mantenimiento":
            return "mantenimiento"

        from django.utils import timezone
        import datetime

        now = timezone.now()
        current_time = now.time()
        current_date = now.date()

        # Verificar si hay una reserva activa en este preciso momento
        reserva_activa = ReservaCancha.objects.filter(
            cancha=self,
            fecha=current_date,
            hora_inicio__lte=current_time,
            hora_fin__gte=current_time,
            estado="confirmada"
        ).exists()

        if reserva_activa:
            return "reservada"

        # Verificar si hay un partido activo (asumimos 2h de duración)
        # Importamos aquí para evitar importaciones circulares si fuera necesario
        from competitions.models import Partido
        
        # Un partido está activo si comenzó hace menos de 2 horas
        two_hours_ago = (now - datetime.timedelta(hours=2)).time()
        
        partido_activo = Partido.objects.filter(
            cancha=self,
            fecha=current_date,
            hora__lte=current_time,
            hora__gte=two_hours_ago
        ).exclude(estado="cancelado").exists()

        if partido_activo:
            return "reservada"

        return "disponible"

    def proxima_disponibilidad(self):
        """
        Devuelve cuándo volverá a estar libre la cancha si está ocupada.
        """
        if self.get_estado_actual() != "reservada":
            return None

        from django.utils import timezone
        import datetime
        now = timezone.now()
        current_time = now.time()
        
        # Buscar fin de la reserva actual
        reserva = ReservaCancha.objects.filter(
            cancha=self,
            fecha=now.date(),
            hora_inicio__lte=current_time,
            hora_fin__gte=current_time,
            estado="confirmada"
        ).order_by('hora_fin').first()

        if reserva:
            return reserva.hora_fin

        from competitions.models import Partido
        two_hours_ago = (now - datetime.timedelta(hours=2)).time()
        partido = Partido.objects.filter(
            cancha=self,
            fecha=now.date(),
            hora__lte=current_time,
            hora__gte=two_hours_ago
        ).exclude(estado="cancelado").order_by('-hora').first()

        if partido:
            # Fin estimado del partido
            dummy_date = datetime.date.today()
            dt_inicio = datetime.datetime.combine(dummy_date, partido.hora)
            dt_fin = dt_inicio + datetime.timedelta(hours=2)
            return dt_fin.time()

        return None

    class Meta:
        verbose_name_plural = "Canchas"
        ordering = ["-updated_at"]


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
