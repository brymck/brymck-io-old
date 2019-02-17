#!/bin/bash -eu
python -c 'import grpc_tools' >/dev/null 2>&1 || pip install grpcio-tools
protodir=../../protobuf
python -m grpc_tools.protoc -I "$protodir" --python_out=. --grpc_python_out=. "$protodir/demo.proto"
