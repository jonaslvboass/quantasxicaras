# Recommender Service

Este serviço é responsável por processar requisições de recomendação de receitas de forma assíncrona, utilizando RabbitMQ para comunicação com a aplicação principal.

## Como funciona

- Consome mensagens da fila `recommendation_requests`.
- Processa a recomendação para o usuário.
- Publica a resposta na fila `recommendation_responses`.

## Dependências

- Python 3.8+
- pika

Instale as dependências com:

```bash
pip install -r requirements.txt
```
