from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Usuario


def is_superuser(user):
    """Check if user is a superuser (can manage admins)"""
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_superuser, login_url='core:home')
def admin_management(request):
    """
    Panel de gestión de administradores.
    Solo accesible para superusuarios.
    """
    # Get all admins (excluding superusers)
    admins = Usuario.objects.filter(
        es_admin_aso=True,
        is_superuser=False
    ).order_by('-date_joined')
    
    # Get all superusers
    superusers = Usuario.objects.filter(is_superuser=True).order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        # Search for users who are NOT already admins
        available_users = Usuario.objects.filter(
            Q(cedula__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        ).filter(
            es_admin_aso=False,
            is_superuser=False
        )[:10]  # Limit to 10 results
    else:
        available_users = []
    
    context = {
        'admins': admins,
        'superusers': superusers,
        'available_users': available_users,
        'search_query': search_query,
    }
    
    return render(request, 'users/admin_management.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:home')
def promote_to_admin(request, user_id):
    """
    Promote a user to admin.
    Only superusers can do this.
    """
    if request.method == 'POST':
        user = get_object_or_404(Usuario, id=user_id)
        
        # Prevent promoting if already admin or superuser
        if user.es_admin_aso or user.is_superuser:
            messages.warning(request, f'{user.get_full_name} ya es administrador.')
        else:
            user.es_admin_aso = True
            user.is_staff = True  # Allow access to Django admin
            user.save()
            messages.success(
                request, 
                f'{user.get_full_name} ha sido promovido a administrador.'
            )
    
    return redirect('users:admin_management')


@login_required
@user_passes_test(is_superuser, login_url='core:home')
def demote_from_admin(request, user_id):
    """
    Remove admin privileges from a user.
    Only superusers can do this.
    Cannot demote other superusers.
    """
    if request.method == 'POST':
        user = get_object_or_404(Usuario, id=user_id)
        
        # Prevent demoting superusers
        if user.is_superuser:
            messages.error(
                request, 
                'No puedes degradar a un superusuario. Usa la consola de Django para esto.'
            )
        elif not user.es_admin_aso:
            messages.warning(request, f'{user.get_full_name} no es administrador.')
        else:
            user.es_admin_aso = False
            user.is_staff = False
            user.save()
            messages.success(
                request, 
                f'{user.get_full_name} ya no es administrador.'
            )
    
    return redirect('users:admin_management')
