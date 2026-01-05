# AgilStore em Django 🐍

Este repositório contém um projeto **Django** desenvolvido **exclusivamente para fins de portfólio**.  
Não há qualquer intenção de que este sistema seja utilizado como um e-commerce real.  
O objetivo é **demonstrar funcionalidades, organização e boas práticas na estrutura de projetos Django**.

---

## 🎯 Objetivo

- Mostrar domínio da estrutura de um projeto Django.
- Implementar múltiplos *apps* para simular funcionalidades comuns em sistemas web.
- Servir como referência de organização de código para estudos e portfólio.

---

## 🗂 Estrutura do Projeto

O projeto está dividido em diferentes *apps*, cada um responsável por uma parte da aplicação:

- **accounts/** → gerenciamento de autenticação e contas de usuários.
- **users/** → extensão do modelo de usuários, perfis customizados.
- **inventory/** → controle de estoque e produtos.
- **cart/** → carrinho de compras (adicionar/remover itens, calcular total).
- **agilstore/** → núcleo da aplicação, integrando os demais módulos.

Arquivos principais:
- `manage.py` → script padrão para comandos Django.
- `db.sqlite3` → banco de dados SQLite para testes.

---

## 🚀 Funcionalidades Demonstradas

- Estrutura modular com múltiplos *apps*.
- Modelos (`models.py`) representando entidades como usuários, produtos e carrinho.
- Views e URLs organizadas para cada app.
- Integração entre apps (ex.: carrinho conectado ao estoque e usuários).
- Uso de banco de dados SQLite para persistência simples.

---

## ⚠️ Aviso Importante

Este projeto **não é um sistema pronto para uso em produção**.  
Ele foi criado apenas para **mostrar conhecimento técnico** e **organização de código** em Django.  
Não há implementação de segurança, escalabilidade ou integração com meios de pagamento.

---

## 📚 Tecnologias Utilizadas

- [Python](https://www.python.org/)  
- [Django](https://www.djangoproject.com/)  
- Banco de dados SQLite (apenas para testes)

---

## 🧑‍💻 Autor

Projeto desenvolvido por **Pedro Idiarte** como parte do portfólio.  
