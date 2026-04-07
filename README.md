# Sistema de Controle Financeiro Pessoal
Aplicação web desenvolvida em Python com Flask para controle de finanças pessoais, com suporte a múltiplos usuários, categorias personalizadas e extrato por período.
## Funcionalidades
- Cadastro e login de usuários (senha criptografada com SHA-256)
- Lançamento de receitas e despesas
- Categorias personalizáveis por usuário
- Filtros por período (mês/ano)
- Extrato com saldo
- Dashboard com resumo financeiro do mês
## Tecnologias
- Python 3.10+
- Flask
- SQLite (via módulo `sqlite3` nativo)
- Bootstrap 5
- Docker
## Estrutura do Projeto
```
sistema-financeiro/
├── app.py                   # Ponto de entrada (Flask)
├── requirements.txt         # Dependências do projeto
├── Dockerfile               # Configuração Docker
├── .dockerignore
├── database/
│   └── connection.py        # Conexão e criação do banco de dados
├── models/
│   ├── usuario.py           # Classe Usuario
│   ├── categoria.py         # Classe Categoria
│   └── transacao.py         # Classe Transacao
├── services/
│   ├── usuario_service.py   # Lógica de autenticação e cadastro
│   ├── categoria_service.py # CRUD de categorias
│   └── transacao_service.py # CRUD e consultas de transações
├── utils/
│   └── validators.py        # Validação de email, data e valor
└── templates/
    ├── base.html            # Template base (navbar, alertas)
    ├── login.html
    ├── cadastro.html
    ├── dashboard.html
    ├── extrato.html
    ├── lancamento.html
    └── categorias.html
```
## Como Executar

### Localmente

1. Certifique-se de ter Python 3.10 ou superior instalado.
2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o sistema:
   ```bash
   python app.py
   ```
5. Acesse no navegador: `http://localhost:5000`

### Com Docker

1. Certifique-se de ter o Docker instalado.
2. Build do container.
   ```bash
   docker-compose up --buid
   ```
4. Acesse no navegador: `http://localhost:5000`

## Como Usar
1. Na tela inicial, crie uma conta ou faça login.
2. Ao criar conta, categorias padrão são adicionadas automaticamente.
3. Use o menu para lançar receitas/despesas, visualizar o extrato e gerenciar categorias.
## Requisitos Atendidos
| Requisito | Como foi atendido |
|---|---|
| Linguagem principal: Python | Todo o projeto em Python |
| Estrutura modular | Separado em `models`, `services`, `utils` |
| Orientação a Objetos | Classes `Usuario`, `Categoria`, `Transacao` |
| Persistência de dados | Banco de dados SQLite |
| Interface | Aplicação web com Flask e Bootstrap 5 |
| Tratamento de erros | Try/except em todas as operações de banco |
| Validação de entrada | Módulo `validators.py` dedicado |
| Boas práticas (PEP8) | Nomes significativos, funções pequenas e coesas |
