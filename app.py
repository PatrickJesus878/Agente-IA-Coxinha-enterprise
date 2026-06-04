import streamlit as str
import os
from groq import Groq

# 1. Configuração da Página (Título e Layout)
str.set_page_config(
    page_title="Coxinha Enterprise - IA",
    page_icon="🍗",
    layout="centered"
)

# 2. Design de Milhões (CSS Customizado para deixar lindo e intuitivo)
str.markdown("""
    <style>
    /* Mudar a cor de fundo e fontes */
    .stApp {
        background-color: #FDFBF7;
    }
    h1, h2, h3 {
        color: #D35400 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Estilizar as caixas de chat */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }
    /* Botão Bonito */
    .stButton>button {
        background-color: #E67E22;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #D35400;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Exibição da Logo e Título
if os.path.exists("logo.png"):
    str.image("logo.png", width=180)
else:
    str.title("🍗 Coxinha Enterprise")

str.subheader("O sabor que move você! 🚇✈️")
str.write("Bem-vindo ao assistente inteligente da Coxinha Enterprise. Como posso te ajudar hoje?")

# 4. Conexão Oculta e Segura com a Groq
if "GROQ_API_KEY" in str.secrets:
    api_key = str.secrets["GROQ_API_KEY"]
else:
    str.error("Por favor, configure a sua chave GROQ_API_KEY nos Secrets do Streamlit.")
    str.stop()

client = Groq(api_key=api_key)

# 5. O Prompt Secreto do Agente (Amigável, Amável e Vendedor)
PROMPT_AGENTE = """
Você é a 'Coxinha Inteligente', o assistente virtual super amigável, amável, caloroso e prestativo da Coxinha Enterprise.
Seu objetivo é encantar os clientes, compartilhar receitas e fechar negócios de atacado com outras lanchonetes.

Suas diretrizes de personalidade e respostas:
1. Use emojis de comida e carinho (🍗, ❤️, ✨, ☕). Seja sempre muito educado, alegre e use termos acolhedores.
2. Localização: Atuamos com vendas rápidas nos metrôs e aeroportos (como Viracopos e Congonhas).
3. Preços: Nossos preços são médios e super justos pela qualidade artesanal que entregamos.
4. Receitas: Se o cliente pedir uma receita, compartilhe uma receita deliciosa de coxinha, com dicas de ouro, sempre incentivando ele a testar ou comprar a nossa.
5. Vendas B2B (Outras lanchonetes): Se uma empresa ou lanchonete quiser comprar em grande quantidade para revender, passe o nosso e-mail oficial: contato@coxinhaenterprise.com. Ofereça descontos especiais para parceiros comerciais!

Responda sempre em português de forma clara, bonita e organizada.
"""

# 6. Histórico de Conversa (Para a IA lembrar do que já foi dito)
if "messages" not in str.session_state:
    str.session_state.messages = [
        {"role": "system", "content": PROMPT_AGENTE}
    ]

# Mostrar as mensagens anteriores na tela (menos o prompt do sistema)
for msg in str.session_state.messages:
    if msg["role"] != "system":
        with str.chat_message(msg["role"]):
            str.write(msg["content"])

# 7. Entrada de texto do usuário
if user_input := str.chat_input("Digite sua mensagem aqui (ex: 'Me passa uma receita?' ou 'Quero revender')"):
    
    with str.chat_message("user"):
        str.write(user_input)
    
    str.session_state.messages.append({"role": "user", "content": user_input})
    
    with str.chat_message("assistant"):
        message_placeholder = str.empty()
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=str.session_state.messages,
            temperature=0.7,
        )
        
        resposta = completion.choices[0].message.content
        message_placeholder.write(resposta)
        
    str.session_state.messages.append({"role": "assistant", "content": resposta})
