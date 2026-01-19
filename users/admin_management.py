from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Usuario


def is_superuser(user):
    """Check if user is a superuser (can manage admins)"""
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_superuser, login_url="core:home")
def admin_management(request):
    """
    Panel de gestión de administradores.
    Solo accesible para superusuarios.
    """
    # Get all admins (excluding superusers)
    admins = Usuario.objects.filter(es_admin_aso=True, is_superuser=False).order_by(
        "-date_joined"
    )

    # Get all superusers
    superusers = Usuario.objects.filter(is_superuser=True).order_by("-date_joined")

    # Search functionality - busca TODOS los usuarios para cambiar roles
    search_query = request.GET.get("search", "")
    if search_query:
        # Buscar usuarios (excepto superusers para protegerlos)
        available_users = Usuario.objects.filter(
            Q(cedula__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        ).exclude(is_superuser=True)[:15]  # Limit to 15 results
    else:
        available_users = []

    context = {
        "admins": admins,
        "superusers": superusers,
        "available_users": available_users,
        "search_query": search_query,
    }

    return render(request, "users/admin_management.html", context)


@login_required
@user_passes_test(is_superuser, login_url="core:home")
def promote_to_admin(request, user_id):
    """
    Promote a user to admin.
    Only superusers can do this.
    When promoted, the user loses player/referee roles but they are saved for restoration.
    """
    if request.method == "POST":
        user = get_object_or_404(Usuario, id=user_id)

        # Prevent promoting if already admin or superuser
        if user.es_admin_aso or user.is_superuser:
            messages.warning(request, f"{user.get_full_name()} ya es administrador.")
        else:
            # Guardar rol previo antes de promover
            if user.es_jugador and user.es_arbitro:
                user.rol_previo_admin = "ambos"
            elif user.es_jugador:
                user.rol_previo_admin = "jugador"
            elif user.es_arbitro:
                user.rol_previo_admin = "arbitro"
            else:
                user.rol_previo_admin = "ninguno"

            # Guardar roles anteriores para el mensaje
            roles_anteriores = []
            if user.es_jugador:
                roles_anteriores.append("jugador")
            if user.es_arbitro:
                roles_anteriores.append("árbitro")

            # Promover a admin y quitar otros roles
            user.es_admin_aso = True
            user.is_staff = True  # Allow access to Django admin
            user.es_jugador = False  # No puede ser jugador
            user.es_arbitro = False  # No puede ser árbitro
            user.save()

            if roles_anteriores:
                mensaje_roles = " y ".join(roles_anteriores)
                messages.success(
                    request,
                    f"{user.get_full_name()} ha sido promovido a administrador. "
                    f"Ya no es {mensaje_roles}. (Se restaurará al revocar)",
                )
            else:
                messages.success(
                    request,
                    f"{user.get_full_name()} ha sido promovido a administrador.",
                )

    return redirect("users:admin_management")


@login_required
@user_passes_test(is_superuser, login_url="core:home")
def demote_from_admin(request, user_id):
    """
    Remove admin privileges from a user and restore their previous role.
    Only superusers can do this.
    Cannot demote other superusers.
    """
    if request.method == "POST":
        user = get_object_or_404(Usuario, id=user_id)

        # Prevent demoting superusers
        if user.is_superuser:
            messages.error(
                request,
                "No puedes degradar a un superusuario. Usa la consola de Django para esto.",
            )
        elif not user.es_admin_aso:
            messages.warning(request, f"{user.get_full_name()} no es administrador.")
        else:
            # Restaurar rol previo
            rol_restaurado = []
            if user.rol_previo_admin == "jugador":
                user.es_jugador = True
                rol_restaurado.append("jugador")
            elif user.rol_previo_admin == "arbitro":
                user.es_arbitro = True
                rol_restaurado.append("árbitro")
            elif user.rol_previo_admin == "ambos":
                user.es_jugador = True
                user.es_arbitro = True
                rol_restaurado.extend(["jugador", "árbitro"])
            # Si era "ninguno" o None, no se restaura ningún rol

            user.es_admin_aso = False
            user.is_staff = False
            user.rol_previo_admin = None  # Limpiar el campo
            user.save()

            if rol_restaurado:
                roles_msg = " y ".join(rol_restaurado)
                messages.success(
                    request,
                    f"{user.get_full_name()} ya no es administrador. "
                    f"Ha sido restaurado como {roles_msg}.",
                )
            else:
                messages.success(
                    request, f"{user.get_full_name()} ya no es administrador."
                )

    return redirect("users:admin_management")


@login_required
@user_passes_test(is_superuser, login_url="core:home")
def change_user_role(request, user_id):
    """
    Cambiar los roles de cualquier usuario.
    Solo superusuarios pueden hacer esto.
    Permite asignar/quitar roles de admin, árbitro y jugador.
    """
    if request.method == "POST":
        user = get_object_or_404(Usuario, id=user_id)

        # No permitir modificar a otros superusuarios
        if user.is_superuser and user != request.user:
            messages.error(
                request, "No puedes modificar los roles de otro superusuario."
            )
            return redirect("users:admin_management")

        # Obtener nuevos roles del formulario
        nuevo_admin = request.POST.get("es_admin_aso") == "on"
        nuevo_arbitro = request.POST.get("es_arbitro") == "on"
        nuevo_jugador = request.POST.get("es_jugador") == "on"

        # Un admin no puede ser jugador ni árbitro
        if nuevo_admin and (nuevo_jugador or nuevo_arbitro):
            messages.error(
                request,
                "Un administrador no puede ser jugador ni árbitro al mismo tiempo.",
            )
            return redirect("users:admin_management")

        # Guardar cambios
        cambios = []

        # Cambio a admin
        if nuevo_admin and not user.es_admin_aso:
            # Guardar rol previo antes de promover
            if user.es_jugador and user.es_arbitro:
                user.rol_previo_admin = "ambos"
            elif user.es_jugador:
                user.rol_previo_admin = "jugador"
            elif user.es_arbitro:
                user.rol_previo_admin = "arbitro"
            else:
                user.rol_previo_admin = "ninguno"
            user.es_admin_aso = True
            user.is_staff = True
            user.es_jugador = False
            user.es_arbitro = False
            cambios.append("promovido a admin")
        elif not nuevo_admin and user.es_admin_aso:
            user.es_admin_aso = False
            user.is_staff = False
            cambios.append("removido de admin")

        # Solo aplicar cambios de jugador/árbitro si no es admin
        if not nuevo_admin:
            if nuevo_jugador != user.es_jugador:
                user.es_jugador = nuevo_jugador
                cambios.append("jugador: " + ("sí" if nuevo_jugador else "no"))
            if nuevo_arbitro != user.es_arbitro:
                user.es_arbitro = nuevo_arbitro
                cambios.append("árbitro: " + ("sí" if nuevo_arbitro else "no"))

        if cambios:
            user.save()
            cambios_msg = ", ".join(cambios)
            messages.success(
                request,
                f"Roles actualizados para {user.get_full_name()}: {cambios_msg}",
            )
        else:
            messages.info(
                request, f"No hubo cambios en los roles de {user.get_full_name()}."
            )

    return redirect("users:admin_management")
