# Country Catalog API

Este projeto é uma API REST desenvolvida em Python com FastAPI que consome a API pública [REST Countries](https://restcountries.com) para listar, buscar e avaliar países. As avaliações são persistidas em um banco de dados, com duas implementações: uma usando SQLite (`country_catalog.py`) e outra usando MySQL (`country_catalog_mysql.py`). Os resultados incluem nome, população, continente e contagem de curtidas/não curtidas.

## Funcionalidades

- **Listar os 10 países mais populosos**: Endpoint `GET /paises/top10` retorna os 10 países com maior população, incluindo nome, população, continente e avaliações.
- **Buscar um país pelo nome**: Endpoint `GET /paises/buscar?nome=<nome>` retorna os dados de um país específico no mesmo formato.
- **Avaliar um país**: Endpoint `POST /paises/avaliar` registra uma avaliação ("curti" ou "nao_curti"), salvando no banco e retornando o status e total de votos.

## Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal.
- **FastAPI**: Framework para criação da API.
- **SQLite** (em `country_catalog.py`): Banco de dados leve, sem necessidade de servidor.
- **MySQL** (em `country_catalog_mysql.py`): Banco de dados relacional.
- **Bibliotecas**:
  - `fastapi`: Para construção da API.
  - `uvicorn`: Servidor ASGI.
  - `requests`: Para consumir a API REST Countries.
  - `pydantic`: Para validação de dados.
  - `mysql-connector-python` (para MySQL): Conexão com MySQL.
- **REST Countries API**: Fonte de dados sobre países.

## Pré-requisitos

- Python 3.8 ou superior instalado.
- Git para clonar o repositório.
- Para a versão MySQL: MySQL Server instalado e rodando.
- Ferramenta para testar APIs (ex.: navegador em `/docs`).

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/vincemendneck/Country_Catalog.git
   cd Country_Catalog


Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


Instale as dependências:

Para a versão SQLite:pip install fastapi uvicorn requests pydantic


Para a versão MySQL (adicione a biblioteca do MySQL):pip install fastapi uvicorn requests pydantic mysql-connector-python




Configuração do Banco de Dados:

SQLite (country_catalog.py):
Não requer configuração. O banco countries.db é criado automaticamente no diretório do projeto.


MySQL (country_catalog_mysql.py):
Instale o MySQL Server (ex.: sudo apt install mysql-server no Ubuntu, ou MySQL Installer no Windows).
Inicie o servidor: sudo service mysql start (Linux) ou mysql.server start (macOS).
Acesse o MySQL: mysql -u root -p.
Crie o banco: CREATE DATABASE countries_db;.
Opcional: Crie um usuário: CREATE USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin'; GRANT ALL PRIVILEGES ON countries_db.* TO 'admin'@'localhost';.
Edite country_catalog_mysql.py e ajuste DB_CONFIG com suas credenciais (host, database, user, password).




Execute a API:

Para SQLite:python country_catalog.py


Para MySQL:python country_catalog_mysql.py



A API estará disponível em http://localhost:8000. Acesse http://localhost:8000/docs para a documentação interativa do FastAPI.


Configuração do Banco de Dados

SQLite:

O banco countries.db é criado automaticamente na primeira execução.
Tabela ratings: id (autoincrementado), country_name (texto), rating (1 para "curti", 0 para "nao_curti").


MySQL:

O banco countries_db deve ser criado manualmente (veja passo 4).
Tabela ratings (criada automaticamente): id (INT AUTO_INCREMENT), country_name (VARCHAR(255)), rating (BOOLEAN).



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
Use a interface /docs em http://localhost:8000/docs:

Clique em GET /paises/top10, "Try it out", e "Execute" para listar países.
Para GET /paises/buscar, insira nome=brasil e execute.
Para POST /paises/avaliar, insira JSON como {"nome": "Brasil", "avaliacao": "curti"} e execute.

Estrutura do Projeto
Country_Catalog/
├── country_catalog.py      # Versão com SQLite
├── country_catalog_mysql.py # Versão com MySQL
├── countries.db           # Banco SQLite (criado automaticamente)
├── README.md              # Este arquivo

Nota: O banco MySQL (countries_db) é gerenciado pelo servidor MySQL, não como um arquivo local.

Desafios e Soluções

Consumo da API REST Countries:

Desafio: A API não suporta ordenação por população.

Solução: Ordenação local com sorted em Python, filtrando campos (name,population,continents).


Persistência de Avaliações:

Desafio: Contar curtidas e não curtidas eficientemente.

Solução: Consultas SQL com SUM(CASE ...) para cálculos dinâmicos.


Tratamento de Erros:

Desafio: Respostas consistentes para falhas.

Solução: Tratamento de erros HTTP (404, 400, 500) com mensagens claras.


Uso de Bancos:

Desafio: Suportar SQLite e MySQL com compatibilidade no FastAPI.

Solução: SQLite usa arquivo local; MySQL usa mysql-connector-python com auth_plugin para compatibilidade.





