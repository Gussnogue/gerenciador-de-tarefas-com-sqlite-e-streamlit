# 📋 Gerenciador de Tarefas com SQLite e Streamlit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-3-07405E?logo=sqlite&logoColor=white)](https://sqlite.org)
[![bcrypt](https://img.shields.io/badge/bcrypt-Password%20Hashing-green)](https://pypi.org/project/bcrypt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Um sistema simples e funcional de gerenciamento de tarefas com autenticação de usuários, desenvolvido em Python com Streamlit e banco de dados SQLite. Cada usuário pode criar suas próprias tarefas, atribuí-las a outros usuários (por email) e marcá-las como concluídas.

---

## ✨ Funcionalidades

- ✅ Cadastro e login de usuários (com senha criptografada usando bcrypt)
- ✅ Criação de tarefas com título e responsável (email)
- ✅ Listagem de tarefas pendentes e concluídas
- ✅ Marcar tarefas como concluídas ou reabri-las
- ✅ Exclusão de tarefas (apenas pelo criador)
- ✅ Tarefas atribuídas a outros usuários aparecem para eles também
- ✅ Interface simples e responsiva com Streamlit
- ✅ Tudo rodando localmente, sem dependência de serviços externos

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://python.org)
- [Streamlit](https://streamlit.io) – interface web
- [SQLite3](https://sqlite.org) – banco de dados local
- [bcrypt](https://pypi.org/project/bcrypt/) – criptografia de senhas

---

## 📁 Estrutura de Arquivos

├── app.py # Aplicação principal (interface e lógica)

├── auth.py # Funções de autenticação (hash, cadastro, login)

├── database.py # Conexão e inicialização do banco

├── requirements.txt # Dependências do projeto

└── README.md # Este arquivo

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.10 ou superior instalado
- Git (opcional, para clonar o repositório)

### Passo a Passo

#### 1. Clone o repositório (ou baixe os arquivos)

```bash
git clone https://github.com/seu-usuario/gerenciador-de-tarefas-com-sqlite-e-streamlit.git
cd tarefas-app
```

## 2. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 4. Crie o banco de dados SQLite

Execute os seguintes comandos no terminal para criar as tabelas manualmente (garantindo a estrutura correta):

```bash
sqlite3 tarefas.db
```

Dentro do shell do SQLite, segue comando:

```bash
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    responsible_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
.exit
```

## 5. Execute a aplicação

```bash
streamlit run app.py
```

## 6. Faça seu primeiro cadastro

Acesse a aba "Cadastrar" e crie um usuário com email e senha.
Depois, faça login na aba "Login" e comece a criar tarefas!


## 🧠 Como Usar

Criar tarefa: Preencha o título e, se quiser, o email do responsável (pode ser outro usuário cadastrado).

Ver tarefas: As tarefas são separadas em "Pendentes" e "Concluídas".

Concluir/Reabrir: Use os botões ✅ e 🔄 ao lado de cada tarefa.

Excluir: Apenas o criador da tarefa pode excluí‑la (botão 🗑️).

Sair: Clique no botão "Sair" na barra lateral.

## 📄 Licença
Este projeto está sob a licença MIT. Sinta‑se à vontade para usar, modificar e distribuir.
