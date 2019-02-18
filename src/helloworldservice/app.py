import os
import time
from concurrent.futures import ThreadPoolExecutor

import grpc
from grpc_health.v1.health import HealthServicer
from opencensus.trace.exporters.stackdriver_exporter import StackdriverExporter
from opencensus.trace.ext.grpc.server_interceptor import OpenCensusServerInterceptor
from opencensus.trace.samplers.always_on import AlwaysOnSampler

import demo_pb2
import demo_pb2_grpc
from grpc_health.v1.health_pb2 import HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server

from logger import get_json_logger

logger = get_json_logger("helloworldservice")


class HelloWorldService(demo_pb2_grpc.HelloWorldServiceServicer):
    def Greet(self, request, context):
        response = demo_pb2.GreetResponse()
        response.message = f"Hello, {request.name}"
        return response

    def Check(self, request, context):
        return HealthCheckResponse(status=HealthCheckResponse.SERVING)


def serve():
    logger.info("initializing frontend")

    try:
        sampler = AlwaysOnSampler()
        exporter = StackdriverExporter()
        tracer_interceptor = OpenCensusServerInterceptor(sampler, exporter)
    except:
        tracer_interceptor = OpenCensusServerInterceptor()

    port = os.environ.get("PORT", "8080")

    server = grpc.server(ThreadPoolExecutor(max_workers=3))

    service = HelloWorldService()
    demo_pb2_grpc.add_HelloWorldServiceServicer_to_server(service, server)
    add_HealthServicer_to_server(service, server)

    logger.info(f"listening on port: {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
