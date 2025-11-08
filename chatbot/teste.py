import requests

API_URL = "https://n8n.conekta.tech/webhook/chatbot-sa"

def enviar_mensagem(mensagem):
    try:
        r = requests.post(API_URL, json={"mensagem": mensagem})
        r.raise_for_status()
        return r.json().get("resposta", "Sem resposta.")
    except Exception as e:
        return f"Erro: {e}"

while True:
    msg = input("Você: ")
    if msg.lower() in ["sair", "exit"]:
        break
    print("Bot:", enviar_mensagem(msg))