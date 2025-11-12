import hashlib
import sys
import os

# Adicionar o diretório raiz ao path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sistema import database as db
from sistema.chat import iniciar_chat


# === FUNÇÕES DE SEGURANÇA - HASH DE SENHAS ===
def hash_senha(senha):
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def verificar_senha(senha, hash_armazenado):
    """Verifica se a senha corresponde ao hash armazenado"""
    return hash_senha(senha) == hash_armazenado


class Listar:
    def __init__(self, conexao):
        self.conn = conexao
        self.cursor = self.conn.cursor()

    def listar(self, tabela, colunas="*"):
        
        try:
            query = f"SELECT {colunas} FROM {tabela}"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            
            if resultados:
                return resultados
            else:
                print(f"\n⚠️ Nenhum registro encontrado em '{tabela}'.")
        except Exception as e:
            print(f"❌ Erro ao listar '{tabela}': {e}")





# === CADASTRO E LOGIN ===
def adicionar_usuario(nome, email, matricula, senha, tipo_usuario, materia=None):
    conn = db.conectar()
    cursor = conn.cursor()
    # Hash da senha antes de salvar
    senha_hash = hash_senha(senha)
    cursor.execute("""
    INSERT INTO usuarios (nome, email, matricula, senha, tipo_usuario, materia)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, email, matricula, senha_hash, tipo_usuario, materia))
    conn.commit()
    conn.close()

def verificar_login(email_ou_matricula, senha):
    conn = db.conectar()
    cursor = conn.cursor()
    # Busca o usuário sem verificar senha primeiro
    cursor.execute("""
    SELECT * FROM usuarios WHERE (email = ? OR matricula = ?)
    """, (email_ou_matricula, email_ou_matricula))
    user = cursor.fetchone()
    conn.close()
    
    # Se encontrou o usuário, verifica se a senha está correta
    if user:
        senha_hash_armazenada = user[4]  # índice 4 é a coluna senha
        if verificar_senha(senha, senha_hash_armazenada):
            return user
    return None


# === FUNÇÕES PROFESSOR ===
def cadastrar_nota(materia, matricula, np1=None, np2=None, pim=None):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {materia} WHERE matricula = ?", (matricula,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute(f"""
            UPDATE {materia}
            SET np1 = COALESCE(?, np1),
                np2 = COALESCE(?, np2),
                pim = COALESCE(?, pim)
            WHERE matricula = ?
        """, (np1, np2, pim, matricula))
    else:
        cursor.execute(f"""
            INSERT INTO {materia} (matricula, np1, np2, pim)
            VALUES (?, ?, ?, ?)
        """, (matricula, np1, np2, pim))
    conn.commit()
    conn.close()

def consultar_notas(materia, matricula):
    """Função legada - mantida para compatibilidade. Use consultar_notas_por_disciplina."""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT np1, np2, pim FROM {materia} WHERE matricula = ?", (matricula,))
    notas = cursor.fetchone()
    conn.close()
    return notas

def consultar_notas_por_disciplina(disciplina_id, matricula):
    """Consulta notas NP1, NP2 e PIM de um aluno em uma disciplina específica"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT np1, np2, pim FROM notas 
        WHERE disciplina_id = ? AND matricula = ?
    """, (disciplina_id, matricula))
    notas = cursor.fetchone()
    conn.close()
    return notas

def cadastrar_nota_por_disciplina(disciplina_id, matricula, np1=None, np2=None, pim=None):
    """Cadastra notas NP1, NP2 e PIM na tabela de notas usando disciplina_id"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Verifica se já existe registro
    cursor.execute("SELECT id FROM notas WHERE disciplina_id = ? AND matricula = ?", (disciplina_id, matricula))
    existe = cursor.fetchone()
    
    if existe:
        cursor.execute("""
            UPDATE notas
            SET np1 = COALESCE(?, np1),
                np2 = COALESCE(?, np2),
                pim = COALESCE(?, pim)
            WHERE disciplina_id = ? AND matricula = ?
        """, (np1, np2, pim, disciplina_id, matricula))
    else:
        cursor.execute("""
            INSERT INTO notas (disciplina_id, matricula, np1, np2, pim)
            VALUES (?, ?, ?, ?, ?)
        """, (disciplina_id, matricula, np1, np2, pim))
    
    conn.commit()
    conn.close()
    return True

def atualizar_presenca(matricula, data, presente):
    """Atualiza ou insere presença de um aluno em uma data específica"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Verificar se já existe registro para esta matrícula e data
    cursor.execute("SELECT id FROM presencas WHERE matricula = ? AND data = ?", (matricula, data))
    existe = cursor.fetchone()
    
    if existe:
        # Atualizar registro existente
        cursor.execute("UPDATE presencas SET presente = ? WHERE matricula = ? AND data = ?", (presente, matricula, data))
    else:
        # Inserir novo registro
        cursor.execute("INSERT INTO presencas (matricula, data, presente) VALUES (?, ?, ?)", (matricula, data, presente))
    
    conn.commit()
    conn.close()

def consultar_presenca(matricula):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT data, presente FROM presencas WHERE matricula = ?", (matricula,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_presencas_disciplina(disciplina_id):
    """Retorna lista de presenças de todos os alunos de uma disciplina"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Buscar todos os alunos da disciplina
    alunos = buscar_alunos_por_disciplina(disciplina_id)
    
    if not alunos:
        conn.close()
        return []
    
    # Para cada aluno, buscar suas presenças
    resultados = []
    for aluno in alunos:
        nome_aluno, matricula = aluno
        
        # Buscar todas as presenças do aluno
        cursor.execute("SELECT data, presente FROM presencas WHERE matricula = ? ORDER BY data DESC", (matricula,))
        presencas = cursor.fetchall()
        
        # Calcular estatísticas
        total_presencas = len(presencas)
        presentes = sum(1 for p in presencas if p[1] == 1)
        faltas = total_presencas - presentes
        percentual_presenca = (presentes / total_presencas * 100) if total_presencas > 0 else 0
        
        # Últimas presenças (últimas 5)
        ultimas_presencas = presencas[:5] if len(presencas) > 5 else presencas
        
        resultados.append({
            'nome': nome_aluno,
            'matricula': matricula,
            'total_aulas': total_presencas,
            'presentes': presentes,
            'faltas': faltas,
            'percentual': percentual_presenca,
            'ultimas_presencas': ultimas_presencas
        })
    
    conn.close()
    return resultados

def adicionar_aula_cronograma(sala, data, dia_semana, conteudo):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cronograma (sala, data, dia_semana, conteudo)
    VALUES (?, ?, ?, ?)
    """, (sala, data, dia_semana, conteudo))
    conn.commit()
    conn.close()

def consultar_cronograma():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT sala, data, dia_semana, conteudo FROM cronograma")
    cronogramas = cursor.fetchall()
    conn.close()
    return cronogramas

def listar(tabela,*colunas):
    conn = db.conectar()
    listar = Listar(conn)

    colunas_str = ", ".join(colunas)
    lista = listar.listar(f"{tabela}", colunas_str)
    conn.close()
    return lista



def excluir_usuario(matricula):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
    usuario = cursor.fetchone()

    if usuario:
        cursor.execute("DELETE FROM usuarios WHERE matricula = ?", (matricula,))
        conn.commit()
        print(f"Usuário '{usuario[1]}' deletado com sucesso!")
    else:
        print(f"Nenhum usuário encontrado com a matricula {matricula}.")
    conn.close()

def redefinir_senha(matricula, nova_senha):
    conn = db.conectar()
    cursor = conn.cursor()

    usuario = consultar_usuario(matricula)

    if usuario == True:
        # Hash da nova senha antes de salvar
        nova_senha_hash = hash_senha(nova_senha)
        cursor.execute("""
            UPDATE usuarios
            SET senha = ?
            WHERE matricula = ?
    """, (nova_senha_hash, matricula,))
        conn.commit()
        conn.close()
        print("Senha redefinida com sucesso!")
        
    else:
        print(f"Nenhum usuário encontrado com a matricula {matricula}.")
    conn.close()

def consultar_usuario(matricula):
    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
    usuario = cursor.fetchone()

    return True if usuario else False

def buscar_dados_completos_aluno(matricula):
    """Busca todos os dados do aluno para relatório"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Buscar dados do aluno
    cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
    aluno = cursor.fetchone()
    
    if not aluno:
        conn.close()
        return None
    
    # Buscar todas as disciplinas
    disciplinas = buscar_disciplinas()
    
    # Buscar notas de todas as disciplinas
    notas_disciplinas = []
    if disciplinas:
        for disc_id, disc_nome in disciplinas:
            notas = consultar_notas_por_disciplina(disc_id, matricula)
            if notas and any(notas):
                notas_disciplinas.append({
                    'disciplina': disc_nome,
                    'np1': notas[0],
                    'np2': notas[1],
                    'pim': notas[2]
                })
    
    # Buscar presenças
    presencas = consultar_presenca(matricula)
    
    dados = {
        'aluno': aluno,
        'notas': notas_disciplinas,
        'presencas': presencas
    }
    
    conn.close()
    return dados



def listar_turmas():
    conn = db.conectar()
    lista = listar("turmas","nome, ano, professor_id")
    if lista:
        print(f"\n{"Turma":<15} | {"Ano":<15} | {"Professor":<15}")
        print("-" * 53)
        for u in lista: 
            professor_id = u[2] if u[2] is not None else "Sem professor"
            print(f"{u[0]:<15} | {u[1]:<15} | {professor_id:<15}")
    conn.close()

def listar_usuarios():
    conn = db.conectar()

    lista = listar("usuarios","nome, email, matricula, tipo_usuario")
    if lista:
        print("\n{:<15} | {:<25} | {:<15} | {:<10}".format("Nome", "Email", "Matrícula", "Tipo"))
        print("-" * 75)
    
        for u in lista:
            print("{:<15} | {:<25} | {:<15} | {:<10}".format(u[0], u[1], u[2], u[3]))
    conn.close()


def criar_turma(nome, ano, curso_id=None, matricula_professor=None):
    conn = db.conectar()
    cursor = conn.cursor()

    # Converter curso_id para inteiro se fornecido
    if curso_id:
        try:
            curso_id = int(curso_id) if curso_id else None
        except (ValueError, TypeError):
            print("❌ ID do curso deve ser um número!")
            conn.close()
            return False

    # Buscar ID do professor pela matrícula se fornecido
    professor_id = None
    if matricula_professor and matricula_professor.strip():
        cursor.execute("SELECT id FROM usuarios WHERE matricula = ? AND tipo_usuario = 'professor'", (matricula_professor.strip(),))
        prof = cursor.fetchone()
        if prof:
            professor_id = prof[0]
        else:
            print(f"❌ Professor com matrícula '{matricula_professor}' não encontrado!")
            conn.close()
            return False

    if professor_id:
        cursor.execute("""
        INSERT INTO turmas (nome, ano, professor_id, curso_id)
        VALUES (?, ?, ?, ?)
        """, (nome, ano, professor_id, curso_id))
    else:
        cursor.execute("""
        INSERT INTO turmas (nome, ano, curso_id)
        VALUES (?, ?, ?)
        """, (nome, ano, curso_id))
    conn.commit()   
    conn.close()
    print("✅ Turma criada com sucesso")
    return True

def excluir_turma(nome_turma):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM turmas WHERE nome = ?", (nome_turma,))
    turma = cursor.fetchone()

    if turma:
        cursor.execute("DELETE FROM turmas WHERE nome = ?", (nome_turma,))
        conn.commit()
        print(f"Turma deletada com sucesso!")
    else:
        print(f"Turma não encontrada.")
    conn.close()

def vincular_aluno_turma(matricula, nome_turma):
    try:
        conn = db.conectar()
        cursor = conn.cursor()
        
        # Buscar aluno na tabela usuarios
        cursor.execute("SELECT * FROM usuarios WHERE matricula = ? AND tipo_usuario = 'aluno'", (matricula,))
        aluno = cursor.fetchone()
        
        if not aluno:
            conn.close()
            print(f"Erro! Matrícula de aluno '{matricula}' não encontrada.")
            return False
        
        # Verificar se a turma existe e buscar o curso_id
        cursor.execute("SELECT curso_id FROM turmas WHERE nome = ?", (nome_turma.lower(),))
        turma = cursor.fetchone()
        
        if not turma:
            conn.close()
            print(f"Erro! Turma '{nome_turma}' não encontrada.")
            return False
        
        # Buscar o nome do curso se a turma tiver curso_id
        curso_nome = None
        if turma[0]:  # Se curso_id não for None
            cursor.execute("SELECT nome FROM cursos WHERE id = ?", (turma[0],))
            curso = cursor.fetchone()
            if curso:
                curso_nome = curso[0]
        
        # Atualizar turma_id e curso na tabela usuarios
        if curso_nome:
            cursor.execute("UPDATE usuarios SET turma_id = ?, curso = ? WHERE matricula = ? AND tipo_usuario = 'aluno'", (nome_turma.lower(), curso_nome, matricula))
        else:
            cursor.execute("UPDATE usuarios SET turma_id = ? WHERE matricula = ? AND tipo_usuario = 'aluno'", (nome_turma.lower(), matricula))
        
        conn.commit()
        conn.close()
        
        if curso_nome:
            print(f"✅ Aluno vinculado à turma '{nome_turma}' e ao curso '{curso_nome}' com sucesso!")
        else:
            print(f"✅ Aluno vinculado à turma '{nome_turma}' com sucesso!")
        return True
    except Exception as e:
        if conn:
            conn.close()
        print(f"Erro ao vincular aluno à turma: {str(e)}")
        raise

def vincular_professor_turma(matricula, nome_turma):
    try:
        conn = db.conectar()
        cursor = conn.cursor()

        # Buscar professor na tabela usuarios para obter o ID
        cursor.execute("SELECT id FROM usuarios WHERE matricula = ? AND tipo_usuario = 'professor'", (matricula,))
        professor = cursor.fetchone()

        if not professor:
            conn.close()
            print(f"Erro! Professor com matrícula '{matricula}' não encontrado.")
            return False

        professor_id = professor[0]
        
        # Verificar se a turma existe
        cursor.execute("SELECT * FROM turmas WHERE nome = ?", (nome_turma.lower(),))
        turma = cursor.fetchone()
        
        if not turma:
            conn.close()
            print(f"Erro! Turma '{nome_turma}' não encontrada.")
            return False

        # Atualizar turma com o ID do professor
        cursor.execute("""
            UPDATE turmas
            SET professor_id = ?
            WHERE nome = ?
        """, (professor_id, nome_turma.lower()))
        conn.commit()
        conn.close()
        print(f"✅ Professor vinculado à turma '{nome_turma}' com sucesso!")
        return True
    except Exception as e:
        if conn:
            conn.close()
        print(f"Erro ao vincular professor à turma: {str(e)}")
        raise


def listar_disciplinas():
    conn = db.conectar()
    lista = listar("disciplinas","id, nome, professor_id, carga_horaria")
    if lista:
        print(f"\n{"ID":<5} | {"Disciplina":<15} | {"Professor":<15} | {"Carga Horaria":<15} |")
        print("-" * 60)
        for u in lista:
            print(f"{u[0]:<5} | {u[1]:<15} | {u[2]:<15} | {u[3]} {"Horas":<12} |\n")
    else:
        return None
    conn.close()

def buscar_disciplinas():
    """Retorna lista de todas as disciplinas cadastradas"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM disciplinas ORDER BY nome")
    disciplinas = cursor.fetchall()
    conn.close()
    return disciplinas

def buscar_disciplinas_por_professor(professor_id):
    """Retorna lista de disciplinas vinculadas a um professor com nome do curso"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.id, d.nome, d.curso_id, COALESCE(c.nome, 'Sem curso') as nome_curso
        FROM disciplinas d
        LEFT JOIN cursos c ON d.curso_id = c.id
        WHERE d.professor_id = ?
        ORDER BY d.nome
    """, (professor_id,))
    disciplinas = cursor.fetchall()
    conn.close()
    return disciplinas

def buscar_disciplina_por_id(disciplina_id):
    """Retorna uma disciplina específica por ID"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, professor_id, carga_horaria, curso_id, turma_id FROM disciplinas WHERE id = ?", (disciplina_id,))
    disciplina = cursor.fetchone()
    conn.close()
    return disciplina

def buscar_alunos_por_disciplina(disciplina_id):
    """Retorna lista de alunos vinculados a uma disciplina através da turma"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Buscar a disciplina para obter o turma_id
    cursor.execute("SELECT turma_id FROM disciplinas WHERE id = ?", (disciplina_id,))
    disciplina = cursor.fetchone()
    
    if not disciplina or not disciplina[0]:
        conn.close()
        return []
    
    turma_id = disciplina[0]
    
    # Buscar alunos dessa turma
    cursor.execute("SELECT nome, matricula FROM usuarios WHERE turma_id = ? AND tipo_usuario = 'aluno' ORDER BY nome", (turma_id,))
    alunos = cursor.fetchall()
    conn.close()
    return alunos

def buscar_disciplinas_por_aluno(matricula):
    """Retorna lista de disciplinas vinculadas a um aluno através da turma"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Buscar a turma do aluno
    cursor.execute("SELECT turma_id FROM usuarios WHERE matricula = ? AND tipo_usuario = 'aluno'", (matricula,))
    aluno = cursor.fetchone()
    
    if not aluno or not aluno[0]:
        conn.close()
        return []
    
    turma_id = aluno[0]
    
    # Buscar disciplinas dessa turma com nome do curso
    cursor.execute("""
        SELECT d.id, d.nome, d.curso_id, COALESCE(c.nome, 'Sem curso') as nome_curso
        FROM disciplinas d
        LEFT JOIN cursos c ON d.curso_id = c.id
        WHERE d.turma_id = ?
        ORDER BY d.nome
    """, (turma_id,))
    disciplinas = cursor.fetchall()
    conn.close()
    return disciplinas

def listar_notas_disciplina(disciplina_id):
    """Retorna lista de todos os alunos e suas notas de uma disciplina"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Buscar todos os alunos da disciplina
    alunos = buscar_alunos_por_disciplina(disciplina_id)
    
    if not alunos:
        conn.close()
        return []
    
    # Para cada aluno, buscar suas notas
    resultados = []
    for aluno in alunos:
        nome_aluno, matricula = aluno
        
        # Buscar notas do aluno nesta disciplina
        cursor.execute("""
            SELECT np1, np2, pim FROM notas 
            WHERE disciplina_id = ? AND matricula = ?
        """, (disciplina_id, matricula))
        notas = cursor.fetchone()
        
        np1 = notas[0] if notas and notas[0] is not None else None
        np2 = notas[1] if notas and notas[1] is not None else None
        pim = notas[2] if notas and notas[2] is not None else None
        
        # Calcular média (se todas as notas existirem)
        media = None
        if np1 is not None and np2 is not None and pim is not None:
            media = (np1 + np2 + pim) / 3
        
        resultados.append({
            'nome': nome_aluno,
            'matricula': matricula,
            'np1': np1,
            'np2': np2,
            'pim': pim,
            'media': media
        })
    
    conn.close()
    return resultados

def buscar_id_professor_por_matricula(matricula):
    """Busca o ID do professor pela matrícula"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE matricula = ? AND tipo_usuario = 'professor'", (matricula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def criar_disciplina(nome, professor_matricula, carga_horaria, curso_id=None, turma_id=None):
    """Cria uma disciplina vinculada a um professor pela matrícula"""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Busca o ID do professor pela matrícula
    professor_id = None
    if professor_matricula:
        if isinstance(professor_matricula, str) and professor_matricula.strip():
            professor_id = buscar_id_professor_por_matricula(professor_matricula.strip())
            if not professor_id:
                print(f"❌ Professor com matrícula '{professor_matricula}' não encontrado!")
                conn.close()
                return False
    
    # Converte carga_horaria para inteiro
    try:
        if carga_horaria:
            carga_horaria = int(carga_horaria)
        else:
            print("❌ Carga horária é obrigatória!")
            conn.close()
            return False
    except (ValueError, TypeError):
        print("❌ Carga horária deve ser um número!")
        conn.close()
        return False

    # Converter curso_id para inteiro se fornecido
    if curso_id:
        try:
            curso_id = int(curso_id) if curso_id else None
        except (ValueError, TypeError):
            print("❌ ID do curso deve ser um número!")
            conn.close()
            return False

    # Verificar se a turma existe se fornecida
    if turma_id:
        # Se turma_id é string, fazer strip e verificar
        if isinstance(turma_id, str) and turma_id.strip():
            cursor.execute("SELECT * FROM turmas WHERE nome = ?", (turma_id.strip().lower(),))
            turma = cursor.fetchone()
            if not turma:
                print(f"❌ Turma '{turma_id}' não encontrada!")
                conn.close()
                return False
            turma_id = turma_id.strip().lower()
        elif not isinstance(turma_id, str):
            # Se não é string e não é None, pode ser um problema
            turma_id = None

    cursor.execute("""
    INSERT INTO disciplinas (nome, professor_id, carga_horaria, curso_id, turma_id)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, professor_id, carga_horaria, curso_id, turma_id))
    conn.commit()   
    conn.close()
    print("✅ Disciplina criada com sucesso")
    return True


def excluir_disciplina(id_disciplina):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM disciplinas WHERE id = ?", (id_disciplina,))
    disciplina = cursor.fetchall()

    if disciplina:
        cursor.execute("DELETE FROM disciplinas WHERE id = ?", (id_disciplina,))
        conn.commit()
        print(f"Disciplina deletada com sucesso!")
    else:
        print(f"Erro! id de disciplina não encontrado.")
    conn.close()

def vincular_disciplina_professor(id_disciplina, id_professor):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM disciplinas WHERE id = ?", (id_disciplina,))
    disciplina = cursor.fetchone()
    
    if disciplina:
        cursor.execute("UPDATE disciplinas SET professor_id = ? WHERE id = ?", (id_professor, id_disciplina))
        conn.commit()
        print(f"Disciplina vinculada ao professor com sucesso!")
    else:
        print(f"Erro! id de disciplina não encontrado.")
    conn.close()
    return True

def vincular_aluno_disciplina(matricula_aluno, id_disciplina):
    """Vincula um aluno a uma disciplina usando a tabela usuarios"""
    try:
        conn = db.conectar()
        cursor = conn.cursor()
        
        # Buscar aluno na tabela usuarios
        cursor.execute("SELECT * FROM usuarios WHERE matricula = ? AND tipo_usuario = 'aluno'", (matricula_aluno,))
        aluno = cursor.fetchone()
        
        if not aluno:
            conn.close()
            print(f"Erro! Aluno com matrícula '{matricula_aluno}' não encontrado.")
            return False
        
        # Verificar se a disciplina existe
        cursor.execute("SELECT * FROM disciplinas WHERE id = ?", (id_disciplina,))
        disciplina = cursor.fetchone()
        
        if not disciplina:
            conn.close()
            print(f"Erro! Disciplina com ID '{id_disciplina}' não encontrada.")
            return False
        
        # Nota: A vinculação aluno-disciplina é feita através da tabela de notas
        # que já tem a relação matricula e disciplina_id
        # Esta função pode ser usada para outras finalidades no futuro
        conn.close()
        print(f"Aluno vinculado à disciplina com sucesso!")
        return True
    except Exception as e:
        if conn:
            conn.close()
        print(f"Erro ao vincular aluno à disciplina: {str(e)}")
        raise


def vincular_disciplina_curso(id_disciplina, id_curso):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM disciplinas WHERE id = ?", (id_disciplina,))
    disciplina = cursor.fetchone()
    
    if disciplina:
        cursor.execute("UPDATE disciplinas SET curso_id = ? WHERE id = ?", (id_curso, id_disciplina))
        conn.commit()
        print(f"Disciplina vinculada ao curso com sucesso!")
    else:
        print(f"Erro! id de disciplina não encontrado.")
    conn.close()

def vincular_disciplina_turma(id_disciplina, nome_turma):
    """Vincula uma disciplina a uma turma. Todos os alunos da turma ficam automaticamente vinculados à disciplina."""
    conn = db.conectar()
    cursor = conn.cursor()
    
    # Verificar se a disciplina existe
    cursor.execute("SELECT * FROM disciplinas WHERE id = ?", (id_disciplina,))
    disciplina = cursor.fetchone()
    
    if not disciplina:
        conn.close()
        print(f"Erro! Disciplina com ID '{id_disciplina}' não encontrada.")
        return False
    
    # Verificar se a turma existe
    cursor.execute("SELECT * FROM turmas WHERE nome = ?", (nome_turma.lower(),))
    turma = cursor.fetchone()
    
    if not turma:
        conn.close()
        print(f"Erro! Turma '{nome_turma}' não encontrada.")
        return False
    
    # Atualizar o turma_id na disciplina
    cursor.execute("UPDATE disciplinas SET turma_id = ? WHERE id = ?", (nome_turma.lower(), id_disciplina))
    conn.commit()
    conn.close()
    print(f"✅ Disciplina vinculada à turma '{nome_turma}' com sucesso! Todos os alunos da turma estão automaticamente vinculados à disciplina.")
    return True

def cadastrar_notaa(avaliacao, matricula, nota, data_lancamento=None):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT avaliacao FROM avaliacoes WHERE id_matricula_fk = ? AND avaliacao = ?", (matricula, avaliacao))
    existente = cursor.fetchone()
    
    if existente is not None and avaliacao == existente[0]:
        cursor.execute("""
        UPDATE avaliacoes 
        SET nota = ?, data_lancamento = ?
        WHERE id_matricula_fk = ? AND avaliacao = ?
    """, (nota, data_lancamento, matricula, avaliacao))
        print(f"{avaliacao.upper()}: Nota para a matrícula {matricula} foi atualizada para {nota}")

    else:
        cursor.execute("""
            INSERT INTO avaliacoes (id_matricula_fk, nota, avaliacao, data_lancamento) VALUES (?, ?, ?, ?)""", (matricula, nota, avaliacao, data_lancamento))
        print(f"Nota {nota} lançada para a matrícula {matricula}!")
    
    conn.commit()
    conn.close()


def listar_cursos():
    conn = db.conectar()
    lista = listar("cursos","id, nome, inicio, duracao")
    if lista:
        print(f"\n{"ID":<5} | {"Nome":<20} | {"Início":<30} | {"Duração (semestres)":<20} |")
        print("-" * 80)
        for u in lista:
            print(f"{u[0]:<5} | {u[1]:<20} | {u[2]:<30} | {u[3]:<20} |\n")
    else:
        return None
    conn.close()

def criar_curso(nome, inicio, duracao):
    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cursos (nome, inicio, duracao)
    VALUES (?, ?, ?)
    """, (nome, inicio, duracao))
    conn.commit()   
    conn.close()
    print("✅ Curso criado com sucesso")

def excluir_curso(id_curso):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cursos WHERE id = ?", (id_curso,))
    curso = cursor.fetchone()

    if curso:
        cursor.execute("DELETE FROM cursos WHERE id = ?", (id_curso,))
        conn.commit()
        print(f"Curso deletado com sucesso!")
    else:
        print(f"Erro! id de curso não encontrado.")
    conn.close()   

def vincular_aluno_curso(matricula_aluno, id_curso):
    """Vincula um aluno a um curso usando a tabela usuarios"""
    try:
        conn = db.conectar()
        cursor = conn.cursor()
        
        # Buscar aluno na tabela usuarios
        cursor.execute("SELECT * FROM usuarios WHERE matricula = ? AND tipo_usuario = 'aluno'", (matricula_aluno,))
        aluno = cursor.fetchone()
        
        if not aluno:
            conn.close()
            print(f"Erro! Aluno com matrícula '{matricula_aluno}' não encontrado.")
            return False
        
        # Verificar se o curso existe
        cursor.execute("SELECT * FROM cursos WHERE id = ?", (id_curso,))
        curso = cursor.fetchone()
        
        if not curso:
            conn.close()
            print(f"Erro! Curso com ID '{id_curso}' não encontrado.")
            return False
        
        # Atualizar curso na tabela usuarios
        cursor.execute("UPDATE usuarios SET curso = ? WHERE matricula = ? AND tipo_usuario = 'aluno'", (id_curso, matricula_aluno))
        conn.commit()
        conn.close()
        print(f"Aluno vinculado ao curso com sucesso!")
        return True
    except Exception as e:
        if conn:
            conn.close()
        print(f"Erro ao vincular aluno ao curso: {str(e)}")
        raise

def listar_professores():
    """Lista todos os professores cadastrados"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, matricula, tipo_usuario FROM usuarios WHERE tipo_usuario = 'professor'")
    lista = cursor.fetchall()
    conn.close()
    
    if lista:
        print(f"\n{"ID":<5} | {"Nome":<20} | {"Email":<30} | {"Matrícula":<15} | {"Tipo":<10} |")
        print("-" * 90)
        for u in lista:
            print(f"{u[0]:<5} | {u[1]:<20} | {u[2]:<30} | {u[3] or 'N/A':<15} | {u[4]:<10} |")
        return lista
    else:
        print("\n⚠️ Nenhum professor cadastrado.")
        return None

def buscar_professores():
    """Retorna lista de professores para uso em interfaces"""
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, matricula FROM usuarios WHERE tipo_usuario = 'professor' ORDER BY nome")
    professores = cursor.fetchall()
    conn.close()
    return professores