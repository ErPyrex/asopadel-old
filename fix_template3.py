#!/usr/bin/env python3
# -*- coding: utf-8 -*-

file_path = '/app/templates/core/partidos/confirmar_eliminar_partido.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Print lines 32-36 to debug
print("Lines 32-36 before fix:")
for i in range(31, 36):
    print(f"Line {i+1}: {repr(lines[i])}")

# Fix line 34 specifically (index 33)
if len(lines) > 33:
    # Replace the problematic line
    lines[33] = '                                {{ jugador.get_full_name }}{% if not forloop.last %}, {% endif %}\n'

print("\nLine 34 after fix:")
print(f"Line 34: {repr(lines[33])}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nFile fixed successfully!")
