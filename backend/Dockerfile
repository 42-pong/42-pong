# syntax=docker/dockerfile:1

FROM python:3.13

WORKDIR /pong

# todo: 一旦全部
COPY . .

# todo: pythonの簡易的なserver起動(仮)。Djangoを入れたらDjango起動に変更
CMD ["python", "-m", "http.server", "8000"]

