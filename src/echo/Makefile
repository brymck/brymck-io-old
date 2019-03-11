proto: proto-server proto-proxy proto-openapi

init:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go
	pip install grpcio-tools

proto-server:
	python -m grpc_tools.protoc -I/usr/local/include -I. \
        -I${GOPATH}/src \
        -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
        --python_out=service \
        --grpc_python_out=service \
        echo.proto

proto-proxy:
	protoc -I/usr/local/include -I. \
		-I${GOPATH}/src \
	    -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
	    --go_out=plugins=grpc:proxy \
	    --grpc-gateway_out=logtostderr=true:proxy \
	    echo.proto

proto-openapi:
	protoc -I/usr/local/include -I. \
	    -I${GOPATH}/src \
	    -I${GOPATH}/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
	    --swagger_out=logtostderr=true:openapi \
	    echo.proto

.PHONY: \
	all \
	init \
	proto-server \
	proto-proxy \
	proto-openapi
