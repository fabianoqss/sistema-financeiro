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
