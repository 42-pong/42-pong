#!/bin/bash

python3 manage.py migrate --noinput

# todo: username, email. passwordの環境変数で登録
python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model

username = 'admin'
email = 'admin@example.com'
password = 'password'

User = get_user_model()
User.objects.create_superuser(username=username, email=email, password=password)
EOF

exec "$@"
