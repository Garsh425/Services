FROM registry.astralinux.ru/library/astra/ubi18-python311:latest
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv venv
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["./venv/bin/python", "index.py"]