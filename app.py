import streamlit as st
from auth import register_user, login_user
from database import get_db_connection
import sqlite3

# Inicializa banco de dados (se não existir)
from database import init_db
init_db()

# Sessão do usuário
if "user" not in st.session_state:
    st.session_state.user = None

# Funções para tarefas
def get_tasks(user_id):
    with get_db_connection() as conn:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? OR responsible_email = ? ORDER BY created_at DESC",
            (user_id, st.session_state.user["email"])
        ).fetchall()
        return [dict(task) for task in tasks]

def add_task(user_id, title, responsible_email):
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO tasks (user_id, title, responsible_email) VALUES (?, ?, ?)",
            (user_id, title, responsible_email if responsible_email else None)
        )
        conn.commit()

def update_task_status(task_id, completed):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (1 if completed else 0, task_id)
        )
        conn.commit()

def delete_task(task_id, user_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()

# Páginas
def pagina_login():
    st.title("🔐 Login / Cadastro")
    tab1, tab2 = st.tabs(["Login", "Cadastrar"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar"):
            user = login_user(email, senha)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Email ou senha incorretos")

    with tab2:
        email = st.text_input("Email", key="cad_email")
        senha = st.text_input("Senha", type="password", key="cad_senha")
        if st.button("Cadastrar"):
            user_id = register_user(email, senha)
            if user_id:
                st.success("Cadastro realizado! Faça login.")
            else:
                st.error("Email já existe")

def pagina_tarefas():
    st.title("📋 Gerenciador de Tarefas")
    st.sidebar.button("Sair", on_click=lambda: st.session_state.update(user=None))
    st.sidebar.write(f"Logado como: {st.session_state.user['email']}")

    user = st.session_state.user

    # Formulário nova tarefa
    with st.form("nova_tarefa"):
        titulo = st.text_input("Título da tarefa")
        responsavel = st.text_input("Responsável (email)", value="")
        if st.form_submit_button("Criar") and titulo:
            add_task(user["id"], titulo, responsavel)
            st.rerun()

    # Listar tarefas
    tarefas = get_tasks(user["id"])
    pendentes = [t for t in tarefas if not t["completed"]]
    concluidas = [t for t in tarefas if t["completed"]]

    st.subheader(f"📌 Pendentes ({len(pendentes)})")
    for t in pendentes:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
        with col1:
            st.write(t["title"])
        with col2:
            if t["responsible_email"]:
                st.write(f"👤 {t['responsible_email']}")
        with col3:
            if st.button("✅ Concluir", key=f"concluir_{t['id']}"):
                update_task_status(t["id"], True)
                st.rerun()
        with col4:
            if t["user_id"] == user["id"]:
                if st.button("🗑️", key=f"del_{t['id']}"):
                    delete_task(t["id"], user["id"])
                    st.rerun()

    st.subheader(f"✅ Concluídas ({len(concluidas)})")
    for t in concluidas:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
        with col1:
            st.write(f"~~{t['title']}~~")
        with col2:
            if t["responsible_email"]:
                st.write(f"👤 {t['responsible_email']}")
        with col3:
            if st.button("🔄 Reabrir", key=f"reabrir_{t['id']}"):
                update_task_status(t["id"], False)
                st.rerun()
        with col4:
            if t["user_id"] == user["id"]:
                if st.button("🗑️", key=f"del2_{t['id']}"):
                    delete_task(t["id"], user["id"])
                    st.rerun()

# Controle de fluxo
if st.session_state.user is None:
    pagina_login()
else:
    pagina_tarefas()


    