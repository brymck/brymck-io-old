package main

import (
	"context"
	pb "github.com/brymck/brymck-io/src/api/genproto"
)

func (fe *apiServer) greet(ctx context.Context, name string) (string, error) {
	resp, err := pb.NewHelloWorldServiceClient(fe.helloWorldSvcConn).
		Greet(ctx, &pb.GreetRequest{Name: name})
	return resp.GetMessage(), err
}
