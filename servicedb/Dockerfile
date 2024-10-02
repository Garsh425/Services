FROM registry.astralinux.ru/library/astra/ubi18-python311:latest
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /venv
RUN /venv/bin/pip install --no-cache-dir --upgrade pip
RUN /venv/bin/pip install --no-cache-dir pika
RUN /venv/bin/pip install --no-cache-dir psycopg2-binary
RUN /venv/bin/pip install --no-cache-dir tornado
COPY . .
ENV PATH="/venv/bin:$PATH"
EXPOSE 5000
CMD ["python3", "index.py"]