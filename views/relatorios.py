from services.transacao_service import listar_transacoes, resumo_por_categoria, saldo_total
from datetime import datetime


def _linha(char='-', tamanho=55):
    print(char * tamanho)


def _cabecalho(titulo: str):
    _linha('=')
    print(titulo.center(55))
    _linha('=')


def exibir_saldo(usuario_id: int, mes: int = None, ano: int = None):
    periodo = f"{mes:02d}/{ano}" if mes and ano else "Geral"
    _cabecalho(f"RESUMO FINANCEIRO — {periodo}")

    dados = saldo_total(usuario_id, mes, ano)
    print(f"  {'Receitas:':<20} R$ {dados['receita']:>10.2f}")
    print(f"  {'Despesas:':<20} R$ {dados['despesa']:>10.2f}")
    _linha()
    saldo = dados['saldo']
    status = "POSITIVO" if saldo >= 0 else "NEGATIVO"
    print(f"  {'Saldo (' + status + '):':<20} R$ {saldo:>10.2f}")
    _linha()


def exibir_extrato(usuario_id: int, mes: int = None, ano: int = None):
    periodo = f"{mes:02d}/{ano}" if mes and ano else "Completo"
    _cabecalho(f"EXTRATO — {periodo}")

    transacoes = listar_transacoes(usuario_id, mes, ano)
    if not transacoes:
        print("  Nenhuma transação encontrada.")
        _linha()
        return

    for t in transacoes:
        sinal = "+" if t.tipo == "receita" else "-"
        data_fmt = datetime.strptime(t.data, '%Y-%m-%d').strftime('%d/%m/%Y')
        linha = f"  {data_fmt}  {t.descricao[:25]:<25}  {sinal}R$ {t.valor:>9.2f}"
        print(linha)

    _linha()
    print(f"  Total de transações: {len(transacoes)}")
    _linha()


def exibir_por_categoria(usuario_id: int, mes: int = None, ano: int = None):
    periodo = f"{mes:02d}/{ano}" if mes and ano else "Geral"
    _cabecalho(f"GASTOS POR CATEGORIA — {periodo}")

    dados = resumo_por_categoria(usuario_id, mes, ano)
    if not dados:
        print("  Nenhum dado encontrado.")
        _linha()
        return

    receitas = [d for d in dados if d['tipo'] == 'receita']
    despesas = [d for d in dados if d['tipo'] == 'despesa']

    if receitas:
        print("  RECEITAS:")
        for d in receitas:
            cat = d['categoria'] or 'Sem categoria'
            print(f"    {cat:<25} R$ {d['total']:>9.2f}  ({d['qtd']} lançamentos)")

    if despesas:
        print("  DESPESAS:")
        for d in despesas:
            cat = d['categoria'] or 'Sem categoria'
            print(f"    {cat:<25} R$ {d['total']:>9.2f}  ({d['qtd']} lançamentos)")

    _linha()


def exibir_grafico_despesas(usuario_id: int, mes: int = None, ano: int = None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n  [!] matplotlib não instalado. Execute: pip install matplotlib\n")
        return

    dados = resumo_por_categoria(usuario_id, mes, ano)
    despesas = [d for d in dados if d['tipo'] == 'despesa' and d['total'] > 0]

    if not despesas:
        print("\n  Nenhuma despesa para exibir no gráfico.\n")
        return

    labels = [d['categoria'] or 'Sem categoria' for d in despesas]
    valores = [d['total'] for d in despesas]

    periodo = f"{mes:02d}/{ano}" if mes and ano else "Geral"
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(f'Despesas por Categoria — {periodo}')
    plt.tight_layout()
    plt.show()
