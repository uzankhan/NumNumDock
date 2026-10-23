# 🐰 NumNumDock

**The Secure-by-Default Local AI Deployment Engine.**

NumNumDock is a command-line tool that allows developers to run local Large Language Models (LLMs) securely. It wraps Ollama in a hardened Docker container with network isolation and provides a secure proxy for API key authentication.

## 🚀 Features

- **Zero-Config Security:** Runs Ollama in an isolated Docker network (no internet access).
- **API Key Authentication:** Built-in reverse proxy that verifies API keys before reaching the LLM.
- **Advanced Secret Redaction:** Fail-closed redaction layer that masks API keys, passwords, and PEM keys from generated text.
- **Hardware Detection:** Automatically recommends the best model based on your GPU/CPU.
- **Random Port Allocation:** Prevents port squatting and local network exposure.

## 📦 Installation

```bash
pip install numnumdock
```

🛠️ Usage
Deploy a secure local model:

bash
numnumdock run llama3.2:1b
Check the status of your local deployments:

bash
numnumdock status
Run security diagnostics:

bash
numnumdock doctor
🔒 Security Architecture
NumNumDock ensures that your local AI is never exposed to the public internet. It creates an internal Docker bridge network, downloads the model securely, disconnects the container from the internet, and serves it via an authenticated FastAPI proxy on 127.0.0.1.

📄 License
MIT License