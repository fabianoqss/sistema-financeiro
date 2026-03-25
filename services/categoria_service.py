from database.connection import get_connection
from models.categoria import Categoria


def criar_categoria(nome: str, tipo: str, usuario_id: int) -> Categoria | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO categorias (nome, tipo, usuario_id) VALUES (?, ?, ?)",
            (nome.strip(), tipo, usuario_id)
        )
        conn.commit()
        return Categoria(id=cursor.lastrowid, nome=nome, tipo=tipo, usuario_id=usuario_id)
    except Exception:
        return None
    finally:
        conn.close()


def listar_categorias(usuario_id: int, tipo: str = None) -> list[Categoria]:
    conn = get_connection()
    cursor = conn.cursor()
    if tipo:
        cursor.execute(
            "SELECT * FROM categorias WHERE usuario_id = ? AND tipo = ? ORDER BY nome",
            (usuario_id, tipo)
        )
    else:
        cursor.execute(
            "SELECT * FROM categorias WHERE usuario_id = ? ORDER BY tipo, nome",
            (usuario_id,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [Categoria(id=r['id'], nome=r['nome'], tipo=r['tipo'], usuario_id=r['usuario_id']) for r in rows]


def excluir_categoria(categoria_id: int, usuario_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as total FROM transacoes WHERE categoria_id = ? AND usuario_id = ?",
        (categoria_id, usuario_id)
    )
    if cursor.fetchone()['total'] > 0:
        conn.close()
        return False
    cursor.execute(
        "DELETE FROM categorias WHERE id = ? AND usuario_id = ?",
        (categoria_id, usuario_id)
    )
    conn.commit()
    conn.close()
    return True


def criar_categorias_padrao(usuario_id: int):
    categorias_padrao = [
        ('Salário', 'receita'),
        ('Freelance', 'receita'),
        ('Investimentos', 'receita'),
        ('Alimentação', 'despesa'),
        ('Transporte', 'despesa'),
        ('Moradia', 'despesa'),
        ('Saúde', 'despesa'),
        ('Lazer', 'despesa'),
        ('Educação', 'despesa'),
        ('Outros', 'despesa'),
    ]
    for nome, tipo in categorias_padrao:
        criar_categoria(nome, tipo, usuario_id)
