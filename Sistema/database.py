import sqlite3


con = sqlite3.connect("sistema_academico.db", check_same_thread=False)
cur = con.cursor()

#Esse arquivo cria o banco de dados e cria as tabelas

def criar_tabelas():
    # Tabela usuarios
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            matricula TEXT UNIQUE,
            senha TEXT NOT NULL,
            tipo_usuario INTEGER NOT NULL
        )
    """)

    # Tabela turmas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_disciplina TEXT NOT NULL,
            semestre TEXT NOT NULL,
            id_professor_fk INTEGER NOT NULL,
            FOREIGN KEY (id_professor_fk) REFERENCES usuarios(id_usuario)
                ON DELETE CASCADE ON UPDATE CASCADE
        )
    """)

    # Tabela matriculas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS matriculas (
            id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno_fk INTEGER NOT NULL,
            id_turma_fk INTEGER NOT NULL,
            FOREIGN KEY (id_aluno_fk) REFERENCES usuarios(id_usuario)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (id_turma_fk) REFERENCES turmas(id_turma)
                ON DELETE CASCADE ON UPDATE CASCADE,
            UNIQUE(id_aluno_fk, id_turma_fk)
        )
    """)

    # Tabela avaliacoes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_matricula_fk INTEGER,
            np1 REAL CHECK (np1 >= 0 AND np1 <= 10),
            np2 REAL CHECK (np2 >= 0 AND np2 <= 10),
            exame REAL CHECK (exame >= 0 AND exame <= 10),
            data_lancamento TEXT NOT NULL,
            FOREIGN KEY (id_matricula_fk) REFERENCES matriculas(id_matricula)
                ON DELETE CASCADE ON UPDATE CASCADE
    )
""")


    
    print("Tabelas criadas com sucesso!")
    con.commit()


criar_tabelas()