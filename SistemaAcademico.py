import sqlite3

class SitemaAcademico:
    def area_professor(self):
        print("""\n--- Area Professor ---
              1. Cadastrar Notas
              2. Gerar Relatório
              3. Sair""")
        

    def area_aluno(self):
        print("""\n--- Area Aluno ---
              1. Ver Notas
              2. Sair""")
class Aluno:
    def __init__(self, nome, matricula, senha):
        self.nome = nome
        self.matricula = matricula
        self.senha = senha
        #self.curso = []
        #self.nota = []

   # def adicionar_nota(self, aula, nota):
        #self.aulas.append(aula)
       # self.notas.append(nota)

    #def listar_cursos(self):
        #return [aula.nome for curso in self.aulas], [nota for nota in self.notas]

    def aluno_registro(self):
        return (self.nome, self.matricula, self.senha)
    
    
class BancodeDados:
    def __init__(self):
        self.con = sqlite3.connect("sistema_academico.db")
        self.cur = self.con.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS aulas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                curso_id INTEGER,
                nota REAL,
                FOREIGN KEY(aluno_id) REFERENCES alunos(id),
                FOREIGN KEY(curso_id) REFERENCES cursos(id)
            )
        """)
        self.con.commit()

    def adicionar_aluno(self, aluno):
        sql_insert = "INSERT INTO alunos (nome, matricula, senha) VALUES (?, ?, ?)"
        try:
            self.cur.execute(sql_insert, aluno.aluno_registro())
            self.con.commit()
            print(f"Aluno {aluno.nome} adicionado com sucesso!")
        except sqlite3.IntegrityError:
            print(f"ERRO: Matrícula {aluno.matricula} já cadastrada.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            self.fechar_conexao() 
    
    def verificar_login(self, nome, matricula, senha):
        sql_query = "SELECT * FROM alunos WHERE nome = ? AND matricula = ? AND senha = ?"  # Consulta SQL para verificar a matrícula e senha.
        self.cur.execute(sql_query, (nome, matricula, senha)) # Executa a consulta com os parâmetros fornecidos.
        resultado = self.cur.fetchone() # Busca o primeiro resultado da consulta.
        return resultado is not None # Retorna True se o aluno foi encontrado, caso contrário, False.


    def fechar_conexao(self):
        self.con.close()
    
def main():
    print("""
    Bem-vindo ao Sistema Acadêmico
    1. Cadastrar
    2. Login
    3. Sair
          """)
    
    escolha = input("Escolha uma opção: ")
    if escolha == '1':
        nome = input("Nome: ")
        matricula = input("Matrícula: ")
        senha = input("Senha: ")
        novo_aluno = Aluno(nome, matricula, senha) # Cria um novo objeto Aluno com os dados fornecidos.
        banco = BancodeDados()  # Instancia o banco de dados. Isso cria o objeto banco e automaticamente, conecta-se ao banco e cria as tabela.
        banco.adicionar_aluno(novo_aluno)  # Adiciona o aluno ao banco de dados.    

    elif escolha == '2':
        nome = input("Nome: ")
        matricula = input("Matrícula: ")
        senha = input("Senha: ")
        banco = BancodeDados()  # Instancia o banco de dados.
         
        if matricula == 'ProfessorAdmin' and senha == 'Professor123':
            print("✅ Login de professor bem-sucedido!")
            sistema = SitemaAcademico()
            sistema.area_professor()
        
    
        elif banco.verificar_login(nome, matricula, senha): # Usa a lógica do banco de dados
            print(f"✅ Aluno {nome} logado com sucesso!")
            sistema = SitemaAcademico()
            sistema.area_aluno()
        
   
        else:
            print("❌ Matrícula ou senha incorretos.")


    elif escolha == '3':
        print("Saindo do sistema...")
    else:
        print("Opção inválida. Tente novamente.")
    
if __name__ == "__main__":
    main()