from services import transacao_service, categoria_service, usuario_service
from views import relatorios
from utils.validators import validar_email, validar_valor, validar_data, validar_tipo
from datetime import datetime


# ─────────────────────────── HELPERS ────────────────────────────

def _linha(char='-', tamanho=55):
    print(char * tamanho)


def _cabecalho(titulo: str):
    _linha('=')
    print(titulo.center(55))
    _linha('=')


def _input(prompt: str) -> str:
    return input(f"  {prompt}").strip()


def _pausar():
    input("\n  Pressione ENTER para continuar...")


def _mes_ano_atual():
    agora = datetime.now()
    return agora.month, agora.year


def _pedir_periodo() -> tuple[int, int] | tuple[None, None]:
    entrada = _input("Período (MM/AAAA) ou ENTER para mês atual: ")
    if not entrada:
        return _mes_ano_atual()
    try:
        partes = entrada.split('/')
        return int(partes[0]), int(partes[1])
    except Exception:
        print("  Formato inválido. Usando mês atual.")
        return _mes_ano_atual()


# ─────────────────────────── AUTENTICAÇÃO ────────────────────────────

def tela_inicial() -> object | None:
    while True:
        _cabecalho("SISTEMA DE CONTROLE FINANCEIRO")
        print("  [1] Login")
        print("  [2] Criar conta")
        print("  [0] Sair")
        _linha()
        opcao = _input("Opção: ")

        if opcao == '1':
            usuario = tela_login()
            if usuario:
                return usuario
        elif opcao == '2':
            tela_cadastro()
        elif opcao == '0':
            print("\n  Até logo!\n")
            return None
        else:
            print("  Opção inválida.")


def tela_login():
    _cabecalho("LOGIN")
    email = _input("Email: ")
    senha = _input("Senha: ")

    usuario = usuario_service.login(email, senha)
    if usuario:
        print(f"\n  Bem-vindo(a), {usuario.nome}!")
        _pausar()
        return usuario
    else:
        print("\n  Email ou senha incorretos.")
        _pausar()
        return None


def tela_cadastro():
    _cabecalho("CRIAR CONTA")

    nome = _input("Nome completo: ")
    if not nome:
        print("  Nome obrigatório.")
        return

    email = _input("Email: ")
    if not validar_email(email):
        print("  Email inválido.")
        return

    if usuario_service.email_ja_cadastrado(email):
        print("  Este email já está cadastrado.")
        return

    senha = _input("Senha: ")
    if len(senha) < 4:
        print("  Senha deve ter pelo menos 4 caracteres.")
        return

    usuario = usuario_service.cadastrar_usuario(nome, email, senha)
    if usuario:
        categoria_service.criar_categorias_padrao(usuario.id)
        print(f"\n  Conta criada com sucesso! Categorias padrão adicionadas.")
    else:
        print("  Erro ao criar conta.")
    _pausar()


# ─────────────────────────── MENU PRINCIPAL ────────────────────────────

def menu_principal(usuario):
    while True:
        _cabecalho(f"MENU PRINCIPAL — {usuario.nome}")
        print("  [1] Lançar Receita")
        print("  [2] Lançar Despesa")
        print("  [3] Extrato")
        print("  [4] Relatórios")
        print("  [5] Categorias")
        print("  [6] Excluir transação")
        print("  [0] Sair")
        _linha()
        opcao = _input("Opção: ")

        if opcao == '1':
            tela_lancamento(usuario, tipo_fixo='receita')
        elif opcao == '2':
            tela_lancamento(usuario, tipo_fixo='despesa')
        elif opcao == '3':
            tela_extrato(usuario)
        elif opcao == '4':
            menu_relatorios(usuario)
        elif opcao == '5':
            menu_categorias(usuario)
        elif opcao == '6':
            tela_excluir_transacao(usuario)
        elif opcao == '0':
            break
        else:
            print("  Opção inválida.")


# ─────────────────────────── LANÇAMENTOS ────────────────────────────

def tela_lancamento(usuario, tipo_fixo: str = None):
    tipo = tipo_fixo
    if not tipo:
        tipo_str = _input("Tipo (receita/despesa): ")
        tipo = validar_tipo(tipo_str)
        if not tipo:
            print("  Tipo inválido.")
            _pausar()
            return

    _cabecalho(f"LANÇAR {tipo.upper()}")

    descricao = _input("Descrição: ")
    if not descricao:
        print("  Descrição obrigatória.")
        _pausar()
        return

    valor_str = _input("Valor (R$): ")
    valor = validar_valor(valor_str)
    if valor is None:
        print("  Valor inválido. Use números positivos.")
        _pausar()
        return

    data_str = _input("Data (DD/MM/AAAA) ou ENTER para hoje: ")
    if not data_str:
        data = datetime.now().strftime('%Y-%m-%d')
    else:
        data = validar_data(data_str)
        if not data:
            print("  Data inválida.")
            _pausar()
            return

    categorias = categoria_service.listar_categorias(usuario.id, tipo)
    categoria_id = None
    if categorias:
        print(f"\n  Categorias disponíveis:")
        for i, c in enumerate(categorias, 1):
            print(f"    [{i}] {c.nome}")
        print("    [0] Sem categoria")
        escolha = _input("Escolha a categoria: ")
        try:
            idx = int(escolha)
            if 1 <= idx <= len(categorias):
                categoria_id = categorias[idx - 1].id
        except ValueError:
            pass

    transacao = transacao_service.adicionar_transacao(
        descricao, valor, tipo, data, categoria_id, usuario.id
    )
    if transacao:
        sinal = "+" if tipo == 'receita' else "-"
        print(f"\n  Lançamento registrado: {sinal}R$ {valor:.2f} — {descricao}")
    else:
        print("\n  Erro ao registrar lançamento.")
    _pausar()


# ─────────────────────────── EXTRATO ────────────────────────────

def tela_extrato(usuario):
    _cabecalho("EXTRATO")
    print("  [1] Mês atual")
    print("  [2] Período específico")
    print("  [3] Todos os lançamentos")
    opcao = _input("Opção: ")

    if opcao == '1':
        mes, ano = _mes_ano_atual()
        relatorios.exibir_saldo(usuario.id, mes, ano)
        relatorios.exibir_extrato(usuario.id, mes, ano)
    elif opcao == '2':
        mes, ano = _pedir_periodo()
        relatorios.exibir_saldo(usuario.id, mes, ano)
        relatorios.exibir_extrato(usuario.id, mes, ano)
    elif opcao == '3':
        relatorios.exibir_saldo(usuario.id)
        relatorios.exibir_extrato(usuario.id)
    _pausar()


# ─────────────────────────── RELATÓRIOS ────────────────────────────

def menu_relatorios(usuario):
    while True:
        _cabecalho("RELATÓRIOS")
        print("  [1] Resumo por categoria (mês atual)")
        print("  [2] Resumo por categoria (período)")
        print("  [3] Gráfico de despesas")
        print("  [0] Voltar")
        _linha()
        opcao = _input("Opção: ")

        if opcao == '1':
            mes, ano = _mes_ano_atual()
            relatorios.exibir_saldo(usuario.id, mes, ano)
            relatorios.exibir_por_categoria(usuario.id, mes, ano)
            _pausar()
        elif opcao == '2':
            mes, ano = _pedir_periodo()
            relatorios.exibir_saldo(usuario.id, mes, ano)
            relatorios.exibir_por_categoria(usuario.id, mes, ano)
            _pausar()
        elif opcao == '3':
            mes, ano = _pedir_periodo()
            relatorios.exibir_grafico_despesas(usuario.id, mes, ano)
            _pausar()
        elif opcao == '0':
            break


# ─────────────────────────── CATEGORIAS ────────────────────────────

def menu_categorias(usuario):
    while True:
        _cabecalho("CATEGORIAS")
        print("  [1] Listar categorias")
        print("  [2] Nova categoria")
        print("  [3] Excluir categoria")
        print("  [0] Voltar")
        _linha()
        opcao = _input("Opção: ")

        if opcao == '1':
            cats = categoria_service.listar_categorias(usuario.id)
            _cabecalho("MINHAS CATEGORIAS")
            if not cats:
                print("  Nenhuma categoria cadastrada.")
            for c in cats:
                print(f"  [{c.id}] {c.nome:<25} ({c.tipo})")
            _linha()
            _pausar()

        elif opcao == '2':
            _cabecalho("NOVA CATEGORIA")
            nome = _input("Nome: ")
            if not nome:
                print("  Nome obrigatório.")
                _pausar()
                continue
            tipo_str = _input("Tipo (receita/despesa): ")
            tipo = validar_tipo(tipo_str)
            if not tipo:
                print("  Tipo inválido.")
                _pausar()
                continue
            cat = categoria_service.criar_categoria(nome, tipo, usuario.id)
            if cat:
                print(f"  Categoria '{nome}' criada.")
            else:
                print("  Erro ao criar categoria.")
            _pausar()

        elif opcao == '3':
            cats = categoria_service.listar_categorias(usuario.id)
            if not cats:
                print("  Nenhuma categoria para excluir.")
                _pausar()
                continue
            for c in cats:
                print(f"  [{c.id}] {c.nome} ({c.tipo})")
            id_str = _input("ID da categoria para excluir: ")
            try:
                cat_id = int(id_str)
                ok = categoria_service.excluir_categoria(cat_id, usuario.id)
                if ok:
                    print("  Categoria excluída.")
                else:
                    print("  Não é possível excluir: categoria possui transações vinculadas.")
            except ValueError:
                print("  ID inválido.")
            _pausar()

        elif opcao == '0':
            break


# ─────────────────────────── EXCLUIR TRANSAÇÃO ────────────────────────────

def tela_excluir_transacao(usuario):
    _cabecalho("EXCLUIR TRANSAÇÃO")
    mes, ano = _mes_ano_atual()
    transacoes = transacao_service.listar_transacoes(usuario.id, mes, ano)

    if not transacoes:
        print("  Nenhuma transação encontrada no mês atual.")
        _pausar()
        return

    for t in transacoes:
        sinal = "+" if t.tipo == 'receita' else "-"
        print(f"  [{t.id}] {t.data}  {t.descricao[:25]:<25}  {sinal}R$ {t.valor:.2f}")

    _linha()
    id_str = _input("ID da transação para excluir (0 para cancelar): ")
    try:
        tid = int(id_str)
        if tid == 0:
            return
        ok = transacao_service.excluir_transacao(tid, usuario.id)
        print("  Transação excluída." if ok else "  Transação não encontrada.")
    except ValueError:
        print("  ID inválido.")
    _pausar()
