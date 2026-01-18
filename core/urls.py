from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import views_api

app_name = 'core'

urlpatterns = [
    # 🏠 Públicas
    path('', views.home, name='home'),  # ✅ vista completa con noticias, torneos, ranking y canchas
    path('torneos/', views.public_tournament_list, name='public_torneos_list'),
    path('canchas/', views.public_court_list, name='public_canchas_list'),
    path('canchas/<int:cancha_id>/', views.public_court_detail, name='public_court_detail'),
    path('noticias/', views.public_noticias_list, name='public_noticias_list'),
    path('noticias/<int:noticia_id>/', views.public_noticia_detail, name='public_noticia_detail'),

    # 🔐 Dashboards por rol
    path('dashboard/', views.dashboard_by_role, name='dashboard_by_role'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('arbitro-dashboard/', views.arbitro_dashboard, name='arbitro_dashboard'),
    path('jugador-dashboard/', views.jugador_dashboard, name='jugador_dashboard'),

    # 🏆 Torneos (Admin)
    path('admin-gestion/torneos/', views.admin_tournament_list, name='admin_torneos_list'),
    path('admin-gestion/torneos/crear/', views.admin_create_tournament, name='admin_create_tournament'),
    path('admin-gestion/torneos/<int:torneo_id>/editar/', views.admin_edit_tournament, name='admin_edit_tournament'),
    path('admin-gestion/torneos/<int:torneo_id>/eliminar/', views.admin_delete_tournament, name='admin_delete_tournament'),
    
    # 🏟️ Canchas (Admin)
    path('admin-gestion/canchas/', views.admin_court_list, name='admin_canchas_list'),
    path('admin-gestion/canchas/crear/', views.admin_create_court, name='admin_create_court'),
    path('admin-gestion/canchas/<int:cancha_id>/editar/', views.admin_edit_court, name='admin_edit_court'),
    path('admin-gestion/canchas/<int:cancha_id>/eliminar/', views.admin_delete_court, name='admin_delete_court'),

    # 🎾 Jugadores (Admin)
    path('admin-gestion/jugadores/', views.admin_player_list, name='admin_player_list'),
    path('admin-gestion/jugadores/crear/', views.admin_create_player, name='admin_create_player'),
    path('admin-gestion/jugadores/<int:jugador_id>/editar/', views.admin_edit_player, name='admin_edit_player'),
    path('admin-gestion/jugadores/<int:jugador_id>/eliminar/', views.admin_delete_player, name='admin_delete_player'),
    
    # 🧑‍⚖️ Gestión de Árbitros (Admin)
    path('admin-gestion/arbitros/', views.admin_referee_list, name='admin_arbitros_list'),
    path('admin-gestion/arbitros/crear/', views.admin_create_referee, name='admin_create_arbitro'),
    path('admin-gestion/arbitros/<int:arbitro_id>/editar/', views.admin_edit_referee, name='admin_edit_arbitro'),
    path('admin-gestion/arbitros/<int:arbitro_id>/eliminar/', views.admin_delete_referee, name='admin_delete_arbitro'),

    # 🗓️ Partidos (Admin)
    # 🗓️ Partidos (Admin)
    path('admin-gestion/partidos/', views.admin_match_list, name='admin_partidos_list'),
    path('admin-gestion/partidos/crear/', views.admin_create_match, name='admin_create_match'),
    path('admin-gestion/partidos/pendientes/', views.admin_pending_results_list, name='admin_pending_results_list'), # Nueva ruta
    path('admin-gestion/partidos/<int:partido_id>/', views.admin_match_detail, name='admin_match_detail'),
    path('admin-gestion/partidos/<int:partido_id>/editar/', views.admin_edit_match, name='admin_edit_match'),
    path('admin-gestion/partidos/<int:partido_id>/resultado/', views.admin_record_result, name='admin_record_result'), # Nueva ruta
    path('admin-gestion/partidos/<int:partido_id>/eliminar/', views.admin_delete_match, name='admin_delete_match'),

    # 🧑‍🎾 Reservas (Jugador)
    path('player-reservar-cancha/', views.player_reserve_court, name='player_reserve_court'),
    path('mis-reservas/', views.player_reservation_list, name='player_reservations'),
    path('mis-reservas/<int:reserva_id>/cancelar/', views.player_cancel_reservation, name='player_cancel_reservation'),
    
    # 📰 Noticias
    path('admin-gestion/noticias/', views.admin_noticias_list, name='admin_noticias_list'),
    path('admin-gestion/noticias/crear/', views.admin_create_noticia, name='admin_create_noticia'),

    # 🔌 API (Internal)
    path('api/cancha/<int:cancha_id>/disponibilidad/', views_api.get_court_availability, name='api_court_availability'),

    # 🏆 Ranking
    path('ranking/', views.ranking, name='ranking'),
    path('jugador/<int:player_id>/', views.player_public_profile, name='player_public_profile'),
]