#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os

file_path = '/app/templates/core/partidos/lista_partidos.html'

if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original content length:", len(content))

# Maps of regex pattern to replacement string
replacements = [
    (
        r'{{\s*partido\.torneo\.nombre\s*\|\s*default\s*:\s*["\']Partido\s+Amistoso\s*/\s*Casual["\']\s*}}',
        '{{ partido.torneo.nombre|default:"Partido Amistoso / Casual" }}'
    ),
    (
        r'{{\s*partido\.cancha\.nombre\s*\|\s*default\s*:\s*["\']No\s+asignada["\']\s*}}',
        '{{ partido.cancha.nombre|default:"No asignada" }}'
    ),
    (
        r'{{\s*partido\.fecha\s+a\s+las\s+{{\s*partido\.hora\s*}}\s*}}', # This might be nested or adjacent, let's fix parts individually
        None # logic handled below
    ),
     (
        r'{{\s*partido\.hora\s*}}',
        '{{ partido.hora }}'
    ),
    (
        r'{{\s*partido\.fecha\s*}}',
        '{{ partido.fecha }}'
    )
]

# Apply regex replacements allowing for multiline and dotall
# Fix Torneo Name
content = re.sub(
    r'{{\s*partido\.torneo\.nombre\s*\|\s*default\s*:\s*["\']Partido\s*Amistoso\s*/\s*Casual["\']\s*}}',
    '{{ partido.torneo.nombre|default:"Partido Amistoso / Casual" }}',
    content,
    flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
)

# Fix Cancha Name
content = re.sub(
    r'{{\s*partido\.cancha\.nombre\s*\|\s*default\s*:\s*["\']No\s*asignada["\']\s*}}',
    '{{ partido.cancha.nombre|default:"No asignada" }}',
    content,
    flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
)

# Fix Fecha and Hora which seem to be {{ partido.fecha }} a las {{ partido.hora }}
# Sometimes these get split too.
content = re.sub(
    r'{{\s*partido\.fecha\s*}}',
    '{{ partido.fecha }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)
content = re.sub(
    r'{{\s*partido\.hora\s*}}',
    '{{ partido.hora }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

print("Fixed content length:", len(content))

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched lista_partidos.html")
