# Local DeepSeek Chat with Ollama + Streamlit

**Run DeepSeek‑R1 entirely offline with Ollama and give it a clean Streamlit interface — all developed from PyCharm under WSL.**

---

## Features

| Stack             | What it does                                                         |
| ----------------- | -------------------------------------------------------------------- |
| **Ollama**        | Pulls & serves the DeepSeek‑R1 14B model on `localhost:11434`.       |
| **Streamlit**     | Lightweight web UI with live token streaming and “thinking” display. |
| **WSL + PyCharm** | Linux‐native toolchain while coding comfortably on Windows.          |

---

## 🖥 Quick terminal chat

```bash
# Pull the model (≈ 9 GB once):
ollama pull deepseek-r1:14b

# Start the server (default port 11434)
ollama serve

# Chat from another shell
ollama run deepseek-r1:14b -- "Explain the Fast Inverse Square Root trick"
```

---

## Run the Streamlit web app

```bash
# Clone this repo
git clone https://github.com/YOUR‑USER/deepseek-streamlit-chat.git
cd deepseek-streamlit-chat

# Create an isolated env (avoids PEP 668 issues)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Ollama server must still be running in a separate shell
streamlit run app.py
```

Browse to [http://localhost:8501](http://localhost:8501) and start chatting. While the LLM thinks the UI shows a faded *Thinking…* placeholder, then streams the final answer token‑by‑token.

---

## Architecture

```
User → Streamlit UI (WSL) → Ollama (DeepSeek‑R1)
```

Two small processes; nothing else required.

---

## Full WSL + PyCharm setup

1. **Install WSL & Ubuntu**

   ```powershell
   wsl --install -d Ubuntu
   ```
2. **Inside Ubuntu**

   ```bash
   # Ollama
   curl https://ollama.ai/install.sh | sh
   ollama pull deepseek-r1:14b

   # Dev tools
   sudo apt update && sudo apt install zip python3-venv

   # Clone project
   git clone https://github.com/YOUR‑USER/deepseek-streamlit-chat.git ~/project
   cd ~/project
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **PyCharm**

   * Open `~/project` as a WSL project.
   * Settings ▸ Python Interpreter ▸ **Existing** → `.venv/bin/python`.
   * Run configuration → `streamlit run app.py`.

---

## Deploy on a small VPS

```bash
# /etc/systemd/system/ollama.service
[Service]
ExecStart=/usr/bin/ollama serve
Restart=always
Environment="OLLAMA_HOST=127.0.0.1:11434"

# /etc/systemd/system/streamlit.service
[Service]
WorkingDirectory=/opt/deepseek-streamlit-chat
ExecStart=/opt/deepseek-streamlit-chat/.venv/bin/streamlit run app.py \
         --server.port 8501 --server.headless true --server.enableCORS false
Restart=always

sudo systemctl enable --now ollama streamlit
```

Place Nginx / Caddy in front of port 8501 for HTTPS.

---

## Developer workflow

| Task                  | Command                                                        |
| --------------------- | -------------------------------------------------------------- |
| Start dev server      | `streamlit run app.py`                                         |
| Update DeepSeek model | `ollama pull deepseek-r1:16b`                                  |
| Freeze deps           | `pip freeze > requirements.txt`                                |
| Make a release zip    | `zip -r ../release.zip . -x '*.pyc' '*__pycache__*' '.venv/*'` |


---

## 📄 License

MIT © 2025 Enze
