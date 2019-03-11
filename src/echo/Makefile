all: grpc grpc-gateway grpc-python openapi proxy

init:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go
	pip install grpcio-tools

grpc:
	protoc -I/usr/local/include -I. \
	    -I${GOPATH}/src \
	    -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
	    --go_out=plugins=grpc:proxy \
	    your_service.proto

grpc-python:
	python -m grpc_tools.protoc -I/usr/local/include -I. \
        -I${GOPATH}/src \
        -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
        --python_out=. \
        --grpc_python_out=. \
        your_service.proto

grpc-gateway:
	protoc -I/usr/local/include -I. \
		-I${GOPATH}/src \
	    -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
	    --grpc-gateway_out=logtostderr=true:proxy \
	    your_service.proto

openapi:
	protoc -I/usr/local/include -I. \
	    -I${GOPATH}/src \
	    -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
	    --swagger_out=logtostderr=true:openapi \
	    your_service.proto

proxy:
	go build proxy/...

.PHONY: all init grpc grpc-gateway grpc-python openapi proxy
