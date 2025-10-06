import sqlite3
import database as db

#if __name__ == "__main__":

##### Puxar o arquivo do banco de dados para a raiz da pasta #######

#Esse arquivo armazena as funcoes que serao usadas no arquivo main

def adicionar_usuario(nome, email, matricula, senha, tipo_usuario):
    try:
        db.cur.execute("""
            INSERT INTO usuarios (nome, email, matricula, senha, tipo_usuario)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, email, matricula, senha, tipo_usuario))
        db.con.commit()
        print(f"Usuário {nome} adicionado com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    db.con.commit()


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




def fechar_conexao():
    db.con.close()


