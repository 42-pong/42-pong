# syntax=docker/dockerfile:1

FROM python:3.13

WORKDIR /pong

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY ./tools/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# todo: USER設定

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# defaultはlocalhostのみにbindされるため0.0.0.0を指定
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
