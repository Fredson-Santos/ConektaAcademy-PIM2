from funcoes import *

def area_professor(professor):
    materia = professor[6]
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
            lancar_notas()
        elif opc == "2":
            atualizar_presenca_menu()
        elif opc == "3":
            gerar_relatorio_menu(materia)
        elif opc == "4":
            gerenciar_cronograma_menu()
        elif opc == "5":
            bloco_professor()
        elif opc == "7":
            break
        else:
            print("❌ Opção inválida.")


def lancar_notas():
    print(f"\n📘 Lançamento de Notas")
    matricula = input("Digite a matrícula do aluno: ").strip()
    avaliacao = (input("Digite a avalicao: "))
    nota = float(input(f"Digite a nota da avaliação '{avaliacao}': "))
    
    cadastrar_notaa(avaliacao, matricula, nota,)
    print("✅ Notas lançadas com sucesso!")


def atualizar_presenca_menu():
    matricula = input("Matrícula do aluno: ").strip()
    data = input("Data (ex: 14/10/2025): ").strip()
    presente = int(input("Presente? (1=Sim, 0=Não): "))
    atualizar_presenca(matricula, data, presente)
    print("✅ Presença atualizada com sucesso!")


def gerar_relatorio_menu(materia):
    matricula = input("Matrícula do aluno: ").strip()
    notas = consultar_notas(materia, matricula)
    presencas = consultar_presenca(matricula)
    print(f"\n📄 Relatório — {matricula}")
    if notas:
        print(f"Notas: NP1={notas[0]} | NP2={notas[1]} | PIM={notas[2]}")
    else:
        print("Nenhuma nota registrada.")
    print("Presenças:")
    for data, pres in presencas:
        print(f"{data} - {'Presente' if pres else 'Faltou'}")


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
