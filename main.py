from funcoes import (
    criar_tabelas, adicionar_usuario, verificar_login,
    verificar_usuario, cadastrar_nota, consultar_notas,
    atualizar_presenca, consultar_presenca
)

# Garante que as tabelas existam
criar_tabelas()


class SistemaAcademico:

    def area_professor(self):
        while True:
            print("""
--- Área do Professor ---
1. Consultar Aluno
2. Cadastrar Cronograma
3. Documentos do Professor
4. Sair
""")
            opc = input("Escolha uma opção: ").strip()

            if opc == "1":
                matricula = input("Digite a matrícula do aluno: ")
                self.menu_consultar_aluno(matricula)

            elif opc == "2":
                self.cadastrar_cronograma()

            elif opc == "3":
                print("📂 Área de documentos do professor (em construção...)")

            elif opc == "4":
                print("Saindo da área do professor...")
                break

            else:
                print("❌ Opção inválida. Tente novamente.")

    def menu_consultar_aluno(self, matricula):
        while True:
            print(f"""
--- Consultando Aluno {matricula} ---
1. Cadastrar Nota
2. Atualizar Presença
3. Gerar Relatório
4. Voltar
""")
            opc = input("Escolha uma opção: ").strip()

            if opc == "1":
                avaliacao = input("Digite o nome da avaliação: ")
                nota = input("Digite a nota: ")
                cadastrar_nota(avaliacao, matricula, nota)
                print("✅ Nota cadastrada com sucesso!")

            elif opc == "2":
                data = input("Data da aula (dd/mm/aaaa): ")
                presenca = input("Presente? (1 = sim / 0 = não): ")
                atualizar_presenca(matricula, data, int(presenca))
                print("✅ Presença registrada!")

            elif opc == "3":
                notas = consultar_notas(matricula)
                presencas = consultar_presenca(matricula)
                print("\n📄 --- Relatório do Aluno ---")
                print("Notas:")
                for a, n in notas:
                    print(f"  {a}: {n}")
                print("Presenças:")
                for d, p in presencas:
                    print(f"  {d} - {'Presente' if p == 1 else 'Faltou'}")

            elif opc == "4":
                break

            else:
                print("❌ Opção inválida. Tente novamente.")

    def cadastrar_cronograma(self):
        print("""
📅 --- Cadastrar Cronograma ---
Exemplo:
Sala 6 - 19/02/2025 (Terça) -> Aula de Aritmética
Sala 5 - 20/02/2025 (Quarta) -> Aula de Fração
""")
        print("Função de cronograma em desenvolvimento...")

    def area_aluno(self):
        matricula = input("Digite sua matrícula: ")
        while True:
            print("""
--- Área do Aluno ---
1. Ver Notas
2. Ver Presenças
3. Sair
""")
            opc = input("Escolha uma opção: ").strip()

            if opc == "1":
                notas = consultar_notas(matricula)
                print("\n📘 --- Suas Notas ---")
                for a, n in notas:
                    print(f"{a}: {n}")

            elif opc == "2":
                presencas = consultar_presenca(matricula)
                print("\n📗 --- Suas Presenças ---")
                for d, p in presencas:
                    print(f"{d} - {'Presente' if p == 1 else 'Faltou'}")

            elif opc == "3":
                print("Saindo da área do aluno...")
                break

            else:
                print("❌ Opção inválida. Tente novamente.")


class Usuario:
    def __init__(self, nome, email, matricula, senha, tipo_usuario):
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.senha = senha
        self.tipo_usuario = tipo_usuario


# ---------- MENU PRINCIPAL ----------
sistema = SistemaAcademico()

while True:
    print("""
🏫 Bem-vindo ao Sistema Acadêmico
1. Cadastrar Usuário
2. Login
3. Sair
""")
    escolha = input("Escolha uma opção: ").strip()

    if escolha == '1':
        nome = input("Nome: ")
        email = input("Email: ")
        matricula = input("Matrícula: ")
        senha = input("Senha: ")
        tipo_usuario = int(input("Tipo de usuário (0 = Professor / 1 = Aluno): "))
        adicionar_usuario(nome, email, matricula, senha, tipo_usuario)
        print("✅ Usuário cadastrado com sucesso!")

    elif escolha == '2':
        email = input("Email: ")
        senha = input("Senha: ")

        if verificar_login(email, senha):
            tipo = verificar_usuario(email)
            if tipo == 1:
                print("✅ Aluno logado com sucesso!")
                sistema.area_aluno()
            elif tipo == 0:
                print("✅ Professor logado com sucesso!")
                sistema.area_professor()
            else:
                print("❌ Tipo de usuário desconhecido.")
        else:
            print("❌ Email ou senha incorretos.")

    elif escolha == '3':
        print("Saindo do sistema...")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")