"""
Backend em Flask para o Chatbot IA
------------------------------------
Requisitos:
    pip install flask openai flask-cors

Como rodar:
    python backend.py

Depois abra o arquivo index.html no navegador.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Coloque sua chave de API aqui ou use variável de ambiente
API_KEY = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_AQUI")

client = OpenAI(api_key=API_KEY)

app = Flask(__name__)
CORS(app)  # permite que o front-end (HTML/JS) converse com este servidor

# Histórico da conversa (memória simples, em RAM)
historico = [
    {"role": "system", "content": "Você é um assistente útil e simpático."}
]


@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json()
    mensagem_usuario = dados.get("mensagem", "")

    if not mensagem_usuario:
        return jsonify({"erro": "Nenhuma mensagem enviada"}), 400

    historico.append({"role": "user", "content": mensagem_usuario})

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=historico,
            temperature=0.7,
        )
        texto_resposta = resposta.choices[0].message.content
        historico.append({"role": "assistant", "content": texto_resposta})
        return jsonify({"resposta": texto_resposta})

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
