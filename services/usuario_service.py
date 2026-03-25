import hashlib
from database.connection import get_connection
from models.usuario import Usuario

def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()



def cadastrar_usuario(nome : str, email: str, senha : str) -> Usuario | None :
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome.strip(), email.strip().lower(), _hash_senha(senha))
        )
        conn.commit()
        novo_id = cursor.lastrowid
        print(f"Usuário cadastrado com sucesso! O ID gerado foi: {novo_id}")
        return Usuario(id=novo_id, nome=nome, email=email, senha='')
    except Exception:
        return None
    finally:
        conn.close()



def login(email: str, senha: str) -> Usuario | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
        (email.strip().lower(), _hash_senha(senha))
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return Usuario(id=row['id'], nome=row['nome'], email=row['email'],
                       senha='', criado_em=row['criado_em'])
    return None


def email_ja_cadastrado(email: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email.strip().lower(),))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe
