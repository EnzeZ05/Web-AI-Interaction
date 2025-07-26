# DeepSeek‑R1 + Streamlit Chat

**Self‑hosted LLM chat UI that runs 100 % offline on your own machine.**

|               | What you get                                                                     |
| ------------- | -------------------------------------------------------------------------------- |
| Model      | **DeepSeek‑R1 14B** served by **Ollama**                                         |
| Frontend   | **Streamlit** chat with live token streaming and a faded *Thinking…* placeholder |
| Dev setup  | Write code in **PyCharm** on Windows, but execute everything in **Ubuntu WSL**   |
| Deployment | Single VPS (`systemd` services) or any Linux box                                 |

---

## 0 . Prerequisites

| Tool       | Version              | Notes                            |
| ---------- | -------------------- | -------------------------------- |
| **WSL 2**  | Win 10 22H2 / Win 11 | `wsl --install -d Ubuntu`        |
| **Ubuntu** | 22.04 LTS            | Any recent LTS works             |
| **Python** | 3.9 +                | Comes with Ubuntu; we use `venv` |
| **Ollama** | 0.1.30 +             | « curl install » script        |

> **Disk space:** DeepSeek‑R1 14B = ≈ 9 GB.

---

## 1 . Terminal‑only sanity check (5 minutes)

```bash
# 1 Install Ollama (one‑liner official script)
curl https://ollama.ai/install.sh | sh

# 2 Pull the model (first run only, ~9 GB)
ollama pull deepseek-r1:14b

# 3 Start the Ollama server (default 127.0.0.1:11434)
ollama serve
```

Open **another** WSL tab and test that the model works:

```bash
ollama run deepseek-r1:14b -- "What is the derivative of sin(x)?"
```

You should see the answer stream token‑by‑token. Press **Ctrl‑C** to stop.

---

## 2 . Clone + run the Streamlit UI

```bash
# 2‑a  Get the code
cd ~      # anywhere you like
git clone https://github.com/YOUR‑USER/deepseek-streamlit-chat.git
cd deepseek-streamlit-chat

# 2‑b  Create an isolated Python env (PEP 668‑safe)
python3 -m venv .venv
source .venv/bin/activate

# 2‑c  Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 2‑d  Run the web app  (leave Ollama running in another tab!)
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your Windows browser.

* Type a prompt → it appears in the left pane.
* The right pane shows **Thinking…** (faded) while the model reasons.
* Final answer streams in real time.

---

## 3 . PyCharm + WSL workflow (optional but recommended)

1. **Open PyCharm** → *Open* → `\wsl$\Ubuntu\home\<you>\deepseek-streamlit-chat`.
2. **File ▸ Settings ▸ Python Interpreter** → **Add ▸ Existing** → pick `.venv/bin/python`.
3. **Run ▸ Edit Configurations** → `streamlit run app.py`.
4. Hit Run. Live reload works: save a file, refresh the browser.

### Common tasks

| Task           | Shortcut / command                                           |
| -------------- | ------------------------------------------------------------ |
| Add a PyPI lib | `pip install <lib>` then **Sync Python Packages** in PyCharm |
| Freeze deps    | `pip freeze > requirements.txt`                              |
| Debug          | Right‑click `app.py` ▸ *Debug Streamlit App*                 |

---

## 4 . Deploy to a VPS (systemd)

```bash
# /etc/systemd/system/ollama.service
[Unit]
Description=Ollama Server
After=network.target

[Service]
ExecStart=/usr/bin/ollama serve
Restart=always
Environment="OLLAMA_HOST=127.0.0.1:11434"

[Install]
WantedBy=multi-user.target
```

```bash
# /etc/systemd/system/streamlit.service
[Unit]
Description=Streamlit LLM UI
After=network.target ollama.service

[Service]
WorkingDirectory=/opt/deepseek-streamlit-chat
ExecStart=/opt/deepseek-streamlit-chat/.venv/bin/streamlit run app.py \
         --server.port 8501 \
         --server.headless true \
         --server.enableCORS false
Restart=always

[Install]
WantedBy=multi-user.target
```

Load + enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ollama streamlit
```

Point Nginx or Caddy to `localhost:8501`, add HTTPS, done.

---

## 5 . Update Guide

| Need                 | One‑liner                                                                          |
| -------------------- | ---------------------------------------------------------------------------------- |
| New DeepSeek version | `ollama pull deepseek-r1:16b` and update `MODEL_NAME` in `app.py`. Restart server. |
| New Python deps      | `pip install <lib>` → `pip freeze > requirements.txt`                              |
| Backup code          | `zip -r ~/chat_backup.zip . -x '*.pyc' '*__pycache__*' '.venv/*'`                  |

---

## 6 . License

MIT © 2025 Enze
