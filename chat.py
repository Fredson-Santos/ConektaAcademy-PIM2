import requests

API_URL = "https://n8n.conekta.tech/webhook/chatbot-sa"



def enviar_mensagens(mensagem, matricula):
    try:
        payload = {
            "mensagem": mensagem,
            "matricula": matricula
        }
        resposta = requests.post(API_URL, json=payload, timeout=20)
        resposta.raise_for_status()

        return resposta.text

    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"
    
def iniciar_chat():
    matricula = input("\nDigite sua matricula ou email para iniciar o atendimento: ")
    print("\n🟢 Chat conectado! Digite 'sair' para encerrar.\n")

    while True: 
        mensagem = input("Você: ")

        if mensagem.lower() in ["sair", "exit", "quit"]:
            print("❌ Chat encerrado. 👋")
            break

        resposta = enviar_mensagens(mensagem,matricula)
        print(f"\nBot: {resposta}\n")

if __name__ == "__main__":
    iniciar_chat()
