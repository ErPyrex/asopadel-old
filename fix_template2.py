#!/usr/bin/env python3
# -*- coding: utf-8 -*-

file_path = '/app/templates/core/partidos/confirmar_eliminar_partido.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken template tag for Equipo 2 player name
# The issue is likely on line 34 where it's split across lines
import re

# Replace any instance where get_full_name is split across lines
content = re.sub(
    r'{{\s*jugador\.get_full_name\s*}}',
    '{{ jugador.get_full_name }}',
    content,
    flags=re.MULTILINE | re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template tags fixed successfully!")
