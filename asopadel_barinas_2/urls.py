from django.contrib import admin
from django.urls import path, include
from core import views as core_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('users/', include('users.urls')),
    path('canchas/', include('canchas.urls')),
    path('torneos/', include('torneos.urls')),
]
