# Country Catalog API

Este projeto é uma API REST desenvolvida em Python com FastAPI que consome a API pública [REST Countries](https://restcountries.com) para listar, buscar e avaliar países. As avaliações são persistidas em um banco de dados SQLite, e os resultados incluem informações como nome, população, continente e contagem de curtidas/não curtidas.

## Funcionalidades

- **Listar os 10 países mais populosos**: Endpoint `GET /paises/top10` retorna os 10 países com maior população, incluindo nome, população, continente e avaliações.
- **Buscar um país pelo nome**: Endpoint `GET /paises/buscar?nome=<nome>` retorna os dados de um país específico no mesmo formato.
- **Avaliar um país**: Endpoint `POST /paises/avaliar` permite registrar uma avaliação ("curti" ou "nao_curti") para um país, salvando no banco e retornando o status e total de votos.

## Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal.
- **FastAPI**: Framework para criação da API.
- **SQLite**: Banco de dados leve para persistência de avaliações.
- **Bibliotecas**:
  - `fastapi`: Para construção da API.
  - `uvicorn`: Servidor ASGI para rodar a API.
  - `requests`: Para consumir a API REST Countries.
  - `pydantic`: Para validação de dados.
- **REST Countries API**: Fonte de dados sobre países.

## Pré-requisitos

- Python 3.8 ou superior instalado.
- Git para clonar o repositório.
- Ferramenta para testar APIs (ex.: Postman, curl ou navegador).

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/vincemendneck/Country_Catalog.git
   cd Country_Catalog


Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


Instale as dependências:
pip install fastapi uvicorn requests pydantic

Nota: O SQLite é nativo do Python (sqlite3), então não requer instalação adicional.

Execute a API:
python country_catalog.py

A API estará disponível em http://localhost:8000. Acesse http://localhost:8000/docs para a documentação interativa do FastAPI.


Configuração do Banco de Dados

O banco de dados SQLite é criado automaticamente como countries.db no diretório do projeto na primeira execução.
A tabela ratings é inicializada para armazenar avaliações com as colunas:
id: Identificador único (autoincrementado).
country_name: Nome do país (texto).
rating: Avaliação (1 para "curti", 0 para "nao_curti").



Não é necessário configurar um servidor de banco, pois o SQLite usa um arquivo local.
Endpoints
1. GET /paises/top10

Descrição: Retorna os 10 países mais populosos.
Resposta (JSON):[
  {
    "nome": "India",
    "populacao": 1407563842,
    "continente": "Asia",
    "curtidas": 5,
    "nao_curtidas": 2
  },
  ...
]



2. GET /paises/buscar?nome=<nome>

Descrição: Busca um país pelo nome.
Exemplo: GET /paises/buscar?nome=brasil
Resposta (JSON):{
  "nome": "Brazil",
  "populacao": 214326223,
  "continente": "South America",
  "curtidas": 10,
  "nao_curtidas": 3
}


Erros:
404: País não encontrado.
500: Erro ao consultar a API.



3. POST /paises/avaliar

Descrição: Registra uma avaliação ("curti" ou "nao_curti") para um país.
Corpo da Requisição (JSON):{
  "nome": "Brasil",
  "avaliacao": "curti"
}


Resposta (JSON):{
  "pais": "Brazil",
  "status": "sucesso",
  "quantidade_votos": 13
}


Erros:
400: Avaliação inválida (deve ser "curti" ou "nao_curti").
404: País não encontrado.
500: Erro interno.



Testando a API

Usando Postman:

Configure requisições GET e POST conforme os exemplos acima.
Para o POST, envie o corpo JSON no formato especificado.


Usando curl:

Listar top 10:curl http://localhost:8000/paises/top10


Buscar país:curl http://localhost:8000/paises/buscar?nome=brasil


Avaliar país:curl -X POST http://localhost:8000/paises/avaliar -H "Content-Type: application/json" -d '{"nome":"Brasil","avaliacao":"curti"}'




Usando o navegador:

Acesse http://localhost:8000/paises/top10 ou http://localhost:8000/paises/buscar?nome=brasil para os endpoints GET.
Use /docs para testar interativamente.



Estrutura do Projeto
Country_Catalog/
├── country_catalog.py  # Código principal da API
├── countries.db       # Banco de dados SQLite (criado automaticamente)

Desafios e Soluções

Consumo da API REST Countries:

Desafio: A API não suporta ordenação por população. A ordenação foi feita localmente com sorted em Python.
Solução: Filtramos apenas os campos necessários (name,population,continents) para reduzir o tamanho da resposta.


Persistência de Avaliações:

Desafio: Contar curtidas e não curtidas de forma eficiente.
Solução: Usamos consultas SQL com SUM(CASE ...) para calcular dinamicamente as avaliações por país.


Tratamento de Erros:

Desafio: Garantir respostas consistentes para falhas (ex.: país não encontrado).
Solução: Implementamos tratamento de erros HTTP (404, 400, 500) com mensagens claras.


Uso do SQLite:

Desafio: Garantir compatibilidade com o FastAPI em ambiente assíncrono.
Solução: Configuramos check_same_thread=False na conexão SQLite e fechamos conexões adequadamente.

