# NumNumDock

NumNumDock is a secure local deployment tool for running large language models (LLMs) inside Docker containers with a protected, isolated network setup. It helps users quickly run open-source models on their machine without exposing the backend directly to the internet.

The project automatically checks your hardware, recommends a suitable model, validates Docker availability, deploys the model in a secure container, and exposes a local proxy API with a generated access key. It is designed for developers and AI enthusiasts who want a simple, safe, and self-hosted way to experiment with LLMs.

## Features

- Automatic hardware detection
- Recommended model selection based on available resources
- Docker availability and health checks
- Secure containerized LLM deployment
- Local API proxy with random API key generation
- Status and diagnostics commands for troubleshooting

## Quick Start

1. Install Docker Desktop or Docker Engine.
2. Clone the repository:
   ```bash
   git clone https://github.com/uzankhan/NumNumDock.git
   cd NumNumDock
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python cli.py run
   ```
   or specify a model:
   ```bash
   python cli.py run llama3.2:1b
   ```
5. Check status:
   ```bash
   python cli.py status
   ```

## Commands

- `python cli.py run [MODEL]` — deploy a model securely
- `python cli.py status` — check Docker and running containers
- `python cli.py doctor` — review configuration and health information

## Why NumNumDock?

NumNumDock makes local AI inference easier, safer, and more practical by combining model deployment, networking, and security in one lightweight workflow. It is ideal for users who want to self-host LLMs while keeping the setup simple and secure.
