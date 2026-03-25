from database.connection import get_connection
from models.transacao import Transacao


def adicionar_transacao(descricao: str, valor: float, tipo: str,
                        data: str, categoria_id: int, usuario_id: int) -> Transacao | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT INTO transacoes (descricao, valor, tipo, data, categoria_id, usuario_id)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (descricao.strip(), valor, tipo, data, categoria_id, usuario_id)
        )
        conn.commit()
        return Transacao(id=cursor.lastrowid, descricao=descricao, valor=valor,
                         tipo=tipo, data=data, categoria_id=categoria_id, usuario_id=usuario_id)
    except Exception:
        return None
    finally:
        conn.close()


def listar_transacoes(usuario_id: int, mes: int = None, ano: int = None,
                      tipo: str = None, categoria_id: int = None) -> list[Transacao]:
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM transacoes WHERE usuario_id = ?"
    params = [usuario_id]

    if mes and ano:
        query += " AND strftime('%m', data) = ? AND strftime('%Y', data) = ?"
        params += [f"{mes:02d}", str(ano)]
    elif ano:
        query += " AND strftime('%Y', data) = ?"
        params.append(str(ano))

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)

    if categoria_id:
        query += " AND categoria_id = ?"
        params.append(categoria_id)

    query += " ORDER BY data DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        Transacao(id=r['id'], descricao=r['descricao'], valor=r['valor'],
                  tipo=r['tipo'], data=r['data'], categoria_id=r['categoria_id'],
                  usuario_id=r['usuario_id'], criado_em=r['criado_em'])
        for r in rows
    ]


def excluir_transacao(transacao_id: int, usuario_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM transacoes WHERE id = ? AND usuario_id = ?",
        (transacao_id, usuario_id)
    )
    afetadas = cursor.rowcount
    conn.commit()
    conn.close()
    return afetadas > 0


def resumo_por_categoria(usuario_id: int, mes: int = None, ano: int = None) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT c.nome as categoria, t.tipo, SUM(t.valor) as total, COUNT(*) as qtd
        FROM transacoes t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        WHERE t.usuario_id = ?
    '''
    params = [usuario_id]

    if mes and ano:
        query += " AND strftime('%m', t.data) = ? AND strftime('%Y', t.data) = ?"
        params += [f"{mes:02d}", str(ano)]

    query += " GROUP BY t.categoria_id, t.tipo ORDER BY total DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def saldo_total(usuario_id: int, mes: int = None, ano: int = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT tipo, SUM(valor) as total FROM transacoes WHERE usuario_id = ?"
    params = [usuario_id]

    if mes and ano:
        query += " AND strftime('%m', data) = ? AND strftime('%Y', data) = ?"
        params += [f"{mes:02d}", str(ano)]

    query += " GROUP BY tipo"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    resultado = {'receita': 0.0, 'despesa': 0.0}
    for r in rows:
        resultado[r['tipo']] = r['total']
    resultado['saldo'] = resultado['receita'] - resultado['despesa']
    return resultado
