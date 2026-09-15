# Sistema Distribuído de Notícias Pub/Sub

Um portal de notícias distribuído em tempo real que implementa o padrão arquitetural **Publish-Subscribe (Pub/Sub)** utilizando **gRPC** e **Python**.

Este projeto demonstra como desacoplar produtores de informação (Publishers) de consumidores (Subscribers) através de um Broker central. Ele permite a transmissão de mensagens em tempo real e de forma eficiente, baseada em tópicos específicos.

#Alunos : Edgar Lutterbach, Gabriel Ramalho, Henrique Couri e Vitto Baroni

## 🚀 Funcionalidades

- **Streaming de Dados em Tempo Real**: Utiliza *Server Streaming* do gRPC para enviar notícias aos assinantes instantaneamente.
- **Filtragem por Tópicos**: Os assinantes recebem apenas as notícias dos tópicos nos quais se inscreveram (ex: `League_of_Legends`, `Minecraft`).
- **Desacoplamento Total**: Publishers e Subscribers não precisam se conhecer. O Broker cuida de todo o roteamento.
- **Processamento Concorrente**: Consumo multi-thread no lado do cliente e filas *thread-safe* no lado do servidor.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Framework RPC**: [gRPC](https://grpc.io/) (Baseado em HTTP/2)
- **Serialização**: Protocol Buffers (Protobuf v3)

## 🏗️ Arquitetura

O sistema é dividido em três componentes principais:

1. **Broker (`server.py`)**: O servidor gRPC central que roda na porta `50051`. Ele gerencia as conexões dos clientes, rastreia as inscrições ativas por tópico e roteia as mensagens recebidas dos publishers para os assinantes apropriados.
2. **Publisher (`publisher.py`)**: Um script automatizado que se conecta ao broker e publica continuamente notícias simuladas sobre jogos em vários tópicos.
3. **Subscriber (`subscriber.py`)**: Um cliente interativo de linha de comando. Os usuários podem se inscrever ou cancelar a inscrição em tópicos de forma dinâmica, enquanto uma thread em segundo plano escuta por novas notícias sem bloquear a interface.

## ⚙️ Pré-requisitos e Instalação

1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   
   # No Windows:
   .\venv\Scripts\activate
   
   # No Linux/macOS:
   source venv/bin/activate
   ```
3. Instale as dependências necessárias do gRPC:
   ```bash
   pip install grpcio grpcio-tools
   ```

*(Nota: Os arquivos Protobuf já estão compilados no repositório (`pubsub_pb2.py`, `pubsub_pb2_grpc.py`). Se você alterar o arquivo `pubsub.proto`, precisará recompilá-los).*

## 🎮 Como Executar

Para ver o sistema funcionando, recomendamos abrir **três janelas de terminal separadas**. Certifique-se de que o ambiente virtual está ativado em todas elas.

### 1. Inicie o Broker
No primeiro terminal, inicie o servidor gRPC:
```bash
python server.py
```
*O servidor começará a escutar na porta 50051.*

### 2. Conecte um Subscriber (Assinante)
No segundo terminal, execute o cliente interativo:
```bash
python subscriber.py
```
- Digite um nome de usuário quando solicitado.
- Use o comando `inscrever` e digite um tópico como `League_of_Legends` ou `Minecraft`.
- Deixe o cliente rodando. Ele vai escutar as notícias em segundo plano.

### 3. Publique Notícias
No terceiro terminal, execute o script do publisher:
```bash
python publisher.py
```
*O publisher começará a enviar notícias para o broker. Fique de olho no terminal do seu Subscriber: você receberá instantaneamente as notícias que correspondem aos tópicos que você assinou!*

## 🧪 Rodando os Testes

O projeto inclui scripts de testes isolados para verificar funcionalidades específicas. Com o Broker (`server.py`) rodando, você pode testar:

- `python teste_broker.py`: Publica uma mensagem e já assina para recebê-la simultaneamente.
- `python teste_subscriber.py`: Assina automaticamente o tópico "Nintendo" e aguarda mensagens.
- `python teste_unsubscribe.py`: Valida a lógica de cancelamento de inscrição e a resposta do servidor.
