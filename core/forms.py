from django import forms
import re
from django.utils import timezone

# Importa Usuario porque Torneo, Partido y ReservaCancha referencian a Usuario
from users.models import Usuario
from competitions.models import Torneo, Partido
from facilities.models import Cancha, ReservaCancha
from blog.models import Noticia


class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = [
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "categoria",
            "premios",
            "arbitro",
            "jugadores_inscritos",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "pattern": ".{5,100}",
                    "minlength": "5",
                    "maxlength": "100",
                    "title": "El nombre del torneo debe tener entre 5 y 100 caracteres",
                    "placeholder": "Ej: Torneo Apertura 2024",
                }
            ),
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(
                attrs={
                    "minlength": "10",
                    "maxlength": "500",
                    "rows": 4,
                    "class": "form-control",
                    "title": "Describe el torneo: reglas básicas, lugar, objetivo... (min 10 caracteres)",
                    "placeholder": "Ej: Torneo anual para categorías juveniles...",
                    "oninvalid": "this.setCustomValidity('Describe el torneo: reglas básicas, lugar, objetivo... (min 10 caracteres)')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
            "premios": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "title": "Indica trofeos, premios en metálico o puntos a repartir",
                    "placeholder": "Ej: 1er Lugar: Trofeo + $100...",
                }
            ),
            "jugadores_inscritos": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }

    def clean_descripcion(self):
        desc = self.cleaned_data.get("descripcion")
        if desc and len(desc.strip()) < 10:
            raise forms.ValidationError(
                "La descripción es muy corta. Mínimo 10 caracteres."
            )
        return desc

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre").strip()

        # Longitud mínima
        if len(nombre) < 5:
            raise forms.ValidationError(
                "El nombre del torneo debe tener al menos 5 caracteres"
            )

        # Verificar duplicados (case insensitive)
        query = Torneo.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise forms.ValidationError("Ya existe un torneo con este nombre")

        return nombre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegúrate de que solo los usuarios que son árbitros puedan ser seleccionados
        self.fields["arbitro"].queryset = Usuario.objects.filter(es_arbitro=True)
        self.fields["arbitro"].empty_label = None
        
        # Asegurarse de que categoría no tenga guiones
        self.fields["categoria"].empty_label = None
        
        # Asegúrate de que solo los usuarios que son jugadores puedan ser seleccionados
        self.fields["jugadores_inscritos"].queryset = Usuario.objects.filter(
            es_jugador=True
        )

        # Validación HTML5: Bloquear fechas pasadas en el calendario
        today_str = timezone.now().date().isoformat()
        if "fecha_inicio" in self.fields:
            self.fields["fecha_inicio"].widget.attrs["min"] = today_str
        if "fecha_fin" in self.fields:
            self.fields["fecha_fin"].widget.attrs["min"] = today_str

    def clean_fecha_inicio(self):
        fecha = self.cleaned_data.get("fecha_inicio")
        if not fecha:
            return fecha

        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "La fecha de inicio no puede estar en el pasado"
            )
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get("fecha_inicio")
        fin = cleaned_data.get("fecha_fin")

        if inicio and fin and fin < inicio:
            raise forms.ValidationError(
                {
                    "fecha_fin": "La fecha de fin no puede ser anterior a la fecha de inicio"
                }
            )
        return cleaned_data


class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = [
            "nombre",
            "ubicacion",
            "estado",
            "precio_hora",
            "horario_apertura",
            "horario_cierre",
            "descripcion",
            "imagen",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "pattern": ".{3,50}",
                    "minlength": "3",
                    "maxlength": "50",
                    "class": "form-control",
                    "title": "El nombre de la cancha debe tener entre 3 y 50 caracteres",
                    "placeholder": "Ej: Cancha Principal",
                    "oninvalid": "this.setCustomValidity('El nombre de la cancha debe tener entre 3 y 50 caracteres')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "ubicacion": forms.TextInput(
                attrs={
                    "pattern": ".{10,200}",
                    "minlength": "10",
                    "maxlength": "200",
                    "class": "form-control",
                    "title": "La ubicación debe ser más descriptiva (mínimo 10 caracteres)",
                    "placeholder": "Ej: Av. Principal, al lado del Club...",
                    "oninvalid": "this.setCustomValidity('La ubicación debe ser más descriptiva (mínimo 10 caracteres)')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
            "precio_hora": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "title": "Ingrese un precio válido por hora (mayor a 0)",
                    "placeholder": "Ej: 20.00",
                    "oninvalid": "this.setCustomValidity('El precio debe ser un valor positivo')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
            "horario_apertura": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "style": "width: auto; max-width: 200px; display: inline-block;",
                    "title": "Hora de apertura de la cancha",
                    "oninvalid": "this.setCustomValidity('Seleccione una hora de apertura válida')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
            "horario_cierre": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "style": "width: auto; max-width: 200px; display: inline-block;",
                    "title": "Hora de cierre de la cancha",
                    "oninvalid": "this.setCustomValidity('Seleccione una hora de cierre válida')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "minlength": "10",
                    "title": "Descripción de la cancha (mínimo 10 caracteres)",
                    "placeholder": "Ej: Cancha techada con iluminación LED...",
                    "oninvalid": "this.setCustomValidity('La descripción es obligatoria y debe tener mínimo 10 caracteres')",
                    "oninput": "this.setCustomValidity('')",
                }
            ),
        }

    def clean_precio_hora(self):
        precio = self.cleaned_data.get("precio_hora")
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo")
        return precio

    def clean_descripcion(self):
        desc = self.cleaned_data.get("descripcion")
        if desc and len(desc.strip()) < 10:
            raise forms.ValidationError(
                "La descripción es muy corta (mínimo 10 caracteres)"
            )
        return desc

    def clean(self):
        cleaned_data = super().clean()
        apertura = cleaned_data.get("horario_apertura")
        cierre = cleaned_data.get("horario_cierre")

        if apertura and cierre and cierre <= apertura:
            raise forms.ValidationError(
                "La hora de cierre debe ser posterior a la de apertura"
            )
        return cleaned_data

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get("ubicacion")
        if ubicacion:
            ubicacion = ubicacion.strip()
            if len(ubicacion) < 10:
                raise forms.ValidationError(
                    "La ubicación debe ser más descriptiva (mínimo 10 caracteres)"
                )
        return ubicacion

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre").strip()

        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre de la cancha es muy corto (mínimo 3 caracteres)"
            )

        # Verificar duplicados
        query = Cancha.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise forms.ValidationError("Ya existe una cancha con este nombre")

        return nombre


class UsuarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name} (C.I-{obj.cedula})"


class UsuarioMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name} (C.I-{obj.cedula})"


class PartidoSchedulingForm(forms.ModelForm):
    es_casual = forms.BooleanField(
        required=False,
        label="¿Es partido casual/amistoso?",
        help_text="Marque esta casilla si el partido no pertenece a ningún torneo.",
    )

    arbitro = UsuarioChoiceField(
        queryset=Usuario.objects.filter(es_arbitro=True),
        required=False,
        label="Árbitro",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Team 1 Players
    equipo1_jugador1 = UsuarioChoiceField(
        queryset=Usuario.objects.filter(es_jugador=True),
        label="Equipo 1 - Jugador 1",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    equipo1_jugador2 = UsuarioChoiceField(
        queryset=Usuario.objects.filter(es_jugador=True),
        label="Equipo 1 - Jugador 2 (Opcional para dobles)",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Team 2 Players
    equipo2_jugador1 = UsuarioChoiceField(
        queryset=Usuario.objects.filter(es_jugador=True),
        label="Equipo 2 - Jugador 1",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    equipo2_jugador2 = UsuarioChoiceField(
        queryset=Usuario.objects.filter(es_jugador=True),
        label="Equipo 2 - Jugador 2 (Opcional para dobles)",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    HORARIOS_DISPONIBLES = [
        ("08:00", "08:00 AM - 10:00 AM"),
        ("10:00", "10:00 AM - 12:00 PM"),
        ("12:00", "12:00 PM - 02:00 PM"),
        ("14:00", "02:00 PM - 04:00 PM"),
        ("16:00", "04:00 PM - 06:00 PM"),
        ("18:00", "06:00 PM - 08:00 PM"),
        ("20:00", "08:00 PM - 10:00 PM"),
    ]

    hora = forms.ChoiceField(
        choices=HORARIOS_DISPONIBLES,
        label="Horario",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Partido
        fields = ["torneo", "es_casual", "cancha", "fecha", "hora", "arbitro"]
        widgets = {
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "title": "Selecciona una fecha válida (no pasada)",
                }
            ),
            "torneo": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restaurar etiqueta por defecto y hacer requerido inicialmente
        self.fields["torneo"].required = False
        self.fields["torneo"].empty_label = "--------- Seleccione un Torneo ---------"
        self.fields[
            "torneo"
        ].help_text = "Seleccione el torneo al que pertenece el partido."

        # Add empty option for optional players
        self.fields[
            "equipo1_jugador2"
        ].empty_label = "--------- Sin segundo jugador (individuales) ---------"
        self.fields[
            "equipo2_jugador2"
        ].empty_label = "--------- Sin segundo jugador (individuales) ---------"

        # Load existing team data when editing
        if self.instance and self.instance.pk:
            equipo1_jugadores = list(self.instance.equipo1.all())
            equipo2_jugadores = list(self.instance.equipo2.all())

            # Populate equipo1 fields
            if len(equipo1_jugadores) >= 1:
                self.fields["equipo1_jugador1"].initial = equipo1_jugadores[0]
            if len(equipo1_jugadores) >= 2:
                self.fields["equipo1_jugador2"].initial = equipo1_jugadores[1]

            # Populate equipo2 fields
            if len(equipo2_jugadores) >= 1:
                self.fields["equipo2_jugador1"].initial = equipo2_jugadores[0]
            if len(equipo2_jugadores) >= 2:
                self.fields["equipo2_jugador2"].initial = equipo2_jugadores[1]

        # Validación HTML5: Bloquear fechas pasadas
        today_str = timezone.now().date().isoformat()
        if "fecha" in self.fields:
            self.fields["fecha"].widget.attrs["min"] = today_str

    def clean(self):
        cleaned_data = super().clean()
        es_casual = cleaned_data.get("es_casual")
        torneo = cleaned_data.get("torneo")

        # Validate tournament
        if es_casual:
            cleaned_data["torneo"] = None
        else:
            if not torneo:
                self.add_error(
                    "torneo",
                    "Debe seleccionar un torneo o marcar la opción de 'Partido Casual'.",
                )

        # Get players
        eq1_j1 = cleaned_data.get("equipo1_jugador1")
        eq1_j2 = cleaned_data.get("equipo1_jugador2")
        eq2_j1 = cleaned_data.get("equipo2_jugador1")
        eq2_j2 = cleaned_data.get("equipo2_jugador2")

        # Collect all selected players (excluding None)
        all_players = [p for p in [eq1_j1, eq1_j2, eq2_j1, eq2_j2] if p]

        # Validate: At least 2 players total
        if len(all_players) < 2:
            raise forms.ValidationError(
                "Debe seleccionar al menos 2 jugadores (1 por equipo)"
            )

        # Validate: No duplicate players
        if len(all_players) != len(set(all_players)):
            raise forms.ValidationError(
                "No puede seleccionar el mismo jugador en múltiples posiciones"
            )

        # Validate: Both teams must have at least 1 player
        if not eq1_j1:
            self.add_error(
                "equipo1_jugador1", "El Equipo 1 debe tener al menos un jugador"
            )
        if not eq2_j1:
            self.add_error(
                "equipo2_jugador1", "El Equipo 2 debe tener al menos un jugador"
            )

        # Validate: Team balance (both teams should have same number of players)
        equipo1_count = sum([1 for p in [eq1_j1, eq1_j2] if p])
        equipo2_count = sum([1 for p in [eq2_j1, eq2_j2] if p])

        if equipo1_count != equipo2_count:
            raise forms.ValidationError(
                f"Ambos equipos deben tener la misma cantidad de jugadores. "
                f"Equipo 1: {equipo1_count}, Equipo 2: {equipo2_count}"
            )

        return cleaned_data

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if not fecha:
            return fecha
        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "La fecha del partido no puede estar en el pasado"
            )
        return fecha

    def save(self, commit=True):
        instance = super().save(commit=False)

        def save_m2m():
            # Clear and populate team fields
            instance.equipo1.clear()
            instance.equipo2.clear()

            # Add team 1 players
            if self.cleaned_data.get("equipo1_jugador1"):
                instance.equipo1.add(self.cleaned_data["equipo1_jugador1"])
            if self.cleaned_data.get("equipo1_jugador2"):
                instance.equipo1.add(self.cleaned_data["equipo1_jugador2"])

            # Add team 2 players
            if self.cleaned_data.get("equipo2_jugador1"):
                instance.equipo2.add(self.cleaned_data["equipo2_jugador1"])
            if self.cleaned_data.get("equipo2_jugador2"):
                instance.equipo2.add(self.cleaned_data["equipo2_jugador2"])

        if commit:
            instance.save()
            save_m2m()
        else:
            self.save_m2m = save_m2m

        return instance


class PartidoResultForm(forms.ModelForm):
    equipo_ganador = forms.ChoiceField(
        choices=[(1, "Equipo 1"), (2, "Equipo 2")],
        label="Equipo Ganador",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        help_text="Seleccione el equipo que ganó el partido",
    )

    class Meta:
        model = Partido
        fields = ["marcador", "equipo_ganador"]
        widgets = {
            "marcador": forms.TextInput(
                attrs={
                    "pattern": r"^(\d+-\d+)(,?\s*\d+-\d+)*$",
                    "title": "Formato: Sets separados por coma (Ej: 6-4, 6-3) o conteo simple de sets ganados (Ej: 2-1)",
                    "placeholder": "Ej: 6-4, 6-3 o 2-1",
                    "class": "form-control",
                    "required": "required",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No need to populate choices dynamically, they're static (1 or 2)

    def clean_marcador(self):
        marcador = self.cleaned_data.get("marcador")
        if not marcador:
            raise forms.ValidationError("El marcador es obligatorio")

        import re

        if not re.match(r"^(\d+-\d+)(,?\s*\d+-\d+)*$", marcador):
            raise forms.ValidationError(
                "Formato inválido. Use formato de sets: 6-4, 6-3 o conteo simple: 2-1"
            )
        return marcador

    def clean(self):
        cleaned_data = super().clean()
        equipo_ganador = cleaned_data.get("equipo_ganador")

        if self.instance and self.instance.pk:
            equipo1_jugadores = list(self.instance.equipo1.all())
            equipo2_jugadores = list(self.instance.equipo2.all())

            # Validate teams exist
            if not equipo1_jugadores and not equipo2_jugadores:
                raise forms.ValidationError(
                    "El partido no tiene equipos configurados. "
                    "Asegúrese de que el partido tenga jugadores asignados a cada equipo."
                )

            # Validate at least 2 players total
            total_players = len(equipo1_jugadores) + len(equipo2_jugadores)
            if total_players < 2:
                raise forms.ValidationError(
                    "El partido debe tener al menos 2 jugadores para registrar el resultado"
                )

        return cleaned_data


class ReservaCanchaForm(forms.ModelForm):
    class Meta:
        model = ReservaCancha
        fields = ["cancha", "fecha", "hora_inicio", "hora_fin"]
        widgets = {
            "cancha": forms.Select(
                attrs={"class": "form-select bg-light border-0 py-2", "id": "id_cancha"}
            ),
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control bg-light border-0 py-2",
                    "id": "id_fecha",
                }
            ),
            "hora_inicio": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control bg-light border-0 py-2",
                    "id": "id_hora_inicio",
                }
            ),
            "hora_fin": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control bg-light border-0 py-2",
                    "id": "id_hora_fin",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Validación HTML5: Bloquear fechas pasadas
        today_str = timezone.now().date().isoformat()
        if "fecha" in self.fields:
            self.fields["fecha"].widget.attrs["min"] = today_str

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if not fecha:
            return fecha

        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "La fecha de reserva no puede estar en el pasado"
            )
        return fecha

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data.get("hora_inicio")
        if not hora_inicio:
            return hora_inicio

        import datetime

        limit_start = datetime.time(8, 0)
        limit_end = datetime.time(22, 0)

        if hora_inicio < limit_start or hora_inicio > limit_end:
            raise forms.ValidationError(
                "Las reservas deben ser entre 8:00 AM y 10:00 PM"
            )
        return hora_inicio

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")
        cancha = cleaned_data.get("cancha")
        fecha = cleaned_data.get("fecha")

        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError(
                    "La hora de fin debe ser posterior a la de inicio"
                )

            # Duración
            import datetime

            dummy_date = datetime.date.today()
            dt_inicio = datetime.datetime.combine(dummy_date, hora_inicio)
            dt_fin = datetime.datetime.combine(dummy_date, hora_fin)
            duracion = (dt_fin - dt_inicio).total_seconds() / 3600

            if duracion < 1:
                raise forms.ValidationError("La reserva debe ser de al menos 1 hora")
            if duracion > 4:
                raise forms.ValidationError("La reserva no puede exceder las 4 horas")

            # Conflictos de Solapamiento
            if cancha and fecha:
                reservas = ReservaCancha.objects.filter(
                    cancha=cancha, fecha=fecha
                ).exclude(estado="cancelada")

                if self.instance and self.instance.pk:
                    reservas = reservas.exclude(pk=self.instance.pk)

                for r in reservas:
                    # Lógica de solapamiento: (StartA < EndB) and (EndA > StartB)
                    if hora_inicio < r.hora_fin and hora_fin > r.hora_inicio:
                        raise forms.ValidationError(
                            f"Conflicto: Ya existe una reserva de {r.hora_inicio} a {r.hora_fin}"
                        )

        return cleaned_data


# core/forms.py  crear formularios de registro para árbitros y jugadores


class ArbitroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "pattern": "(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^a-zA-Z0-9]).{8,}",
                "title": "Mínimo 8 caracteres, debe incluir: mayúscula, minúscula, número y algún carácter especial",
                "placeholder": "Ej: MiClave123!",
            }
        ),
        label="Contraseña",
    )

    class Meta:
        model = Usuario
        fields = ["cedula", "first_name", "last_name", "email", "password"]
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
        }
        widgets = {
            "cedula": forms.TextInput(
                attrs={
                    "pattern": "[1-9][0-9]{6,9}",
                    "title": "Completa este campo solo usando números, sin , / .* - ni ningún otro símbolo",
                    "placeholder": "Ej: 12345678",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "pattern": "[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,50}",
                    "title": "El nombre solo debe contener letras (mínimo 2 caracteres)",
                    "placeholder": "Ej: Juan",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "pattern": "[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,50}",
                    "title": "El apellido solo debe contener letras (mínimo 2 caracteres)",
                    "placeholder": "Ej: Pérez",
                }
            ),
            "email": forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")

        # Solo números
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números")

        # Longitud válida
        if len(cedula) < 7 or len(cedula) > 10:
            raise forms.ValidationError("La cédula debe tener entre 7 y 10 dígitos")

        # No puede comenzar con 0
        if cedula.startswith("0"):
            raise forms.ValidationError("La cédula no puede comenzar con 0")

        # Verificar que no exista (excluyendo la instancia actual si estamos editando)
        query = Usuario.objects.filter(cedula=cedula)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("Esta cédula ya está registrada")

        return cedula

    def clean_first_name(self):
        nombre = self.cleaned_data.get("first_name").strip()

        # Solo letras y espacios
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise forms.ValidationError("El nombre solo debe contener letras")

        # Longitud mínima
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres")

        # Capitalizar primera letra
        return nombre.title()

    def clean_last_name(self):
        apellido = self.cleaned_data.get("last_name").strip()

        # Solo letras y espacios
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            raise forms.ValidationError("El apellido solo debe contener letras")

        # Longitud mínima
        if len(apellido) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres")

        return apellido.title()

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Longitud mínima
        if len(password) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )

        # Al menos una mayúscula
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula"
            )

        # Al menos una minúscula
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra minúscula"
            )

        # Al menos un número
        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un número"
            )

        # Al menos un carácter especial
        if not re.search(r"[@#$%^&+=!]", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un carácter especial (@#$%^&+=!)"
            )

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.es_arbitro = True
        if commit:
            user.save()
        return user


class JugadorForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "pattern": "(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^a-zA-Z0-9]).{8,}",
                "title": "Mínimo 8 caracteres, debe incluir: mayúscula, minúscula, número y algún carácter especial",
                "placeholder": "Ej: MiClave123!",
            }
        ),
        label="Contraseña",
    )

    class Meta:
        model = Usuario
        fields = [
            "cedula",
            "first_name",
            "last_name",
            "email",
            "telefono",
            "categoria_jugador",
            "ranking",
            "password",
        ]
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
        }
        widgets = {
            "cedula": forms.TextInput(
                attrs={
                    "pattern": "[1-9][0-9]{6,9}",
                    "title": "Completa este campo solo usando números, sin , / .* - ni ningún otro símbolo",
                    "placeholder": "Ej: 12345678",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "pattern": "[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,50}",
                    "title": "El nombre solo debe contener letras (mínimo 2 caracteres)",
                    "placeholder": "Ej: Juan",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "pattern": "[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]{2,50}",
                    "title": "El apellido solo debe contener letras (mínimo 2 caracteres)",
                    "placeholder": "Ej: Pérez",
                }
            ),
            "email": forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"}),
            "telefono": forms.TextInput(
                attrs={
                    "pattern": "(0414|0424|0412|0416|0426|02[0-9]{2})[0-9]{7}",
                    "maxlength": "11",
                    "title": "Debe ser un número válido de Venezuela (Ej: 0414, 0424, 0412, 0416, 0426 o fijos 02xx) seguido de 7 dígitos",
                    "placeholder": "Ej: 04141234567",
                    "oninput": "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 11);",
                }
            ),
            "ranking": forms.NumberInput(
                attrs={
                    "min": "0",
                    "max": "2500",
                    "step": "1",
                    "title": "El ranking debe ser un número entero entre 0 y 2500",
                    "placeholder": "Ej: 100",
                }
            ),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")

        # Solo números
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números")

        # Longitud válida
        if len(cedula) < 7 or len(cedula) > 10:
            raise forms.ValidationError("La cédula debe tener entre 7 y 10 dígitos")

        # No puede comenzar con 0
        if cedula.startswith("0"):
            raise forms.ValidationError("La cédula no puede comenzar con 0")

        # Verificar que no exista (excluyendo la instancia actual si estamos editando)
        query = Usuario.objects.filter(cedula=cedula)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("Esta cédula ya está registrada")

        return cedula

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()

        # Verificar que no exista (excluyendo la instancia actual si estamos editando)
        query = Usuario.objects.filter(email=email)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("Este email ya está registrado")

        # Dominios no permitidos (emails temporales)
        dominios_bloqueados = [
            "tempmail.com",
            "guerrillamail.com",
            "10minutemail.com",
            "throwaway.email",
            "mailinator.com",
            "maildrop.cc",
            "temp-mail.org",
            "getnada.com",
            "trashmail.com",
        ]
        dominio = email.split("@")[1]
        if dominio in dominios_bloqueados:
            raise forms.ValidationError(
                "No se permiten emails temporales o desechables"
            )

        return email

    def clean_first_name(self):
        nombre = self.cleaned_data.get("first_name").strip()

        # Solo letras y espacios
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise forms.ValidationError("El nombre solo debe contener letras")

        # Longitud mínima
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres")

        # Capitalizar primera letra
        return nombre.title()

    def clean_last_name(self):
        apellido = self.cleaned_data.get("last_name").strip()

        # Solo letras y espacios
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            raise forms.ValidationError("El apellido solo debe contener letras")

        # Longitud mínima
        if len(apellido) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres")

        return apellido.title()

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Longitud mínima
        if len(password) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )

        # Al menos una mayúscula
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula"
            )

        # Al menos una minúscula
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra minúscula"
            )

        # Al menos un número
        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un número"
            )

        # Al menos un carácter especial
        if not re.search(r"[^a-zA-Z0-9]", password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un carácter especial"
            )

        return password

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")

        # Solo números
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números")

        # Longitud exacta 11 dígitos
        if len(telefono) != 11:
            raise forms.ValidationError("El teléfono debe tener exactamente 11 dígitos")

        # Validar códigos de área permitidos
        prefijos_validos = ["0414", "0424", "0412", "0416", "0426"]
        es_movil = any(telefono.startswith(prefijo) for prefijo in prefijos_validos)
        es_fijo = telefono.startswith("02") and len(telefono) == 11

        if not (es_movil or es_fijo):
            raise forms.ValidationError(
                "El código de área no es válido. Use 0414, 0424, 0412, 0416, 0426 o fijos (02xx)"
            )

        return telefono

    def clean_ranking(self):
        ranking = self.cleaned_data.get("ranking")
        if ranking is None:
            return 0
        if ranking < 0:
            raise forms.ValidationError("El ranking no puede ser negativo")
        if ranking > 2500:
            raise forms.ValidationError("El ranking no puede ser mayor a 2500")
        return ranking

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.es_jugador = True
        if commit:
            user.save()
        return user


class NoticiaForm(forms.ModelForm):
    imagen_pos_x = forms.IntegerField(widget=forms.HiddenInput(), initial=50, required=False)
    imagen_pos_y = forms.IntegerField(widget=forms.HiddenInput(), initial=50, required=False)

    class Meta:
        model = Noticia
        fields = ["titulo", "cuerpo", "imagen", "imagen_pos_x", "imagen_pos_y"]

