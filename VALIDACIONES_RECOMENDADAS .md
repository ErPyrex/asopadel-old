# 📋 VALIDACIONES RECOMENDADAS PARA EL PROYECTO ASOPADEL

## 📌 RESUMEN
Este documento detalla todas las validaciones que se pueden implementar en los formularios del proyecto para mejorar la calidad de los datos y la experiencia del usuario.

---

## 🔐 1. FORMULARIOS DE USUARIO (users/forms.py y core/forms.py)

### 1.1 **ArbitroForm** y **JugadorForm**

#### ✅ Campo: `cedula`
**Validaciones actuales:** Ninguna específica
**Validaciones recomendadas:**
- ✨ Solo números (sin letras, puntos ni guiones)
- ✨ Longitud entre 7-10 dígitos (cédulas venezolanas)
- ✨ No permitir cédulas duplicadas
- ✨ No permitir que comience con 0

**Ejemplo de validación:**
```python
def clean_cedula(self):
    cedula = self.cleaned_data.get('cedula')
    
    # Solo números
    if not cedula.isdigit():
        raise forms.ValidationError("La cédula solo debe contener números")
    
    # Longitud válida
    if len(cedula) < 7 or len(cedula) > 10:
        raise forms.ValidationError("La cédula debe tener entre 7 y 10 dígitos")
    
    # No puede comenzar con 0
    if cedula.startswith('0'):
        raise forms.ValidationError("La cédula no puede comenzar con 0")
    
    # Verificar que no exista
    if Usuario.objects.filter(cedula=cedula).exists():
        raise forms.ValidationError("Esta cédula ya está registrada")
    
    return cedula
```

---

#### ✅ Campo: `email`
**Validaciones actuales:** EmailField de Django (formato básico)
**Validaciones recomendadas:**
- ✨ Formato válido de email (ya incluido por Django)
- ✨ No permitir emails duplicados
- ✨ Dominios permitidos (opcional: solo .com, .net, .org, .ve, etc.)
- ✨ No permitir emails temporales/desechables

**Ejemplo de validación:**
```python
def clean_email(self):
    email = self.cleaned_data.get('email').lower()
    
    # Verificar que no exista
    if Usuario.objects.filter(email=email).exists():
        raise forms.ValidationError("Este email ya está registrado")
    
    # Dominios no permitidos (emails temporales)
    dominios_bloqueados = ['tempmail.com', 'guerrillamail.com', '10minutemail.com']
    dominio = email.split('@')[1]
    if dominio in dominios_bloqueados:
        raise forms.ValidationError("No se permiten emails temporales")
    
    return email
```

---

#### ✅ Campo: `first_name` y `last_name`
**Validaciones actuales:** CharField básico
**Validaciones recomendadas:**
- ✨ Solo letras y espacios (sin números ni caracteres especiales)
- ✨ Longitud mínima de 2 caracteres
- ✨ Longitud máxima de 50 caracteres
- ✨ Primera letra en mayúscula (auto-formateo)

**Ejemplo de validación:**
```python
import re

def clean_first_name(self):
    nombre = self.cleaned_data.get('first_name').strip()
    
    # Solo letras y espacios
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
        raise forms.ValidationError("El nombre solo debe contener letras")
    
    # Longitud mínima
    if len(nombre) < 2:
        raise forms.ValidationError("El nombre debe tener al menos 2 caracteres")
    
    # Capitalizar primera letra
    return nombre.title()

def clean_last_name(self):
    apellido = self.cleaned_data.get('last_name').strip()
    
    # Solo letras y espacios
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido):
        raise forms.ValidationError("El apellido solo debe contener letras")
    
    # Longitud mínima
    if len(apellido) < 2:
        raise forms.ValidationError("El apellido debe tener al menos 2 caracteres")
    
    return apellido.title()
```

---

#### ✅ Campo: `password`
**Validaciones actuales:** PasswordInput widget
**Validaciones recomendadas:**
- ✨ Mínimo 8 caracteres
- ✨ Al menos una letra mayúscula
- ✨ Al menos una letra minúscula
- ✨ Al menos un número
- ✨ Al menos un carácter especial (@, #, $, etc.)

**Ejemplo de validación:**
```python
def clean_password(self):
    password = self.cleaned_data.get('password')
    
    # Longitud mínima
    if len(password) < 8:
        raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
    
    # Al menos una mayúscula
    if not re.search(r'[A-Z]', password):
        raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula")
    
    # Al menos una minúscula
    if not re.search(r'[a-z]', password):
        raise forms.ValidationError("La contraseña debe contener al menos una letra minúscula")
    
    # Al menos un número
    if not re.search(r'\d', password):
        raise forms.ValidationError("La contraseña debe contener al menos un número")
    
    # Al menos un carácter especial
    if not re.search(r'[@#$%^&+=!]', password):
        raise forms.ValidationError("La contraseña debe contener al menos un carácter especial (@#$%^&+=!)")
    
    return password
```

---

#### ✅ Campo: `telefono` (JugadorForm)
**Validaciones actuales:** CharField opcional
**Validaciones recomendadas:**
- ✨ Solo números y guiones
- ✨ Formato venezolano: 0XXX-XXXXXXX (11 dígitos con guión)
- ✨ Códigos de área válidos (0412, 0414, 0424, 0416, 0426, 0273, etc.)

**Ejemplo de validación:**
```python
def clean_telefono(self):
    telefono = self.cleaned_data.get('telefono')
    
    if telefono:
        # Remover espacios y guiones para validar
        telefono_limpio = telefono.replace('-', '').replace(' ', '')
        
        # Solo números
        if not telefono_limpio.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números")
        
        # Longitud válida (11 dígitos en Venezuela)
        if len(telefono_limpio) != 11:
            raise forms.ValidationError("El teléfono debe tener 11 dígitos (Ej: 0414-1234567)")
        
        # Debe comenzar con 0
        if not telefono_limpio.startswith('0'):
            raise forms.ValidationError("El teléfono debe comenzar con 0")
        
        # Códigos de área válidos
        codigos_validos = ['0412', '0414', '0424', '0416', '0426', '0273', '0274', '0275', '0212']
        codigo = telefono_limpio[:4]
        if codigo not in codigos_validos:
            raise forms.ValidationError(f"Código de área no válido. Debe ser uno de: {', '.join(codigos_validos)}")
        
        # Formatear automáticamente
        return f"{telefono_limpio[:4]}-{telefono_limpio[4:]}"
    
    return telefono
```

---

#### ✅ Campo: `ranking` (JugadorForm)
**Validaciones actuales:** IntegerField con default=0
**Validaciones recomendadas:**
- ✨ Solo números enteros positivos
- ✨ Rango válido: 0-1000 (o el rango que definas)

**Ejemplo de validación:**
```python
def clean_ranking(self):
    ranking = self.cleaned_data.get('ranking')
    
    if ranking is not None:
        # Debe ser positivo
        if ranking < 0:
            raise forms.ValidationError("El ranking no puede ser negativo")
        
        # Rango máximo
        if ranking > 1000:
            raise forms.ValidationError("El ranking no puede ser mayor a 1000")
    
    return ranking
```

---

## 🏆 2. FORMULARIOS DE TORNEOS (core/forms.py)

### 2.1 **TorneoForm**

#### ✅ Campo: `nombre`
**Validaciones actuales:** CharField básico
**Validaciones recomendadas:**
- ✨ Longitud mínima de 5 caracteres
- ✨ Longitud máxima de 100 caracteres
- ✨ No permitir nombres duplicados

**Ejemplo de validación:**
```python
def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre').strip()
    
    # Longitud mínima
    if len(nombre) < 5:
        raise forms.ValidationError("El nombre del torneo debe tener al menos 5 caracteres")
    
    # Verificar duplicados
    if Torneo.objects.filter(nombre__iexact=nombre).exists():
        raise forms.ValidationError("Ya existe un torneo con este nombre")
    
    return nombre
```

---

#### ✅ Campos: `fecha_inicio` y `fecha_fin`
**Validaciones actuales:** DateInput widget
**Validaciones recomendadas:**
- ✨ La fecha de inicio no puede ser en el pasado
- ✨ La fecha de fin debe ser posterior a la fecha de inicio
- ✨ El torneo no puede durar más de 1 año

**Ejemplo de validación:**
```python
from datetime import date, timedelta

def clean_fecha_inicio(self):
    fecha_inicio = self.cleaned_data.get('fecha_inicio')
    
    # No puede ser en el pasado
    if fecha_inicio < date.today():
        raise forms.ValidationError("La fecha de inicio no puede ser en el pasado")
    
    return fecha_inicio

def clean(self):
    cleaned_data = super().clean()
    fecha_inicio = cleaned_data.get('fecha_inicio')
    fecha_fin = cleaned_data.get('fecha_fin')
    
    if fecha_inicio and fecha_fin:
        # Fecha fin debe ser posterior
        if fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        # No puede durar más de 1 año
        if (fecha_fin - fecha_inicio).days > 365:
            raise forms.ValidationError("El torneo no puede durar más de 1 año")
    
    return cleaned_data
```

---

#### ✅ Campo: `descripcion`
**Validaciones actuales:** TextField básico
**Validaciones recomendadas:**
- ✨ Longitud mínima de 20 caracteres
- ✨ Longitud máxima de 500 caracteres

**Ejemplo de validación:**
```python
def clean_descripcion(self):
    descripcion = self.cleaned_data.get('descripcion').strip()
    
    # Longitud mínima
    if len(descripcion) < 20:
        raise forms.ValidationError("La descripción debe tener al menos 20 caracteres")
    
    # Longitud máxima
    if len(descripcion) > 500:
        raise forms.ValidationError("La descripción no puede exceder 500 caracteres")
    
    return descripcion
```

---

## ⚽ 3. FORMULARIOS DE PARTIDOS (core/forms.py)

### 3.1 **PartidoForm**

#### ✅ Campos: `fecha` y `hora`
**Validaciones actuales:** DateInput y TimeInput widgets
**Validaciones recomendadas:**
- ✨ La fecha no puede ser en el pasado
- ✨ La hora debe estar en horario de operación (8:00 AM - 10:00 PM)
- ✨ No puede haber otro partido en la misma cancha a la misma hora

**Ejemplo de validación:**
```python
from datetime import datetime, time

def clean_fecha(self):
    fecha = self.cleaned_data.get('fecha')
    
    # No puede ser en el pasado
    if fecha < date.today():
        raise forms.ValidationError("La fecha del partido no puede ser en el pasado")
    
    return fecha

def clean_hora(self):
    hora = self.cleaned_data.get('hora')
    
    # Horario de operación
    hora_apertura = time(8, 0)  # 8:00 AM
    hora_cierre = time(22, 0)   # 10:00 PM
    
    if hora < hora_apertura or hora > hora_cierre:
        raise forms.ValidationError("El partido debe ser entre 8:00 AM y 10:00 PM")
    
    return hora

def clean(self):
    cleaned_data = super().clean()
    cancha = cleaned_data.get('cancha')
    fecha = cleaned_data.get('fecha')
    hora = cleaned_data.get('hora')
    
    if cancha and fecha and hora:
        # Verificar conflictos de horario
        conflicto = Partido.objects.filter(
            cancha=cancha,
            fecha=fecha,
            hora=hora
        ).exclude(pk=self.instance.pk if self.instance else None)
        
        if conflicto.exists():
            raise forms.ValidationError("Ya existe un partido en esta cancha a esta hora")
    
    return cleaned_data
```

---

#### ✅ Campo: `marcador`
**Validaciones actuales:** CharField opcional
**Validaciones recomendadas:**
- ✨ Formato válido: "X-Y" (ejemplo: "3-2", "6-4")
- ✨ Solo números y guión

**Ejemplo de validación:**
```python
def clean_marcador(self):
    marcador = self.cleaned_data.get('marcador')
    
    if marcador:
        # Formato válido
        if not re.match(r'^\d+-\d+$', marcador):
            raise forms.ValidationError("El marcador debe tener el formato X-Y (ejemplo: 3-2)")
        
        # Extraer puntajes
        puntajes = marcador.split('-')
        puntaje1 = int(puntajes[0])
        puntaje2 = int(puntajes[1])
        
        # Validar que sean razonables
        if puntaje1 > 99 or puntaje2 > 99:
            raise forms.ValidationError("Los puntajes no pueden ser mayores a 99")
    
    return marcador
```

---

## 🏟️ 4. FORMULARIOS DE CANCHAS (core/forms.py)

### 4.1 **CanchaForm**

#### ✅ Campo: `nombre`
**Validaciones actuales:** CharField básico
**Validaciones recomendadas:**
- ✨ Longitud mínima de 3 caracteres
- ✨ No permitir nombres duplicados

**Ejemplo de validación:**
```python
def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre').strip()
    
    # Longitud mínima
    if len(nombre) < 3:
        raise forms.ValidationError("El nombre de la cancha debe tener al menos 3 caracteres")
    
    # Verificar duplicados
    if Cancha.objects.filter(nombre__iexact=nombre).exists():
        raise forms.ValidationError("Ya existe una cancha con este nombre")
    
    return nombre
```

---

#### ✅ Campo: `ubicacion`
**Validaciones actuales:** CharField básico
**Validaciones recomendadas:**
- ✨ Longitud mínima de 10 caracteres
- ✨ Debe contener información útil

**Ejemplo de validación:**
```python
def clean_ubicacion(self):
    ubicacion = self.cleaned_data.get('ubicacion').strip()
    
    # Longitud mínima
    if len(ubicacion) < 10:
        raise forms.ValidationError("La ubicación debe ser más descriptiva (mínimo 10 caracteres)")
    
    return ubicacion
```

---

#### ✅ Campo: `imagen`
**Validaciones actuales:** ImageField básico
**Validaciones recomendadas:**
- ✨ Solo formatos permitidos: JPG, PNG, WEBP
- ✨ Tamaño máximo: 5MB
- ✨ Dimensiones mínimas: 800x600 px

**Ejemplo de validación:**
```python
from PIL import Image

def clean_imagen(self):
    imagen = self.cleaned_data.get('imagen')
    
    if imagen:
        # Tamaño máximo
        if imagen.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("La imagen no puede pesar más de 5MB")
        
        # Verificar dimensiones
        img = Image.open(imagen)
        width, height = img.size
        
        if width < 800 or height < 600:
            raise forms.ValidationError("La imagen debe tener al menos 800x600 píxeles")
    
    return imagen
```

---

## 📅 5. FORMULARIOS DE RESERVAS (core/forms.py)

### 5.1 **ReservaCanchaForm**

#### ✅ Campos: `hora_inicio` y `hora_fin`
**Validaciones actuales:** TimeInput widget
**Validaciones recomendadas:**
- ✨ La hora de fin debe ser posterior a la hora de inicio
- ✨ Duración mínima: 1 hora
- ✨ Duración máxima: 4 horas
- ✨ Horario de operación: 8:00 AM - 10:00 PM
- ✨ No puede haber otra reserva en el mismo horario

**Ejemplo de validación:**
```python
from datetime import datetime, timedelta

def clean_hora_inicio(self):
    hora_inicio = self.cleaned_data.get('hora_inicio')
    
    # Horario de operación
    hora_apertura = time(8, 0)
    hora_cierre = time(22, 0)
    
    if hora_inicio < hora_apertura or hora_inicio > hora_cierre:
        raise forms.ValidationError("Las reservas deben ser entre 8:00 AM y 10:00 PM")
    
    return hora_inicio

def clean(self):
    cleaned_data = super().clean()
    hora_inicio = cleaned_data.get('hora_inicio')
    hora_fin = cleaned_data.get('hora_fin')
    cancha = cleaned_data.get('cancha')
    fecha = cleaned_data.get('fecha')
    
    if hora_inicio and hora_fin:
        # Hora fin debe ser posterior
        if hora_fin <= hora_inicio:
            raise forms.ValidationError("La hora de fin debe ser posterior a la hora de inicio")
        
        # Calcular duración
        inicio_dt = datetime.combine(date.today(), hora_inicio)
        fin_dt = datetime.combine(date.today(), hora_fin)
        duracion = (fin_dt - inicio_dt).seconds / 3600  # en horas
        
        # Duración mínima
        if duracion < 1:
            raise forms.ValidationError("La reserva debe ser de al menos 1 hora")
        
        # Duración máxima
        if duracion > 4:
            raise forms.ValidationError("La reserva no puede ser mayor a 4 horas")
    
    # Verificar conflictos de horario
    if cancha and fecha and hora_inicio and hora_fin:
        conflictos = ReservaCancha.objects.filter(
            cancha=cancha,
            fecha=fecha,
            estado__in=['pendiente', 'confirmada']
        ).exclude(pk=self.instance.pk if self.instance else None)
        
        for reserva in conflictos:
            # Verificar solapamiento
            if (hora_inicio < reserva.hora_fin and hora_fin > reserva.hora_inicio):
                raise forms.ValidationError(
                    f"Ya existe una reserva en este horario ({reserva.hora_inicio} - {reserva.hora_fin})"
                )
    
    return cleaned_data
```

---

## 📰 6. FORMULARIOS DE NOTICIAS Y HERO (core/forms.py)

### 6.1 **NoticiaForm**

#### ✅ Campo: `titulo`
**Validaciones actuales:** CharField básico
**Validaciones recomendadas:**
- ✨ Longitud mínima de 10 caracteres
- ✨ Longitud máxima de 150 caracteres

**Ejemplo de validación:**
```python
def clean_titulo(self):
    titulo = self.cleaned_data.get('titulo').strip()
    
    # Longitud mínima
    if len(titulo) < 10:
        raise forms.ValidationError("El título debe tener al menos 10 caracteres")
    
    return titulo
```

---

#### ✅ Campo: `cuerpo`
**Validaciones actuales:** TextField básico
**Validaciones recomendadas:**
- ✨ Longitud mínima de 50 caracteres
- ✨ Longitud máxima de 5000 caracteres

**Ejemplo de validación:**
```python
def clean_cuerpo(self):
    cuerpo = self.cleaned_data.get('cuerpo').strip()
    
    # Longitud mínima
    if len(cuerpo) < 50:
        raise forms.ValidationError("El cuerpo de la noticia debe tener al menos 50 caracteres")
    
    # Longitud máxima
    if len(cuerpo) > 5000:
        raise forms.ValidationError("El cuerpo no puede exceder 5000 caracteres")
    
    return cuerpo
```

---

### 6.2 **HeroForm**

#### ✅ Campos: `titulo` y `subtitulo`
**Validaciones actuales:** CharField básico
**Validaciones recomendadas:**
- ✨ Título: longitud mínima de 5 caracteres
- ✨ Subtítulo: longitud mínima de 10 caracteres

**Ejemplo de validación:**
```python
def clean_titulo(self):
    titulo = self.cleaned_data.get('titulo').strip()
    
    if len(titulo) < 5:
        raise forms.ValidationError("El título debe tener al menos 5 caracteres")
    
    return titulo

def clean_subtitulo(self):
    subtitulo = self.cleaned_data.get('subtitulo').strip()
    
    if len(subtitulo) < 10:
        raise forms.ValidationError("El subtítulo debe tener al menos 10 caracteres")
    
    return subtitulo
```

---

## 🎨 7. VALIDACIONES EN EL FRONTEND (HTML5)

Además de las validaciones en el backend (Python), también puedes agregar validaciones en el frontend usando atributos HTML5:

### Ejemplos de atributos HTML5:

```html
<!-- Solo números -->
<input type="text" pattern="[0-9]+" title="Solo números">

<!-- Email -->
<input type="email" required>

<!-- Teléfono -->
<input type="tel" pattern="[0-9]{4}-[0-9]{7}" placeholder="0414-1234567">

<!-- Longitud mínima/máxima -->
<input type="text" minlength="5" maxlength="100">

<!-- Rango numérico -->
<input type="number" min="0" max="1000">

<!-- Fecha mínima/máxima -->
<input type="date" min="2025-01-01">

<!-- Campo requerido -->
<input type="text" required>
```

---

## 📊 RESUMEN DE VALIDACIONES POR PRIORIDAD

### 🔴 **PRIORIDAD ALTA** (Seguridad y datos críticos)
1. ✅ Cédula: solo números, longitud válida, sin duplicados
2. ✅ Email: formato válido, sin duplicados
3. ✅ Contraseña: requisitos de seguridad
4. ✅ Fechas: no en el pasado, rangos válidos
5. ✅ Conflictos de horario: partidos y reservas

### 🟡 **PRIORIDAD MEDIA** (Calidad de datos)
6. ✅ Nombres y apellidos: solo letras
7. ✅ Teléfono: formato venezolano
8. ✅ Marcador: formato válido
9. ✅ Imágenes: tamaño y formato
10. ✅ Textos: longitudes mínimas/máximas

### 🟢 **PRIORIDAD BAJA** (Mejoras de UX)
11. ✅ Auto-formateo: capitalización, espacios
12. ✅ Mensajes de ayuda: placeholders descriptivos
13. ✅ Validaciones en tiempo real con JavaScript

---

## 🚀 PRÓXIMOS PASOS

1. **Implementar validaciones de prioridad alta** en `core/forms.py` y `users/forms.py`
2. **Agregar validaciones HTML5** en los templates
3. **Crear mensajes de error personalizados** en español
4. **Agregar validaciones JavaScript** para feedback en tiempo real
5. **Documentar las validaciones** para futuros desarrolladores

---

## 📝 NOTAS FINALES

- Todas las validaciones deben tener **mensajes de error claros** en español
- Siempre validar **tanto en frontend como en backend** (seguridad)
- Usar **regex** para patrones complejos
- Considerar la **experiencia del usuario** al definir restricciones
- **Probar exhaustivamente** cada validación

---

**Documento creado:** 2025-12-03
**Autor:** Antigravity AI
**Proyecto:** ASOPADEL - Sistema de Gestión de Torneos de Pádel
