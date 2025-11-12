import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from sistema.funcoes import *

def area_professor(professor):
    professor_id = professor[0]  # ID do professor
    print(f"\n🎓 Bem-vindo, Professor {professor[1]}")
    while True:
        print("""
--- Área do Professor ---
1. Lançar notas
2. Atualizar presença
3. Gerar relatório
4. Gerenciar cronograma
5. Bloco do professor
6. Suporte ChatBot
7. Sair
""")
        opc = input("Escolha uma opção: ").strip()

        if opc == "1":
            lancar_notas(professor_id)
        elif opc == "2":
            atualizar_presenca_menu()
        elif opc == "3":
            gerar_relatorio_menu(professor_id)
        elif opc == "4":
            gerenciar_cronograma_menu()
        elif opc == "5":
            bloco_professor()
        elif opc == "6":
            iniciar_chat()
        elif opc == "7":
            break
        else:
            print("❌ Opção inválida.")


def lancar_notas(professor_id):
    
    disciplinas = buscar_disciplinas_por_professor(professor_id)
    if not disciplinas:
        print("\n⚠️ Você não possui disciplinas vinculadas. Entre em contato com a secretaria.")
        return
    
    print(f"\n📘 Lançamento de Notas")
    print("\nSuas disciplinas:")
    for i, (disc_id, disc_nome) in enumerate(disciplinas, start=1):
        print(f"{i}. {disc_nome}")
    
    try:
        escolha = int(input("\nSelecione a disciplina: "))
        if escolha < 1 or escolha > len(disciplinas):
            print("❌ Opção inválida!")
            return
        
        disciplina_id, disciplina_nome = disciplinas[escolha - 1]
        matricula = input("Digite a matrícula do aluno: ").strip()
        
        print("\nDigite as notas (deixe em branco para não alterar):")
        np1_input = input("NP1: ").strip()
        np2_input = input("NP2: ").strip()
        pim_input = input("PIM: ").strip()
        
        np1 = float(np1_input) if np1_input else None
        np2 = float(np2_input) if np2_input else None
        pim = float(pim_input) if pim_input else None
        
        cadastrar_nota_por_disciplina(disciplina_id, matricula, np1, np2, pim)
        print("✅ Notas lançadas com sucesso!")
    except ValueError:
        print("❌ Por favor, digite valores numéricos válidos.")
    except Exception as e:
        print(f"❌ Erro ao lançar notas: {e}")


def atualizar_presenca_menu():
    matricula = input("Matrícula do aluno: ").strip()
    data = input("Data (ex: 14/10/2025): ").strip()
    presente = int(input("Presente? (1=Sim, 0=Não): "))
    atualizar_presenca(matricula, data, presente)
    print("✅ Presença atualizada com sucesso!")


def gerar_relatorio_menu(professor_id):
    
    disciplinas = buscar_disciplinas_por_professor(professor_id)
    if not disciplinas:
        print("\n⚠️ Você não possui disciplinas vinculadas.")
        return
    
    matricula = input("Matrícula do aluno: ").strip()
    presencas = consultar_presenca(matricula)
    
    print(f"\n📄 Relatório — Matrícula: {matricula}")
    print("\nNotas por Disciplina:")
    
    for disciplina_id, disciplina_nome in disciplinas:
        notas = consultar_notas_por_disciplina(disciplina_id, matricula)
        if notas:
            print(f"  {disciplina_nome}: NP1={notas[0] or 'N/A'} | NP2={notas[1] or 'N/A'} | PIM={notas[2] or 'N/A'}")
        else:
            print(f"  {disciplina_nome}: Nenhuma nota registrada")
    
    print("\nPresenças:")
    if presencas:
        for data, pres in presencas:
            print(f"  {data} - {'Presente' if pres else 'Faltou'}")
    else:
        print("  Nenhuma presença registrada.")


def gerenciar_cronograma_menu():
    while True:
        print("""
--- Gerenciar Cronograma ---
1. Ver cronograma
2. Adicionar aula
3. Voltar
""")
        opc = input("Escolha: ").strip()
        if opc == "1":
            cronos = consultar_cronograma()
            for sala, data, dia, conteudo in cronos:
                print(f"Sala {sala} | {data} ({dia}) | {conteudo}")
        elif opc == "2":
            sala = input("Sala: ").strip()
            data = input("Data: ").strip()
            dia = input("Dia da semana: ").strip()
            conteudo = input("Conteúdo: ").strip()
            adicionar_aula_cronograma(sala, data, dia, conteudo)
            print("✅ Aula adicionada com sucesso!")
        elif opc == "3":
            break
        else:
            print("❌ Inválido!")


def bloco_professor():
    print("\n🗒️ Bloco do Professor — anote livremente.")
    print("(Digite 'sair' para encerrar)")
    with open("bloco_professor.txt", "a", encoding="utf-8") as f:
        while True:
            texto = input("> ")
            if texto.lower() == "sair":
                break
            f.write(texto + "\n")
    print("✅ Anotações salvas!")
