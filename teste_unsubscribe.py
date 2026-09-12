import grpc
import pubsub_pb2
import pubsub_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")

stub = pubsub_pb2_grpc.PubSubServiceStub(channel)

resposta = stub.Unsubscribe(
    pubsub_pb2.UnsubscribeRequest(
        subscriber_id="teste1",
        topic="Nintendo"
    )
)

print(resposta.success)