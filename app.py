# flask-angular-app/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 1. Inicialização e Configuração do CORS ---
app = Flask(__name__)

# Configura o Flask-CORS para permitir requisições vindas do servidor Angular.
# O Angular roda por padrão em http://localhost:4200.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})


# --- 2. Simulação de Dados em Memória ---
# (Em uma aplicação real, você usaria um banco de dados)
recursos = []
proximo_id = 1


# --- 3. Endpoint POST (Criação de Recurso) ---
@app.route('/api/recursos', methods=['POST'])
def criar_recurso():
    global proximo_id
    
    # Recebe e decodifica o JSON enviado pelo Angular
    dados_recebidos = request.get_json()
    
    if not dados_recebidos or 'nome' not in dados_recebidos:
        # Retorna um erro 400 se os dados estiverem incompletos
        return jsonify({'erro': 'Nome do recurso é obrigatório'}), 400

    # Cria o novo recurso
    novo_recurso = {
        'id': proximo_id,
        'nome': dados_recebidos['nome'],
        'status': 'Criado'
    }
    
    recursos.append(novo_recurso)
    proximo_id += 1

    # Retorna o recurso criado com o Status Code 201 (Created)
    return jsonify(novo_recurso), 201 

# --- 4. Endpoint GET (Listagem de Recursos) ---
@app.route('/api/recursos', methods=['GET'])
def listar_recursos():
    # Retorna todos os recursos com o Status Code 200 (OK)
    return jsonify(recursos), 200


# --- 5. Execução do Servidor ---
if __name__ == '__main__':
    # Roda o Flask na porta 5000
    print("Flask Server rodando em http://127.0.0.1:5000")
    app.run(debug=True, port=5000)