FROM python:3.10-slim

WORKDIR /app
RUN pip install --no-cache-dir Flask web3 gunicorn

COPY ./faucet.py /app/faucet.py

RUN useradd -s /bin/bash admin
RUN chown -R admin /app

USER admin
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:9000 --threads=4 --worker-class=gthread"
EXPOSE 9000
CMD ["gunicorn", "faucet:app"]
