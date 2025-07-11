# EPI Manager - Sistema de Cadastro de EPIs

Aplicação web para cadastro e gerenciamento de Equipamentos de Proteção Individual (EPIs), construída com Flask, SQLAlchemy, Flask-Login e Flask-WTF. Permite cadastro de usuários, autenticação, níveis de permissão e controle dos EPIs no estoque.

---

## Funcionalidades

- Cadastro e autenticação de usuários com diferentes níveis de permissão (ex: admin)
- Cadastro de EPIs com informações detalhadas
- Controle de estoque com localização física dos EPIs
- Segurança com CSRF e hash de senhas
- Suporte a banco de dados SQLite para desenvolvimento local
- Suporte a banco de dados PostgreSQL para produção (ex: Render.com)

---

## Tecnologias Utilizadas

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (local)
- PostgreSQL (produção)
- Render (para deploy)

---

## Estrutura do Projeto

```
epi_app/
│
├── app/
│   ├── __init__.py       # Cria o app e configura banco e login
│   ├── models.py         # Modelos ORM (User, EPI, etc)
│   ├── routes.py         # Rotas da aplicação (login, cadastro, etc)
│   └── templates/        # HTML/Jinja templates
│
├── instance/
│   └── database.db       # Arquivo do banco SQLite local (gerado automaticamente)
│
├── init_db.py            # Script para criar banco e usuário admin localmente
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente para desenvolvimento local
└── README.md             # Este arquivo
```

---

## Instalação e Uso Local

### Requisitos

- Python 3.10 ou superior
- Git (para clonar o repositório)
- Ambiente virtual (recomendado)

### Passos para rodar localmente

1. Clone o projeto:

```bash
git clone https://github.com/niltongms/EPI_app.git
cd EPI_app
```

2. Crie e ative um ambiente virtual:

No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows (cmd):
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie a pasta `instance` e inicialize o banco SQLite com o usuário admin padrão:

```bash
python init_db.py
```

5. Execute o servidor Flask localmente:

```bash
flask run
```

6. Acesse no navegador: `http://127.0.0.1:5000`

---

## Deploy no Render (Produção)

Este projeto está configurado para usar o PostgreSQL do Render quando em produção.

### Passos básicos para deploy no Render:

1. Crie um banco PostgreSQL no Render.
2. Copie a connection string gerada pelo Render.
3. Configure no painel Render, nas variáveis de ambiente (`Environment`), a variável `DATABASE_URL` com essa connection string.
4. Configure também a variável `SECRET_KEY` para uma chave segura.
5. Crie um serviço Web no Render apontando para seu repositório GitHub.
6. O Render detecta o projeto, instala as dependências e executa automaticamente.
7. A aplicação estará disponível na URL que o Render fornecer.

---

## Variáveis de Ambiente

- `DATABASE_URL` : string de conexão com o banco (PostgreSQL para produção, omitido para usar SQLite local)
- `SECRET_KEY` : chave secreta do Flask para segurança

---

## Observações

- O banco SQLite só funciona localmente para desenvolvimento.
- No deploy Render, o banco PostgreSQL deve ser usado via `DATABASE_URL`.
- As migrações do banco podem ser feitas usando `flask db` (se usar Flask-Migrate).
- Para questões de segurança, nunca publique sua `SECRET_KEY` nem dados sensíveis no repositório.

---

## Contato

Para dúvidas ou sugestões, entre em contato:  
**Elenilton Gomes** – niltonsgms@gmail.com
