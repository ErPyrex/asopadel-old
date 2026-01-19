from django.db import models
from users.models import Usuario


class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    imagen = models.ImageField(upload_to="noticias/", blank=True, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo
