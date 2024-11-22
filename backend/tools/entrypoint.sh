#!/bin/bash

# エラーが発生した場合にスクリプトの実行を停止する
set -e

# todo: makemigrationsなど
python3 manage.py migrate --noinput

python3 manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
    def get_env_value(key: str) -> str:
        value: str | None = os.getenv(key)
        if not value:
            raise ValueError("{key} is not set in environment variables")
        return value

    SUPERUSER_NAME = get_env_value("SUPERUSER_NAME")
    SUPERUSER_EMAIL = get_env_value("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD = get_env_value("SUPERUSER_PASSWORD")

    User.objects.create_superuser(
        username=SUPERUSER_NAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )
    print(f"Superuser '{SUPERUSER_NAME}' created successfully")
else:
    print("Superuser already exists")
EOF

exec "$@"
