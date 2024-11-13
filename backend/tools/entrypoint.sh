#!/bin/bash

python3 manage.py migrate --noinput

# todo: username, email. passwordの環境変数で登録
python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
	username = 'admin'
	email = 'admin@example.com'
	password = 'password'
	User.objects.create_superuser(username=username, email=email, password=password)
	print(f"Superuser '{username}' created successfully")
else:
	print(f"Superuser already exists")
EOF

exec "$@"
