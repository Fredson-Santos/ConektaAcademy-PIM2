import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from sistema.funcoes import *

def area_aluno(aluno):
    print(f"\n🎓 Bem-vindo, {aluno[1]}!")
    while True:
        print("""
--- Área do Aluno ---
1. Ver notas
2. Ver presenças
3. Ver cronograma
4. Bloco do aluno
5. Sair
""")
        opc = input("Escolha: ").strip()

        if opc == "1":
            ver_notas(aluno)
        elif opc == "2":
            ver_presencas(aluno)
        elif opc == "3":
            ver_cronograma()
        elif opc == "4":
            bloco_aluno(aluno)
        elif opc == "5":
            break
        else:
            print("❌ Opção inválida.")


def ver_notas(aluno):
    disciplinas = buscar_disciplinas()
    if not disciplinas:
        print("\n⚠️ Nenhuma disciplina cadastrada no sistema.")
        return
    
    print("\nDisciplinas disponíveis:")
    for i, (disc_id, disc_nome) in enumerate(disciplinas, start=1):
        print(f"{i}. {disc_nome}")
    
    try:
        escolha = int(input("Selecione uma disciplina: "))
        if escolha < 1 or escolha > len(disciplinas):
            print("❌ Opção inválida!")
            return
        
        disciplina_id, disciplina_nome = disciplinas[escolha - 1]
        notas = consultar_notas_por_disciplina(disciplina_id, aluno[3])
        if notas:
            print(f"\n📘 {disciplina_nome} - NP1: {notas[0] or 'N/A'} | NP2: {notas[1] or 'N/A'} | PIM: {notas[2] or 'N/A'}")
        else:
            print(f"Nenhuma nota registrada para {disciplina_nome}.")
    except ValueError:
        print("❌ Por favor, digite um número válido.")
    except Exception as e:
        print(f"❌ Erro ao consultar notas: {e}")


def ver_presencas(aluno):
    presencas = consultar_presenca(aluno[3])
    print("\n📅 Presenças:")
    for data, pres in presencas:
        print(f"{data} - {'Presente' if pres else 'Faltou'}")


def ver_cronograma():
    print("\n📖 Cronograma de Aulas:")
    cronos = consultar_cronograma()
    for sala, data, dia, conteudo in cronos:
        print(f"Sala {sala} | {data} ({dia}) | {conteudo}")


def bloco_aluno(aluno):
    print("\n📔 Bloco do Aluno — suas anotações pessoais.")
    arquivo = f"bloco_{aluno[3]}.txt"
    print("(Digite 'sair' para encerrar)")
    with open(arquivo, "a", encoding="utf-8") as f:
        while True:
            texto = input("> ")
            if texto.lower() == "sair":
                break
            f.write(texto + "\n")
    print("✅ Anotações salvas!")
