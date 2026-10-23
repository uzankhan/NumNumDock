# 🐰 NumNumDock

A secure-by-default local AI deployment engine for running LLMs privately, safely, and efficiently with Docker isolation.

NumNumDock is a Python CLI tool that wraps Ollama inside a hardened Docker environment, adds API-key protection, blocks public exposure, and helps developers deploy local models with a safer, cleaner workflow. It is designed for private AI usage, local experimentation, and secure model execution in development environments.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/Security-By%20Default-16a34a?style=for-the-badge" alt="Security by default" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

## Why NumNumDock?

Running local LLMs should be simple, safe, and private. Many setups expose models to the internet, leave endpoints unprotected, or make it difficult to manage security and deployment effectively.

NumNumDock solves this by combining:

- isolated Docker networking
- local-only serving model
- API key authentication
- secret redaction and fail-closed security checks
- automatic hardware-aware model recommendations
- random port allocation to reduce local exposure

This makes it a strong foundation for local AI experimentation, secure model access, and private lightweight deployment workflows.

---

## Key Features

- Secure-by-default local AI deployment
- Ollama wrapped in an isolated Docker network
- Internal-only communication between proxy and model runtime
- API key verification before requests reach the model
- HMAC-backed auth checks for request validation
- Secret redaction to hide API tokens, JWTs, passwords, and private keys
- Auto-selected model recommendation based on GPU availability
- Dynamic random port selection to reduce port collision and exposure
- Local proxy layer for safer access patterns
- Easy CLI usage for run, status, and diagnostics

---

## Architecture Overview

NumNumDock follows a simple secure flow:

1. Detect hardware and recommend a model
2. Start Ollama inside Docker
3. Pull the selected model securely
4. Isolate the container behind an internal network
5. Expose a local reverse proxy with API-key authentication
6. Route allowed requests only to the local LLM runtime

This keeps direct model access private while still giving developers a clean and usable local interface for AI workloads.

---

## Installation

### Prerequisites

- Python 3.9+
- Docker installed and running
- Git

### Install from source

```bash
git clone https://github.com/uzankhan/NumNumDock.git
cd NumNumDock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Install as a package

```bash
pip install numnumdock
```

---

## Usage

### Run a model

```bash
numnumdock run llama3.2:1b
```

If no model is specified, NumNumDock will choose a recommended one based on your hardware.

### Check status

```bash
numnumdock status
```

### Run diagnostics

```bash
numnumdock doctor
```

---

## Example Workflow

```bash
numnumdock run llama3.2:1b
```

After deployment, the tool starts a secure local proxy and prints the endpoint and generated API key. Requests must carry the correct Bearer token before they are forwarded to the local Ollama backend.

---

## Security Highlights

NumNumDock is designed with a fail-closed mindset:

- network isolation by default
- internal-only model communication
- authentication before request forwarding
- allowed endpoint restrictions
- request size limits
- secret masking for common sensitive values
- no unauthenticated public exposure

This helps reduce common risks when working with local model runtimes.

---

## Project Structure

```bash
NumNumDock/
├── cli.py
├── core/
│   ├── docker_manager.py
│   ├── hardware.py
│   ├── native_manager.py
│   ├── proxy.py
│   └── security.py
├── project.toml
├── requirements.txt
├── readme.md
├── .gitignore
└── LICENSE
```

---

## Roadmap

Planned improvements include:

- broader config management
- better model selection profiles
- more deployment modes
- improved observability and logs
- enhanced security hardening and policies
- easier multi-model management
- more community-driven feature contributions

---

## Contributing

Contributions are welcomed and appreciated.

If you want to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation checks where possible
5. Open a pull request

```bash
git checkout -b feature/my-improvement
git add .
git commit -m "Add my improvement"
git push origin feature/my-improvement
```

We believe in improving the project together through open-source collaboration.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Final Note

I’m very happy to contribute to this project and help make it even better with new ideas, improvements, and community support. Together, we can make NumNumDock more secure, more useful, and more powerful for local AI workflows.

<p align="center">
  <strong>Built with ❤️ for safer local AI workflows.</strong>
</p>
