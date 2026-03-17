# Sistema de Controle Financeiro Pessoal

Aplicação CLI desenvolvida em Python para controle de finanças pessoais, com suporte a múltiplos usuários, categorias personalizadas, relatórios e gráficos.

## Funcionalidades

- Cadastro e login de usuários (senha criptografada com SHA-256)
- Lançamento de receitas e despesas
- Categorias personalizáveis por usuário
- Filtros por período (mês/ano)
- Relatório de extrato com saldo
- Resumo de gastos por categoria
- Gráfico de pizza de despesas (requer matplotlib)

## Tecnologias

- Python 3.10+
- SQLite (via módulo `sqlite3` nativo)
- matplotlib (opcional, para gráficos)

## Estrutura do Projeto

```
sistema-financeiro/
├── main.py                  # Ponto de entrada
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
├── views/
│   ├── menu.py              # Interface CLI (menus e interação)
│   └── relatorios.py        # Exibição de relatórios e gráficos
└── utils/
    └── validators.py        # Validação de email, data, valor e tipo
```

## Como Executar

1. Certifique-se de ter Python 3.10 ou superior instalado.
2. (Opcional) Instale o matplotlib para habilitar gráficos:
   ```
   pip install matplotlib
   ```
3. Execute o sistema:
   ```
   python main.py
   ```

## Como Usar

1. Na tela inicial, crie uma conta ou faça login.
2. Ao criar conta, categorias padrão são adicionadas automaticamente.
3. Use o menu principal para lançar receitas/despesas, visualizar extratos e relatórios.

## Requisitos Atendidos

| Requisito | Como foi atendido |
|---|---|
| Linguagem principal: Python | Todo o projeto em Python |
| Estrutura modular | Separado em `models`, `services`, `views`, `utils` |
| Orientação a Objetos | Classes `Usuario`, `Categoria`, `Transacao` |
| Persistência de dados | Banco de dados SQLite |
| Interface | CLI estruturado com menus |
| Tratamento de erros | Try/except em todas as operações de banco |
| Validação de entrada | Módulo `validators.py` dedicado |
| Boas práticas (PEP8) | Nomes significativos, funções pequenas e coesas |
