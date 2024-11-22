#!/bin/bash

# todo: makemigrationsなど
python3 manage.py migrate --noinput

python3 manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

# 以下場合はエラー
# - 環境変数が存在しない場合
# - 空文字列の場合
SUPERUSER_NAME = os.getenv('SUPERUSER_NAME')
if not SUPERUSER_NAME:
    raise ValueError("SUPERUSER_NAME is not set in environment variables")
SUPERUSER_EMAIL = os.getenv('SUPERUSER_EMAIL')
if not SUPERUSER_EMAIL:
    raise ValueError("SUPERUSER_EMAIL is not set in environment variables")
SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD')
if not SUPERUSER_PASSWORD:
    raise ValueError("SUPERUSER_PASSWORD is not set in environment variables")

User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
	User.objects.create_superuser(username=SUPERUSER_NAME, email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)
	print(f"Superuser '{SUPERUSER_NAME}' created successfully")
else:
	print(f"Superuser already exists")
EOF

exec "$@"
