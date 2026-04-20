import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="DataMentor AI", page_icon="🐍")

# Interface visual
st.title("🐍 DataMentor AI")
st.subheader("Seu mentor sênior de Python, SQL e Dataviz")
st.markdown("---")

# --- CONFIGURAÇÃO DA API (SEGURANÇA) ---
# Tenta pegar a chave do Streamlit Secrets (Nuvem) ou Variável de Ambiente (Local)
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Por favor, configure a GOOGLE_API_KEY nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

# Inicializa o modelo que funcionou nos seus testes
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Persona do Mentor
SYSTEM_PROMPT = (
    "Você é o DataMentor AI, um Analista de Dados Sênior. Seu objetivo é ajudar analistas juniores. "
    "1. Ao fornecer código Python, use bibliotecas como Pandas, Seaborn ou Plotly. "
    "2. Para SQL, foque em legibilidade e boas práticas. "
    "3. Para Dataviz, sugira o melhor gráfico e dicas de storytelling. "
    "Sempre explique o porquê de cada solução de forma didática."
)

# --- HISTÓRICO DE MENSAGENS ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ÁREA DE INTERAÇÃO ---
if prompt := st.chat_input("Como posso te ajudar com seus dados hoje?"):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta com a IA
    with st.chat_message("assistant"):
        with st.spinner("Analisando e gerando solução..."):
            try:
                # Combina a persona com a pergunta
                full_query = f"{SYSTEM_PROMPT}\n\nPergunta do Júnior: {prompt}"
                response = model.generate_content(full_query)
                
                resposta = response.text
                st.markdown(resposta)
                
                # Guarda a resposta no histórico
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
