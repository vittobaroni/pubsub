import grpc
import queue
from concurrent import futures

import pubsub_pb2
import pubsub_pb2_grpc

class PubSubService(pubsub_pb2_grpc.PubSubServiceServicer):
    def __init__(self):
        self.subscribers = {}

    def Subscribe(self, request, context):
        topic = request.topic
        subscriber_id = request.subscriber_id

        if topic not in self.subscribers:
            self.subscribers[topic] = {}

        subscriber_queue = queue.Queue()
        self.subscribers[topic][subscriber_id] = subscriber_queue

        while True:
            noticia = subscriber_queue.get()
            yield noticia #com yield o método continua ativo

    def Publish(self, request, context):
        topic = request.topic
        noticia = pubsub_pb2.Noticia(
            topic=request.topic,
            titulo=request.titulo,
            conteudo=request.conteudo
        )
        if topic in self.subscribers:
            for subscriber_id, subscriber_queue in self.subscribers[topic].items():
                subscriber_queue.put(noticia)

        return pubsub_pb2.PublishResponse(success=True)

    def Unsubscribe(self, request, context):
        topic = request.topic
        subscriber_id = request.subscriber_id

        if topic in self.subscribers:
            if subscriber_id in self.subscribers[topic]:
                del self.subscribers[topic][subscriber_id]

        return pubsub_pb2.UnsubscribeResponse(success=True)

    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    pubsub_pb2_grpc.add_PubSubServiceServicer_to_server(
        PubSubService(),
        server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("Broker rodando na porta 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()        
    