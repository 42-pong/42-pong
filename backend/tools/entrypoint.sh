#!/bin/bash

# todo: createsuperuserなど

# DBのmigrationを実行
python manage.py migrate

exec "$@"
