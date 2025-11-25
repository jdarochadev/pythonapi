## API de Catálogo de Produtos

Esta aplicação é uma API construída com FastAPI para gerenciar um catálogo de produtos. O sistema implementa autenticação baseada em JWT, operações CRUD completas, estrutura modular e persistência utilizando SQLite com SQLAlchemy.
É um projeto voltado para estudo, com foco em organização, boas práticas e arquitetura limpa.

Funcionalidades Principais

Registro e autenticação de usuários com tokens JWT

Login e renovação de sessão via refresh token

Cadastro, listagem, atualização e exclusão de produtos

Paginação de resultados

Validação de dados com Pydantic

Banco de dados gerenciado por SQLAlchemy

Migrações de schema via Alembic

Testes automatizados com pytest

Tecnologias Utilizadas

FastAPI

Python 3.10+

SQLite

SQLAlchemy

Alembic

Pydantic

Python-Jose para JWT

Passlib (bcrypt) para hashing de senhas

Pytest + HTTPX para testes

Estrutura Geral

A aplicação segue uma arquitetura modular organizada em camadas.

Autenticação

POST /auth/register — Criar usuário

POST /auth/login — Realizar login

POST /auth/refresh — Renovar token

Produtos (JWT obrigatório)

GET /products/ — Listar produtos

GET /products/{id} — Obter produto

POST /products/ — Criar produto

PUT /products/{id} — Atualizar produto

PATCH /products/{id} — Atualização parcial

DELETE /products/{id} — Excluir produto

Objetivo

O projeto foi desenvolvido como material de estudo para prática de:

Arquitetura limpa em APIs REST

Uso de FastAPI em contextos reais

ORM com SQLAlchemy

Autenticação moderna com JWT

Boas práticas de organização de código

Testes automatizados