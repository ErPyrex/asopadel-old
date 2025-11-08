from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # 🏠 Públicas
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),  # ✅ vista completa con hero, noticias, torneos, ranking y canchas
    path('torneos/', views.public_tournament_list, name='public_torneos_list'),
    path('canchas/', views.public_court_list, name='public_canchas_list'),
    path('ranking/', views.public_ranking_list, name='public_ranking_list'),
    path('torneo/<int:torneo_id>/inscribirse/', views.inscribirse_torneo, name='inscribirse_torneo'),
    path('torneo/<int:torneo_id>/desinscribirse/', views.desinscribirse_torneo, name='desinscribirse_torneo'),
    path('reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    
    
    # 🔐 Dashboards por rol
    path('dashboard/', views.dashboard_by_role, name='dashboard_by_role'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('arbitro-dashboard/', views.arbitro_dashboard, name='arbitro_dashboard'),
    path('jugador-dashboard/', views.jugador_dashboard, name='jugador_dashboard'),
    path('arbitro/partido/<int:partido_id>/resultado/', views.registrar_resultado, name='registrar_resultado'),
    path('arbitro/partido/<int:partido_id>/detalles/', views.detalles_partido, name='detalles_partido'),
    path('arbitro/cancha/<int:cancha_id>/calendario/', views.calendario_cancha, name='calendario_cancha'),
    path('arbitro/canchas/estado/', views.estado_canchas, name='estado_canchas'),
    path('arbitro/partidos/', views.lista_partidos_arbitrados, name='lista_partidos_arbitrados'),
    path('arbitro/torneos/', views.torneos_asignados, name='torneos_asignados'),
    path('arbitro/cancha/<int:cancha_id>/calendario/', views.calendario_cancha, name='calendario_cancha'),
        
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
    path('admin/canchas/estado/', views.admin_estado_canchas, name='admin_estado_canchas'),
    
    # 🎾 Jugadores (Admin)
    path('admin-gestion/jugadores/', views.admin_player_list, name='admin_player_list'),
    path('admin-gestion/jugadores/crear/', views.admin_create_player, name='admin_create_player'),
    path('admin-gestion/jugadores/<int:jugador_id>/editar/', views.admin_edit_player, name='admin_edit_player'),
    path('admin-gestion/jugadores/<int:jugador_id>/eliminar/', views.admin_delete_player, name='admin_delete_player'),
    
    # 🧑‍⚖️ Gestión de Árbitros (Admin)
    path('admin-gestion/arbitros/', views.admin_referee_list, name='admin_referee_list'),
    path('admin-gestion/arbitros/crear/', views.admin_create_referee, name='admin_create_referee'),
    path('admin-gestion/arbitros/<int:arbitro_id>/editar/', views.admin_edit_referee, name='admin_edit_referee'),
    path('admin-gestion/arbitros/<int:arbitro_id>/eliminar/', views.admin_delete_referee, name='admin_delete_referee'),
        
    # 🗓️ Partidos (Admin)
    path('admin-gestion/partidos/crear/', views.admin_create_match, name='admin_create_match'),

    # 🧑‍🎾 Reservas (Jugador)
    path('player-reservar-cancha/', views.player_reserve_court, name='player_reserve_court'),
    path('player-reservar-cancha/<int:cancha_id>/', views.player_reserve_court, name='player_reserve_court_cancha'),
    path('eliminar-reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    
    
     # 📰 Hero y Noticias (Admin)
    path('admin-gestion/hero/editar/', views.admin_edit_hero, name='admin_edit_hero'),
    path('admin-gestion/noticias/', views.admin_noticias_list, name='admin_noticias_list'),
    path('admin-gestion/noticias/crear/', views.admin_create_noticia, name='admin_create_noticia'),
    path('admin-gestion/noticias/<int:noticia_id>/editar/', views.admin_edit_noticia, name='admin_edit_noticia'),
    path('admin-gestion/noticias/<int:noticia_id>/eliminar/', views.admin_delete_noticia, name='admin_delete_noticia'),
]

