import sqlite3

# ---------- CONEXÃO ----------
def conectar():
    return sqlite3.connect("banco_academico.db")

# ---------- CRIAÇÃO DE TABELAS (caso não existam) ----------
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            nome TEXT,
            email TEXT UNIQUE,
            matricula TEXT PRIMARY KEY,
            senha TEXT,
            tipo_usuario INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            matricula TEXT,
            avaliacao TEXT,
            nota REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presencas (
            matricula TEXT,
            data TEXT,
            presenca INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# ---------- USUÁRIOS ----------
def adicionar_usuario(nome, email, matricula, senha, tipo_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios VALUES (?, ?, ?, ?, ?)",
        (nome, email, matricula, senha, tipo_usuario)
    )
    conn.commit()
    conn.close()

def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

def verificar_usuario(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE email=?", (email,))
    tipo = cursor.fetchone()
    conn.close()
    if tipo:
        return tipo[0]
    return None

# ---------- NOTAS ----------
def cadastrar_nota(avaliacao, matricula, nota):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas VALUES (?, ?, ?)", (matricula, avaliacao, nota))
    conn.commit()
    conn.close()

def consultar_notas(matricula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT avaliacao, nota FROM notas WHERE matricula=?", (matricula,))
    dados = cursor.fetchall()
    conn.close()
    return dados

# ---------- PRESENÇA ----------
def atualizar_presenca(matricula, data, presenca):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presencas VALUES (?, ?, ?)", (matricula, data, presenca))
    conn.commit()
    conn.close()

def consultar_presenca(matricula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT data, presenca FROM presencas WHERE matricula=?", (matricula,))
    dados = cursor.fetchall()
    conn.close()
    return dados