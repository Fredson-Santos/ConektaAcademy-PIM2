import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sistema.database import *
from sistema.funcoes import *
from sistema.classes import *


# === EXECUÇÃO PRINCIPAL ===
sistema = SistemaAcademico()

while True:
    print("""
===== CONEKTAACADEMY =====
1. Cadastrar usuário
2. Login
3. Ajuda - ChatBot
4. Sair
""")
    escolha = input("Escolha: ").strip()
    
    if escolha == "1":
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
        if "@prof" in email:
            tipo_usuario = "professor"
            materia = None  # Matéria será vinculada pela secretaria através de disciplinas
        
        elif "@sec" in email:
            tipo_usuario = "secretaria"
            materia = None
        else: 
            tipo_usuario = "aluno"
            materia = None
        adicionar_usuario(nome, email, matricula, senha, tipo_usuario, materia)
        print("✅ Usuário cadastrado com sucesso!")

    elif escolha == "2":
        login = input("Email ou Matrícula: ")
        senha = input("Senha: ")
        usuario = verificar_login(login, senha)

        if usuario:
            if usuario[5] == "professor":
                sistema.area_professor(usuario)
            elif usuario[5] == "secretaria":
                sistema.area_secretaria(usuario)
            else:
                sistema.area_aluno(usuario)
        else:
            print("❌ Login inválido!")
    
    elif escolha == "3":
        iniciar_chat()

    elif escolha == "4":
        print("Saindo do sistema...")
        break
    else:
        print("❌ Opção inválida!")