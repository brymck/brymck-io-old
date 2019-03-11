FROM python:3.7-slim
RUN apt-get update -qqy && \
    apt-get -qqy install wget && \
    rm -rf /var/lib/apt/lists/*

# Show Python logs as they occur
ENV PYTHONUNBUFFERED=0

# Download the gRPC health probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.2.0 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

# Get packages
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PORT 9090
EXPOSE 9090

CMD ["python", "/app/app.py"]
