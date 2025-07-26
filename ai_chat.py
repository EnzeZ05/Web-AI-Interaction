import streamlit as st
import ollama

st.set_page_config(page_title="DeepSeek‑R1 Chat", layout="centered")
st.title("Personalized AI Chat")

client = ollama.Client(host = "http://localhost:11434")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    st.chat_message(msg["role"]).markdown(msg["content"])

prompt = st.chat_input("Please enter your question…")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    ai_container = st.chat_message("AI")
    placeholder = ai_container.empty()
    placeholder.markdown("Thinking...")

    answer, thinking = "", ""
    stream = client.chat(
        model = "deepseek-r1:14b",
        messages = [{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.history],
        stream = True,
        think = True
    )

    for chunk in stream:
        if chunk["message"].get("thinking"):
            thinking += chunk["message"]["thinking"]
            placeholder.markdown(f"*Thinking…*\n\n{thinking}▌")
        elif chunk["message"].get("content"):
            answer += chunk["message"]["content"]
            placeholder.markdown(answer + "▌")

    placeholder.markdown(answer)
    st.session_state.history.append({"role": "AI", "content": answer})
