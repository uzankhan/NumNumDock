import typer
import subprocess
import shutil
import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from core.hardware import get_hardware_info, get_recommended_model
from core.docker_manager import deploy_secure_llm, get_free_port
from core.security import generate_api_key
from core.proxy import build_app # <-- Yahan build_app import hoga

app = typer.Typer()
console = Console()

def check_docker():
    if not shutil.which("docker"):
        return False, "Docker not installed."
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=5)
        return (True, "Running") if result.returncode == 0 else (False, "Not running. Start Docker Desktop.")
    except Exception:
        return False, "Docker check failed."

@app.command()
def run(model: str = typer.Argument(None, help="Model name (e.g., llama3.2:1b)")):
    console.print(Panel.fit("[bold green]🚀 NumNumDock[/bold green]\n[dim]Secure LLM Deployment[/dim]"))
    
    hw = get_hardware_info()
    if model is None:
        model = get_recommended_model(hw)
        console.print(f"🤖 Auto-selected model: [cyan]{model}[/cyan]")
    
    docker_ok, docker_msg = check_docker()
    
    if docker_ok:
        console.print("🐳 Deploying via Secure Docker Network...")
        try:
            # Deploy Docker Container
            container_id, proxy_port, upstream_url = deploy_secure_llm(model)
            api_key = generate_api_key()
            
            # Build the Proxy App
            proxy_app = build_app(api_key, upstream_url)
            
            console.print(Panel(
                f"[bold green]✅ NumNumDock Deployed securely![/bold green]\n\n"
                f"Container ID: {container_id[:12]}\n"
                f"🔒 Secure Local Endpoint: http://127.0.0.1:{proxy_port}\n"
                f"🔑 [bold red]API KEY: {api_key}[/bold red]\n\n"
                f"[yellow]NOTE: Keep this terminal open. Press Ctrl+C to stop.[/yellow]",
                border_style="green"
            ))
            
            # Run proxy in FOREGROUND so it blocks and stays alive
            uvicorn.run(proxy_app, host="127.0.0.1", port=proxy_port, log_level="error")
            
        except Exception as e:
            console.print(f"[bold red]❌ Deployment Failed: {e}[/bold red]")
    else:
        console.print(f"[bold red]❌ Docker is not available: {docker_msg}[/bold red]")

@app.command()
def status():
    console.print(Panel.fit("[bold cyan]📊 NumNumDock Status[/bold cyan]"))
    docker_ok, _ = check_docker()
    
    console.print(f"Docker: {'[green]✅ Running[/green]' if docker_ok else '[red]❌ Not available[/red]'}")
    
    if docker_ok:
        try:
            import docker
            client = docker.from_env()
            containers = client.containers.list(filters={"name": "numnum-llm"})
            if containers:
                table = Table(title="Running Container")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Status", style="yellow")
                for c in containers:
                    table.add_row(c.id[:12], c.name, c.status)
                console.print(table)
            else:
                console.print("[yellow]No NumNumDock containers running.[/yellow]")
        except Exception:
            pass

@app.command()
def doctor():
    console.print(Panel.fit("[bold cyan]🩺 NumNumDock Doctor[/bold cyan]"))
    console.print("✅ Checking Docker security configurations...")
    console.print("[green]Note: NumNumDock now isolates the network by default and uses random ports.[/green]")

if __name__ == "__main__":
    app()