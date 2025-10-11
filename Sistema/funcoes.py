import sqlite3
import database as db
from datetime import datetime

#if __name__ == "__main__":

#Esse arquivo armazena as funcoes que serao usadas no arquivo main

def adicionar_usuario(nome, email, matricula, senha, tipo_usuario):
    try:
        db.cur.execute("""
            INSERT INTO usuarios (nome, email, matricula, senha, tipo_usuario)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, email, matricula, senha, tipo_usuario))
        print(f"Usuário {nome} adicionado com sucesso!")
        db.con.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def verificar_login(email, senha):
    db.cur.execute("""
    SELECT email, senha FROM usuarios WHERE email = ? AND senha = ?
""", (email, senha))
    
    resultado = db.cur.fetchone()
    if resultado:
        return True
    else: 
        return False


#Verifica se o usuario é aluno(1) ou professor (0)
def verificar_usuario(email):
    db.cur.execute("SELECT tipo_usuario FROM usuarios WHERE email = ?", (email,))
    usuario = db.cur.fetchone()
    if usuario:
        return usuario[0]
    else: return None



def cadastrar_nota(avaliacao, matricula, nota):

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    db.cur.execute("SELECT avaliacao FROM avaliacoes WHERE id_matricula_fk = ? AND avaliacao = ?", (matricula, avaliacao))
    existente = db.cur.fetchone()
    print(existente)
    if existente is not None and avaliacao == existente[0]:
        db.cur.execute("""
        UPDATE avaliacoes 
        SET nota = ?, data_lancamento = ?
        WHERE id_matricula_fk = ? AND avaliacao = ?
    """, (nota, data, matricula, avaliacao))
        print(f"{avaliacao.upper()}: Nota para da matricula {matricula} foi atualizada para {nota}")

    else:
        db.cur.execute("""
            INSERT INTO avaliacoes (id_matricula_fk, nota, avaliacao, data_lancamento) VALUES (?, ?, ?, ?)""", (matricula, nota, avaliacao, data))
        print(f"Nota {nota} lançada para a matricula {matricula}!")
    
    db.con.commit()


def fechar_conexao():
    db.con.close()



