import sqlite3
import bcrypt
from database import get_db_connection

def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt (trunca automaticamente para 72 bytes)."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(email: str, password: str):
    """Cadastra um novo usuário. Retorna o id se bem-sucedido, None se email já existe."""
    with get_db_connection() as conn:
        try:
            hashed = hash_password(password)
            cursor = conn.execute(
                "INSERT INTO users (email, senha_hash) VALUES (?, ?)",
                (email, hashed)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

def login_user(email: str, password: str):
    """Faz login. Retorna dicionário com dados do usuário se ok, None caso contrário."""
    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT id, email, senha_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        if user and verify_password(password, user["senha_hash"]):
            return {"id": user["id"], "email": user["email"]}
        return None

