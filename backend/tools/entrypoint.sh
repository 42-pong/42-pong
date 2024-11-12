#!/bin/bash

python3 manage.py migrate --noinput


exec "$@"
