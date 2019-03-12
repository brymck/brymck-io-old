package main

import (
  "flag"
  "net/http"

  "github.com/golang/glog"
  "github.com/grpc-ecosystem/grpc-gateway/runtime"
  "golang.org/x/net/context"
  "google.golang.org/grpc"
)

const (
  endpoint = ":9090"
)

func init() {
  if err := flag.Set("logtostderr", "true"); err != nil {
    glog.Error(err)
  }
}

func run() error {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithInsecure()}

	err := RegisterEchoServiceHandlerFromEndpoint(ctx, mux, endpoint, opts)
	if err != nil {
	  glog.Error(err)
		return err
	}

	return http.ListenAndServe(":8080", mux)
}

func main() {
	flag.Parse()
	defer glog.Flush()

	if err := run(); err != nil {
		glog.Fatal(err)
	}
}
