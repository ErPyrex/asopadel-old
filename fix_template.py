#!/usr/bin/env python3
# -*- coding: utf-8 -*-

file_path = '/app/templates/core/partidos/confirmar_eliminar_partido.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 45-46
new_lines = []
i = 0
while i < len(lines):
    if i == 44:  # Line 45 (0-indexed)
        # Skip lines 45 and 46, replace with fixed version
        new_lines.append('                            <p class="mb-1"><strong>Árbitro:</strong> {{ partido.arbitro.get_full_name|default:"No asignado" }}</p>\n')
        i += 2  # Skip next line too
    else:
        new_lines.append(lines[i])
        i += 1

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("File fixed successfully!")
