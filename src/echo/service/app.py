from concurrent import futures
import time

import grpc

from grpc_health.v1.health_pb2 import HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server
import your_service_pb2_grpc
import your_service_pb2

from logger import get_json_logger

logger = get_json_logger("echo")
port = "9090"


class Greeter(your_service_pb2_grpc.YourServiceServicer):
    def Echo(self, request, context):
        print("hi")
        return your_service_pb2.StringMessage(value='Hello, {}'.format('world'))

    def Check(self, request, context):
        return HealthCheckResponse(status=HealthCheckResponse.SERVING)


def serve():
    service = Greeter()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))

    your_service_pb2_grpc.add_YourServiceServicer_to_server(service, server)
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

