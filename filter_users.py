import json

with open('backup_data.json', 'r') as f:
    data = json.load(f)

users = [item for item in data if item['model'] == 'users.usuario']

with open('users_only.json', 'w') as f:
    json.dump(users, f, indent=2)

print(f"Extracted {len(users)} users.")
