#!/usr/bin/env python3
# -*- coding: utf-8 -*-

file_path = '/app/templates/core/partidos/confirmar_eliminar_partido.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire Equipo 2 section with properly formatted code
import re

# Find and replace the Equipo 2 player listing section
old_pattern = r'<small class="text-muted ms-2">Equipo 2:</small>\s+{% for jugador in partido\.equipo2\.all %}\s+{{ jugador\.get_full_name }}{% if not forloop\.last %}, {% endif %}\s+{% endfor %}'

new_text = '''<small class="text-muted ms-2">Equipo 2:</small>
                                {% for jugador in partido.equipo2.all %}
                                {{ jugador.get_full_name }}{% if not forloop.last %}, {% endif %}
                                {% endfor %}'''

content = re.sub(old_pattern, new_text, content, flags=re.MULTILINE | re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Equipo 2 section fixed!")
