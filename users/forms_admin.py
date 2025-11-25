"""
Admin-only forms for user management.
These forms should only be used by administrators in the admin panel.
"""

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Usuario


class AdminUsuarioChangeForm(UserChangeForm):
    """
    Form for editing users in the admin panel.
    Only administrators should have access to this form.
    Allows modification of roles and permissions.
    """
    
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = (
            'cedula', 'email', 'first_name', 'last_name',
            'telefono', 'categoria_jugador', 'ranking', 'foto', 'biografia',
            'es_admin_aso', 'es_arbitro', 'es_jugador',
            'is_active', 'is_staff', 'is_superuser'
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and add CSS classes to role checkboxes.
        """
        super().__init__(*args, **kwargs)
        for FieldName in ['es_admin_aso', 'es_arbitro', 'es_jugador']:
            if FieldName in self.fields:
                self.fields[FieldName].widget.attrs.update({'class': 'form-check-input'})
