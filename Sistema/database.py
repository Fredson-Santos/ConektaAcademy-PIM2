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
        curso TEXT,
        materia TEXT
    )
    """)
    
    # Adicionar coluna materia caso a tabela já exista sem ela
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN materia TEXT")
    except sqlite3.OperationalError:
        # Coluna já existe, não precisa fazer nada
        pass
    
    # Adicionar coluna turma_id caso a tabela já exista sem ela
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN turma_id TEXT")
    except sqlite3.OperationalError:
        # Coluna já existe, não precisa fazer nada
        pass

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

    # Tabela de turmas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ano INTEGER,
        professor_id INTEGER,
        curso_id INTEGER,
        FOREIGN KEY (professor_id) REFERENCES usuarios(id),
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
    );
    ''')
    
    # Adicionar coluna curso_id caso a tabela já exista sem ela
    try:
        cursor.execute("ALTER TABLE turmas ADD COLUMN curso_id INTEGER")
    except sqlite3.OperationalError:
        # Coluna já existe, não precisa fazer nada
        pass

    # 🔹 Tabela de cursos (corrigida)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        inicio TEXT,
        duracao INTEGER -- em semestres
    );
    ''')

    # Tabela de disciplinas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        professor_id INTEGER,
        carga_horaria INTEGER,
        curso_id INTEGER,
        turma_id TEXT,
        FOREIGN KEY (curso_id) REFERENCES cursos(id),
        FOREIGN KEY (professor_id) REFERENCES usuarios(id)
    );
    ''')
    
    # Adicionar coluna turma_id caso a tabela já exista sem ela
    try:
        cursor.execute("ALTER TABLE disciplinas ADD COLUMN turma_id TEXT")
    except sqlite3.OperationalError:
        # Coluna já existe, não precisa fazer nada
        pass

    # Tabela de avaliações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_matricula_fk INTEGER,
        id_disciplina_fk TEXT,
        avaliacao TEXT,
        nota REAL,
        data_lancamento TEXT,
        FOREIGN KEY (id_matricula_fk) REFERENCES usuarios(matricula)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (id_disciplina_fk) REFERENCES disciplinas(nome)
            ON DELETE CASCADE ON UPDATE CASCADE
    );
    """)
    
    # Adicionar colunas nota e data_lancamento caso a tabela já exista sem elas
    try:
        cursor.execute("ALTER TABLE avaliacoes ADD COLUMN nota REAL")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE avaliacoes ADD COLUMN data_lancamento TEXT")
    except sqlite3.OperationalError:
        pass

    # Tabela de notas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT,
        disciplina_id INTEGER,
        np1 REAL CHECK (np1 >= 0 AND np1 <= 10),
        np2 REAL CHECK (np2 >= 0 AND np2 <= 10),
        pim REAL CHECK (pim >= 0 AND pim <= 10),
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
    );
    """)

    conn.commit()
    conn.close()

# Executar a criação das tabelas
if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados e tabelas criados com sucesso!")
