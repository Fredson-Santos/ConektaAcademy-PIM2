import requests
import datetime

API_URL = "https://n8n.conekta.tech/webhook/chatbot-sa"

session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def enviar_mensagens(mensagem, email):
    try:
        payload = {
            "mensagem": mensagem,
            "email": email,
            "session_id": session_id
        }
        resposta = requests.post(API_URL, json=payload, timeout=20)
        resposta.raise_for_status()

        return resposta.text

    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {e}"
    
def iniciar_chat():
    email = input("\nDigite seu email para iniciar o atendimento: ")
    print("\n🟢 Chat conectado! Digite 'sair' para encerrar.\n")

    while True: 
        mensagem = input("Você: ")

        if mensagem.lower() in ["sair", "exit", "quit"]:
            print("❌ Chat encerrado. 👋")
            break

        resposta = enviar_mensagens(mensagem,email)
        print(f"\nBot: {resposta}\n")

if __name__ == "__main__":
    iniciar_chat()
