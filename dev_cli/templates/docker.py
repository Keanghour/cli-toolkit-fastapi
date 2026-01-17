# cnb_cli/templates/docker.py

DOCKERFILE = """\
FROM nexus-mirror.xxxx.com/docker-proxy/python:3.10.12-slim

ENV PYTHONUNBUFFERED=1

RUN echo 'Asia/Bangkok' | tee /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Bangkok /etc/localtime

WORKDIR /app

COPY pip.conf /etc/
ADD . /app

RUN pip cache purge
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
"""
