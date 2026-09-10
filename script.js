const inputMensagem = document.getElementById("input-mensagem");
const botaoEnviar = document.getElementById("botao-enviar");
const chatMensagens = document.getElementById("chat-mensagens");

const URL_BACKEND = "http://127.0.0.1:5000/chat";

function adicionarMensagem(texto, tipo) {
    const div = document.createElement("div");
    div.classList.add("mensagem", tipo);
    div.textContent = texto;
    chatMensagens.appendChild(div);
    chatMensagens.scrollTop = chatMensagens.scrollHeight;
}

async function enviarMensagem() {
    const texto = inputMensagem.value.trim();
    if (!texto) return;

    adicionarMensagem(texto, "usuario");
    inputMensagem.value = "";

    adicionarMensagem("Digitando...", "ia");
    const mensagemCarregando = chatMensagens.lastChild;

    try {
        const resposta = await fetch(URL_BACKEND, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem: texto }),
        });

        const dados = await resposta.json();

        if (dados.erro) {
            mensagemCarregando.textContent = "Erro: " + dados.erro;
        } else {
            mensagemCarregando.textContent = dados.resposta;
        }
    } catch (erro) {
        mensagemCarregando.textContent = "Erro ao conectar com o servidor.";
    }
}

botaoEnviar.addEventListener("click", enviarMensagem);

inputMensagem.addEventListener("keypress", (evento) => {
    if (evento.key === "Enter") {
        enviarMensagem();
    }
});
