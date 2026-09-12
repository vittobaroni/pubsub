import grpc
import pubsub_pb2
import pubsub_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")

stub = pubsub_pb2_grpc.PubSubServiceStub(channel)

noticias = stub.Subscribe(
    pubsub_pb2.SubscribeRequest(
        subscriber_id="teste1",
        topic="Nintendo"
    )
)

for noticia in noticias:
    print(noticia.titulo)
    print(noticia.conteudo)