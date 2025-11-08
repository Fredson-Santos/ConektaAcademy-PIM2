from csv import list_dialects
import re
import select
from sqlite3 import Cursor
from tkinter import N, NO

from urllib3.exceptions import ProxySchemeUnknown
import database as db
from chat import iniciar_chat


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
    cursor.execute("""
    INSERT INTO usuarios (nome, email, matricula, senha, tipo_usuario, materia)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, email, matricula, senha, tipo_usuario, materia))
    conn.commit()
    conn.close()

def verificar_login(email_ou_matricula, senha):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM usuarios WHERE (email = ? OR matricula = ?) AND senha = ?
    """, (email_ou_matricula, email_ou_matricula, senha))
    user = cursor.fetchone()
    conn.close()
    return user


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
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT np1, np2, pim FROM {materia} WHERE matricula = ?", (matricula,))
    notas = cursor.fetchone()
    conn.close()
    return notas

def atualizar_presenca(matricula, data, presente):
    conn = db.conectar()
    cursor = conn.cursor()
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
        print(f"Nenhum usuário encontrado com a matricula {matricula,}.")
    conn.close()

def redefinir_senha(matricula, nova_senha):
    conn = db.conectar()
    cursor = conn.cursor()

    usuario = consultar_usuario(matricula)

    if usuario == True:
        cursor.execute("""
            UPDATE usuarios
            SET senha = ?
            WHERE matricula = ?
    """, (nova_senha, matricula,))
        conn.commit()
        conn.close()
        print("Senha redefinida com secesso!")
        
    else:
        print(f"Nenhum usuário encontrado com a matricula {matricula}.")
    conn.close()

def consultar_usuario(matricula):
    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
    usuario = cursor.fetchone()

    return True if usuario else False



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
    conn.close


def criar_turma(nome, ano, matricula=None):
    conn = db.conectar()
    cursor = conn.cursor()

    if matricula:
        cursor.execute("""
        INSERT INTO turmas (nome, ano, professor_id)
        VALUES (?, ?, ?)
        """, (nome, ano, matricula))
    else:
        cursor.execute("""
        INSERT INTO turmas (nome, ano)
        VALUES (?, ?)
        """, (nome, ano))
    conn.commit()   
    conn.close()
    print("✅ Turma criada com sucesso")

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

def vincular_professor(matricula, nome_turma):
    conn = db.conectar()
    cursor = conn.cursor()

    usuario = consultar_usuario(matricula)

    if usuario:
        cursor.execute("""
            UPDATE turmas
            SET professor_id = ?
            WHERE nome = ?
        """, (matricula, nome_turma))
        conn.commit()
        print(f"✅ Professor vinculado à turma '{nome_turma}' com sucesso!")
    conn.close()


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

def criar_disciplina(nome, professor, carga_horaria):
    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO disciplinas (nome, professor_id, carga_horaria)
    VALUES (?, ?, ?)
    """, (nome, professor, carga_horaria))
    conn.commit()   
    conn.close()
    print("✅ Turma criada com sucesso")


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





def cadastrar_notaa(avaliacao, matricula, nota):
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT avaliacao FROM avaliacoes WHERE id_matricula_fk = ? AND avaliacao = ?", (matricula, avaliacao))
    existente = cursor.fetchone()
    print(existente)
    if existente is not None and avaliacao == existente[0]:
        cursor.execute("""
        UPDATE avaliacoes 
        SET nota = ?, data_lancamento = ?
        WHERE id_matricula_fk = ? AND avaliacao = ?
    """, (nota, matricula, avaliacao))
        print(f"{avaliacao.upper()}: Nota para da matricula {matricula} foi atualizada para {nota}")

    else:
        cursor.execute("""
            INSERT INTO avaliacoes (id_matricula_fk, nota, avaliacao) VALUES (?, ?, ?)""", (matricula, nota, avaliacao))
        print(f"Nota {nota} lançada para a matricula {matricula}!")
    
    conn.commit()
    conn.close()