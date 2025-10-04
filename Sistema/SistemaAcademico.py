from funcoes import adicionar_usuario, verificar_login, verificar_usuario

class SistemaAcademico:

    def area_professor(self):
        print("""\n--- Area Professor ---
            1. Cadastrar Notas
            2. Gerar Relatório
            3. Sair""")
        

    def area_aluno(self):
        print("""\n--- Area Aluno ---
            1. Ver Notas
            2. Sair""")

class Usuario:
    def __init__(self, nome, email, matricula, senha, tipo_usuario):
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.senha = senha
        self.tipo_usuario = tipo_usuario
        #self.curso = []
        #self.nota = []

   # def adicionar_nota(self, aula, nota):
        #self.aulas.append(aula)
       # self.notas.append(nota)

    #def listar_cursos(self):
        #return [aula.nome for curso in self.aulas], [nota for nota in self.notas]

    def aluno_registro(self):
        return (self.nome, self.matricula, self.senha)
    

sistema = SistemaAcademico()

while True:
    print("""
    Bem-vindo ao Sistema Acadêmico
    1. Cadastrar
    2. Login
    3. Sair
            """)

    escolha = input("Escolha uma opção: ")
    if escolha == '1':
        nome = input("Nome: ")
        email = input("Email: ")
        matricula = input("Matrícula: ")
        senha = input("Senha: ")
        tipo_usuario = 0 if "@prof" in email else 1
        Usuario(nome,email,matricula,senha,tipo_usuario)
        adicionar_usuario(nome, email, matricula, senha, tipo_usuario)

    elif escolha == '2':
        email = input("email: ")
        senha = input("Senha: ")
        

        if verificar_login(email, senha) == True:

            if verificar_usuario(email) == 1:
                print(f"✅ Aluno logado com sucesso!")
                sistema.area_aluno()
                
            else:
                print(f"✅ Professor logado com sucesso!")
                sistema.area_professor()
            
        else:
            print("❌ E-mail ou senha incorretos.")


    elif escolha == '3':
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")
