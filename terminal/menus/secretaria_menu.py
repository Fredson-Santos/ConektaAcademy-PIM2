import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from sistema.funcoes import *

def area_secretaria(secretaria):
    print(f"\n🗂️ Bem-vindo(a), {secretaria[1]} (Secretaria)")
    while True:
        print("""
--- Área da Secretaria ---
1. Gerenciar usuários
2. Gerenciar turmas
3. Gerenciar disciplinas
4. Gerenciar cursos
5. Emitir/Consultar relatórios
6. Sair
""")
        opc = input("Escolha: ").strip()
        if opc == "1":
            while True:
                print("""
--- GERENCIAR USUÁRIOS ---
1. Listar usuários
2. Cadastrar novo usuário
3. Excluir usuário
4. Resetar senha de usuário
5. Voltar
""")
                opc = input("Escolha: ").strip()
                
                if opc == "1":
                    listar_usuarios()

                elif opc == "2":
                    tipo_usuario = int(input("1- Professor\n2-Aluno\n3-Secretaria\nTipo de usuario:"))
                    nome = input("Nome: ")
                    while not nome:
                        print("❌ O nome não pode ficar em branco!")
                        nome = input("Nome: ")
                    email = input("Email (ou deixe em branco se for aluno): ")
                    matricula = input("Matrícula (ou deixe em branco se for professor): ")
                    senha = input("Senha: ")
                    while not senha:
                        print("❌ A senha não pode ficar em branco!")
                        senha = input("Senha: ")
                    if tipo_usuario == 1:
                        tipo_usuario = "professor"
                        materia = input("Digite a disciplina do professor: ")
                        while not materia:
                            print("❌ A materia não pode ficar em branco!")
                            materia = input("Digite a disciplina do professor: ")
                    elif tipo_usuario == 2:
                        tipo_usuario = "aluno"
                        materia = None
                    else:
                        tipo_usuario = "secretaria"
                        materia = None
                    
                    adicionar_usuario(nome, email, matricula, senha, tipo_usuario, materia)
                    print("✅ Usuário cadastrado com sucesso!")
        
                elif opc == "3":
                    matricula = input("Digite a matricula do usuario a ser excluido: ")
                    while not matricula:
                        print("❌ A matricula não pode ficar em branco!")
                        matricula = input("Digite a matricula do usuario a ser excluido: ")
                    excluir_usuario(matricula)
                    
                elif opc == "4":
                    matricula = input("Digite a matrícula para redefinir a senha: ")
                    while not matricula:
                        print("❌ A matrícula não pode ficar em branco!")
                        matricula = input("Digite a matrícula para redefinir a senha: ")

                    usuario = consultar_usuario(matricula)

                    while not usuario:
                        print("❌ Matrícula não encontrada!")
                        matricula = input("Digite a matrícula para redefinir a senha: ")
                        usuario = consultar_usuario(matricula)

                    nova_senha = input("Digite a nova senha: ")
                    while not nova_senha:
                        print("❌ A senha não pode ficar em branco!")
                        nova_senha = input("Digite a nova senha: ")

                    redefinir_senha(matricula, nova_senha)

                elif opc == "5":
                    break

        elif opc == "2":
            while True:
                print("""
--- GERENCIAR TURMAS ---
1. Listar turmas
2. Criar nova turma
3. Excluir turma
4. Vincular turma a professor
5. Voltar
""")
                opc = input("Escolha: ").strip()
                if opc == "1":
                    listar_turmas()


                elif opc == "2":
                    nome = input("Digite o nome da turma: ")
                    while not nome:
                        print("❌ O nome não pode ficar em branco!")
                        nome = input("Digite o nome da turma: ")

                    ano = input("Digite o ano da turma: ")
                    while not ano:
                        print("❌ O ano não pode ficar em branco!")
                        ano = input("Digite o ano da turma: ")

                    matriculaProf = input("Digite a matricula do professor responsável (opcional): ")          
                    
                    if matriculaProf:
                        usuario = consultar_usuario(matriculaProf)
                        while not usuario:
                            print("❌ Matrícula não encontrada!")
                            matriculaProf = input("Digite uma matricula de professor valida: ")
                            usuario = consultar_usuario(matriculaProf)
                    
                    # Perguntar curso_id opcional
                    curso_id_input = input("Digite o ID do curso (ou deixe em branco): ").strip()
                    curso_id_turma = int(curso_id_input) if curso_id_input else None
                    criar_turma(nome.lower(), ano, curso_id_turma, matriculaProf if matriculaProf else None)


                elif opc == "3":
                    nome_turma = input("Digite o nome da turma: ")
                    excluir_turma(nome_turma)

                elif opc == "4":
                    matricula = input("Digite a matricula do professor: ")
                    listar_usuarios()
                    while not matricula:
                        print("❌ A matricula não pode ficar em branco!")
                        matricula = input("Digite a matricula do professor: ")
                    
                    usuario = consultar_usuario(matricula)

                    while not usuario:
                        print("❌ Matrícula não encontrada!")
                        matricula = input("Digite a matricula do professor: ")
                        usuario = consultar_usuario(matricula)

                    listar_turmas()
                    nome_turma = input("\nDigite a turma a ser vinculada: ")
                    vincular_professor_turma(matricula,nome_turma)

                elif opc == "5":
                    break

        elif opc == "3":
            while True:
                print("""
--- GERENCIAR DISCIPLINAS ---
1. Listar disciplinas
2. Criar nova disciplina
3. Excluir disciplina
4. Vincular disciplina a professor
5. Vincular disciplina a curso
6. Vincular aluno a disciplina
7. Voltar
""")
                opc = input("Escolha: ").strip()
                if opc == "1":
                    listar_disciplinas()
                

                elif opc == "2":
                    nome = input("Digite o nome da disciplina: ")
                    listar_professores()
                    professor = input("Digite o matricula do professor que ira lecionar(ou deixe em branco): ")
                    carga_horaria = input("Informe a carga horaria da disciplina(em horas): ")
                    curso_id = input("Informe o ID do curso ao qual a disciplina pertence (ou deixe em branco): ")
                    curso_id = int(curso_id) if curso_id.strip() else None
                    turma_id = input("Informe o nome da turma (ou deixe em branco): ").strip()
                    turma_id = turma_id.lower() if turma_id else None
                    criar_disciplina(nome.lower(), professor, carga_horaria, curso_id, turma_id)


                elif opc == "3":
                    listar_disciplinas()
                    id_disciplina = input("Digite o id da disciplina que deseja excluir: ")
                    excluir_disciplina(id_disciplina)


                elif opc == "4":
                    listar_disciplinas()
                    if listar_disciplinas() is not None:
                        listar_disciplinas()
                        id_disciplina = input("Digite o id da disciplina que deseja vincular a professor: ")
                        while not id_disciplina:
                            print("❌ A matricula não pode ficar em branco!")
                            id_disciplina = input("Digite o id da disciplina que deseja vincular a professor: ")
                        listar_disciplinas()
                        listar_professores()
                        id_professor = input("Digite a matricula do professor que deseja vincular a disciplina: ")
                        while not id_professor:
                            print("❌ A matricula não pode ficar em branco!")
                            id_professor = input("Digite a matricula do professor que deseja vincular a disciplina: ")
                        vincular_disciplina_professor(id_disciplina, id_professor)
                    else:
                        print("❌ Nenhuma disciplina encontrada!")
                        break

                elif opc == "5":
                    listar_disciplinas()
                    if listar_disciplinas() is not None:
                        id_disciplina = input("Digite o id da disciplina que deseja vincular a curso: ")
                        while not id_disciplina:
                            print("❌ A matricula não pode ficar em branco!")
                            id_disciplina = input("Digite o id da disciplina que deseja vincular a curso: ")
                        listar_cursos()
                        id_curso = input("Digite o id do curso que deseja vincular a disciplina: ")
                        while not id_curso:
                            print("❌ A matricula não pode ficar em branco!")
                            id_curso = input("Digite o id do curso que deseja vincular a disciplina: ")
                        vincular_disciplina_curso(id_disciplina, id_curso)
                    else:
                        print("❌ Nenhuma disciplina encontrada!")
                        break

                elif opc == "6":
                    break

        elif opc == "4":
            while True:
                print("""
--- GERENCIAR CURSOS ---
1. Listar cursos
2. Criar novo curso
3. Excluir curso
4. Voltar
""")                
                opc = input("Escolha: ").strip()
                if opc == "1":
                    listar_cursos()
                elif opc == "2":
                    nome = input("Digite o nome do curso: ")
                    inicio = input("Digite a data de inicio do curso: ")
                    duracao = input("Informe a duração do curso (em semestres): ")
                    criar_curso(nome, inicio, duracao)
                
                elif opc == "3":
                    listar_cursos()
                    id_curso = input("Digite o id do curso que deseja excluir: ")
                    excluir_curso(id_curso)
                
                elif opc == "4":
                    break



        elif opc == "7":
            break
