import subprocess
from .security import generate_api_key

def deploy_native_llm(model_name: str):
    api_key = generate_api_key()
    print(f"📥 Pulling model: {model_name}...")
    subprocess.run(["ollama", "pull", model_name], check=True)
    print(f"🏃 Starting model: {model_name}...")
    subprocess.Popen(["ollama", "run", model_name], shell=True)
    return api_key

def list_native_llms():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    models = []
    for line in result.stdout.strip().split("\n")[1:]:
        parts = line.split()
        if len(parts) >= 3:
            models.append({"name": parts[0], "size": parts[2]})
    return models

def stop_native_llm(model_name: str):
    subprocess.run(["ollama", "stop", model_name], capture_output=True)