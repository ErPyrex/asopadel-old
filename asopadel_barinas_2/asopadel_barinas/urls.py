from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Rutas principales del sitio
    path('', include('core.urls')),         # Página de inicio, dashboard, home, etc.
    path('users/', include('users.urls')),  # Login, registro, paneles por rol
]

# Archivos estáticos y media en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])