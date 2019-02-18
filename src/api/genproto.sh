#!/bin/bash -eu
protodir=../../protobuf
mkdir -p genproto
protoc --go_out=plugins=grpc:genproto -I $protodir $protodir/demo.proto
