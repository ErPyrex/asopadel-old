#!/usr/bin/env python3
# -*- coding: utf-8 -*-

file_path = '/app/templates/core/partidos/lista_partidos.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all the template tags that might be broken
import re

# Fix partido.torneo.nombre
content = re.sub(
    r'{{\s*partido\.torneo\.nombre\s*\|\s*default\s*:\s*["\']Partido Amistoso / Casual["\']\s*}}',
    '{{ partido.torneo.nombre|default:"Partido Amistoso / Casual" }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# Fix partido.cancha.nombre
content = re.sub(
    r'{{\s*partido\.cancha\.nombre\s*\|\s*default\s*:\s*["\']No asignada["\']\s*}}',
    '{{ partido.cancha.nombre|default:"No asignada" }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# Fix partido.fecha
content = re.sub(
    r'{{\s*partido\.fecha\s*}}',
    '{{ partido.fecha }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# Fix partido.hora
content = re.sub(
    r'{{\s*partido\.hora\s*}}',
    '{{ partido.hora }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# Fix j.get_full_name
content = re.sub(
    r'{{\s*j\.get_full_name\s*}}',
    '{{ j.get_full_name }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

# Fix partido.arbitro.get_full_name
content = re.sub(
    r'{{\s*partido\.arbitro\.get_full_name\s*\|\s*default\s*:\s*["\']No asignado["\']\s*}}',
    '{{ partido.arbitro.get_full_name|default:"No asignado" }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("All template tags in lista_partidos.html fixed!")
