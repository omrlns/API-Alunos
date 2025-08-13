# 📚 PAQ-Project

API para cadastro e gerenciamento de alunos, desenvolvida como parte de um projeto de estudo para aprofundar conhecimentos em **Python**, **DuckDB** e **FastAPI**.

## 🚀 Tecnologias Utilizadas

- [Python 3] — Linguagem principal.
- [FastAPI] — Framework web para criação da API.
- [DuckDB] — Banco de dados analítico em formato colunar.
- [Uvicorn] — Servidor ASGI para rodar a API.

## 📌 Funcionalidades

- Cadastro de alunos.
- Listagem de alunos.
- Atualização (PUT/PATCH) de dados de alunos.
- Exclusão de registros.
- Conexão simples e rápida com DuckDB.

## 📥 Instalação

```bash
# Clone este repositório
git clone https://github.com/omrlns/PAQ-Project.git

# Instale as dependências
pip install -r requirements.txt

# Acesse a pasta do projeto
cd PAQ-Project 
````

▶️ Executando a API
Para iniciar o servidor local, utilize:

```bash
uvicorn app:app --reload
````

A API estará disponível em: http://127.0.0.1:8000

A documentação interativa do FastAPI pode ser acessada em:

Swagger UI → http://127.0.0.1:8000/docs

## 🧪 Endpoints

### Listar alunos
- **GET** `/alunos`  
  Retorna a lista de todos os alunos.

### Buscar aluno pelo ID
- **GET** `/alunos/{id}`  
  Retorna os dados de um aluno específico pelo seu ID.

### Cadastrar novo aluno
- **POST** `/alunos`  
  Adiciona um novo aluno à base de dados.

### Atualização completa
- **PUT** `/alunos/{id}`  
  Atualiza **todos os dados** de um aluno específico.

### Atualização parcial
- **PATCH** `/alunos/{id}`  
  Atualiza **parte dos dados** de um aluno específico.

### Remover aluno
- **DELETE** `/alunos/{id}`  
  Remove um aluno da base de dados pelo ID.

