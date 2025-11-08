import sqlite3


# === CONEXÃO E CONFIGURAÇÃO INICIAL ===
def conectar():
    return sqlite3.connect("sistema_academico.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de usuários (professores e alunos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        matricula TEXT,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL,
        materia TEXT
    )
    """)

    # Tabelas de notas por matéria
    materias = ["matematica", "portugues", "ciencias", "geografia"]
    for materia in materias:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {materia} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT,
            np1 REAL,
            np2 REAL,
            pim REAL
        )
        """)

    # Tabela de presença
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS presencas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT,
        data TEXT,
        presente INTEGER
    )
    """)

    # Cronograma
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cronograma (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sala TEXT,
        data TEXT,
        dia_semana TEXT,
        conteudo TEXT
    )
    """)
    # Criar tabela "turmas"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ano INTEGER,
        professor_id INTEGER,
        FOREIGN KEY (professor_id) REFERENCES usuarios(id)
    );
    ''')

    # Criar tabela "disciplinas"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        professor_id INTEGER,
        carga_horaria INTEGER
    );
    ''')

    # Tabela avaliacoes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_matricula_fk INTEGER,
            id_disciplina_fk TEXT,
            avaliacao TEXT,
            nota REAL CHECK (nota >= 0 AND nota <= 10),
            data_lancamento TEXT,
            FOREIGN KEY (id_matricula_fk) REFERENCES usuarios(matricula)
                ON DELETE CASCADE ON UPDATE CASCADE
            FOREIGN KEY (id_disciplina_fk) REFERENCES disciplinas(nome)
                ON DELETE CASCADE ON UPDATE CASCADE
    )
""")


    conn.commit()
    conn.close()

