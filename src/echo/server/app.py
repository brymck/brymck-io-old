from concurrent import futures
import os
import time

import grpc
from grpc_health.v1.health_pb2 import HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server
import psycopg2

import echo_pb2_grpc
import echo_pb2
from logger import get_json_logger

logger = get_json_logger("echo")
port = "9090"


class EchoService(echo_pb2_grpc.EchoServiceServicer):
    def __init__(self):
        psql_host, psql_port = os.environ['POSTGRES_DB_HOST'].split(':')
        logger.info(f"psql_host: {psql_host}, psql_port: {psql_port}")
        self._conn = psycopg2.connect(
            user=os.environ['POSTGRES_DB_USER'],
            password=os.environ['POSTGRES_DB_PASSWORD'],
            host=psql_host,
            port=psql_port,
        )
        logger.info("Done creating connection")

    def Echo(self, request, context):
        cur = self._conn.cursor()
        cur.execute('select name from names')
        name, = cur.fetchone()
        self._conn.commit()
        cur.close()
        return echo_pb2.StringMessage(value=f"Hello, {name}!")

    def Check(self, request, context):
        return HealthCheckResponse(status=HealthCheckResponse.SERVING)


def serve():
    service = EchoService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))

    echo_pb2_grpc.add_EchoServiceServicer_to_server(service, server)
    add_HealthServicer_to_server(service, server)

    logger.info(f"listening on port: {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

