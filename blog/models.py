from django.db import models
from users.models import Usuario


class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    imagen = models.ImageField(upload_to="noticias/", blank=True, null=True)
    imagen_pos_x = models.IntegerField(default=50, help_text="Posición X del punto focal (0-100)")
    imagen_pos_y = models.IntegerField(default=50, help_text="Posición Y del punto focal (0-100)")
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo

    @property
    def imagen_position(self):
        """Devuelve el CSS object-position para la imagen."""
        return f"{self.imagen_pos_x}% {self.imagen_pos_y}%"

