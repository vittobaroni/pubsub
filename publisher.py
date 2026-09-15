import grpc
import time

import pubsub_pb2
import pubsub_pb2_grpc

def iniciar_publicador():
    # Conecta ao servidor Broker 
    canal = grpc.insecure_channel('localhost:50051')
    
    stub = pubsub_pb2_grpc.PubSubServiceStub(canal)

    #lista de noticias de jogos
    noticias = [
        {
            "topic": "League_of_Legends",
            "titulo": "Mundial 2026",
            "conteudo": "Gen-G, T1, HLE e DK são as confirmadas coreanas para o mundial deste ano."
        },
        {
            "topic": "Minecraft",
            "titulo": "Nova Snapshot Disponível",
            "conteudo": "A atualização 1.22 traz novos biomas e mecânicas aprimoradas de sobrevivência."
        },
        {
            "topic": "League_of_Legends",
            "titulo": "Novos Cosméticos",
            "conteudo": "Novas skins estão disponíveis na loja a partir do dia 31/02"
        },
        {
            "topic": "GTA_V",
            "titulo": "Recorde de Jogadores",
            "conteudo": "Servidores de Roleplay batem meta histórica de usuários simultâneos no fim de semana."
        },
        {
            "topic": "Fifa",
            "titulo": "Anuncio do fifa 27",
            "conteudo": "Dia de lançamento foi anunciado e os valores assustam"
        },
        {
            "topic": "Mario",
            "titulo": "Novo jogo do mario",
            "conteudo": "super mario galaxy 3 lançara em outubro de 2027"
        }
    ]

    print("Iniciando a transmissão de notícias no portal...\n")
    
    for noticia in noticias:
        print(f"[Enviando] [{noticia['topic']}] {noticia['titulo']}")
        
        # montando a requisição do .proto
        requisicao = pubsub_pb2.PublishRequest(
            topic=noticia["topic"],
            titulo=noticia["titulo"],
            conteudo=noticia["conteudo"]
        )
        
        # chama a função Publish no servidor
        resposta = stub.Publish(requisicao)
        
        # verifica resposta do .proto
        if resposta.success:
            print(" -> Sucesso --> Notícia entregue ao Broker!\n")
        else:
            print(" -> Falha --> O Broker não confirmou o recebimento.\n")
            
        time.sleep(2)

if __name__ == '__main__':
    iniciar_publicador()