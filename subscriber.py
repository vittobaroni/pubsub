import grpc
import threading

import pubsub_pb2
import pubsub_pb2_grpc

ENDERECO = "localhost:50051"

# topico -> objeto de stream retornado pelo Subscribe
inscricoes = {}


def escutar_topico(stream, topico):
    # Roda em uma thread separada. Bloqueia consumindo o stream.
    try:
        for noticia in stream:
            print(f"\n[{noticia.topic}] {noticia.titulo}")
            print(f"  {noticia.conteudo}")
    except grpc.RpcError:
        print(f"\n[ENCERRADO] Stream do topico '{topico}' foi fechado.")


def inscrever(stub, subscriber_id, topico):
    if topico in inscricoes:
        print(f"[AVISO] Voce ja esta inscrito em '{topico}'.")
        return

    requisicao = pubsub_pb2.SubscribeRequest(
        subscriber_id=subscriber_id,
        topic=topico
    )

    # Nao bloqueia: retorna o iterador imediatamente
    stream = stub.Subscribe(requisicao)
    inscricoes[topico] = stream

    thread = threading.Thread(
        target=escutar_topico,
        args=(stream, topico),
        daemon=True
    )
    thread.start()

    print(f"[INSCRITO] Recebendo noticias de '{topico}'.")


def cancelar(stub, subscriber_id, topico):
    if topico not in inscricoes:
        print(f"[AVISO] Voce nao esta inscrito em '{topico}'.")
        return

    # 1. Avisa o broker para parar de enfileirar noticias para mim
    resposta = stub.Unsubscribe(
        pubsub_pb2.UnsubscribeRequest(
            subscriber_id=subscriber_id,
            topic=topico
        )
    )

    # 2. Cancela o stream: isso lanca RpcError na thread e ela termina
    inscricoes[topico].cancel()
    del inscricoes[topico]

    print(f"[CANCELADO] Broker confirmou: {resposta.success}")


def main():
    canal = grpc.insecure_channel(ENDERECO)
    stub = pubsub_pb2_grpc.PubSubServiceStub(canal)

    print("=== Subscriber do portal de noticias ===")
    subscriber_id = input("Seu identificador: ").strip() or "anonimo"
    print(f"Conectado como '{subscriber_id}'.")
    print("Comandos: inscrever | cancelar | listar | sair")

    while True:
        comando = input("\n> ").strip().lower()

        if comando == "inscrever":
            inscrever(stub, subscriber_id, input("Topico: ").strip())
        elif comando == "cancelar":
            cancelar(stub, subscriber_id, input("Topico: ").strip())
        elif comando == "listar":
            print("Inscricoes ativas:", list(inscricoes.keys()) or "nenhuma")
        elif comando == "sair":
            for topico in list(inscricoes.keys()):
                cancelar(stub, subscriber_id, topico)
            canal.close()
            print("Encerrando.")
            break
        else:
            print("Comando invalido.")


if __name__ == "__main__":
    main()