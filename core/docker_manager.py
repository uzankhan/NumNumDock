import docker
import socket
import re

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def validate_model_name(model_name: str):
    if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,100}$", model_name):
        raise ValueError("Invalid model name format")

def deploy_secure_llm(model_name: str):
    validate_model_name(model_name)
    
    try:
        client = docker.from_env()
    except Exception:
        raise Exception("Docker is not running.")
    
    internal_net_name = "numnum-internal-net"
    bridge_net_name = "bridge"
    
    # 1. Create Internal Network (No Internet)
    try:
        internal_net = client.networks.create(internal_net_name, driver="bridge", internal=True)
    except docker.errors.APIError:
        internal_net = client.networks.get(internal_net_name)

    # 2. Pull Image
    client.images.pull('ollama/ollama:latest')
    
    # Cleanup old container
    try:
        client.containers.get('numnum-llm').remove(force=True)
    except:
        pass
    
    # 3. Run Container on Default Bridge first (To download model)
    container = client.containers.run(
        'ollama/ollama:latest',
        command="serve",
        network=bridge_net_name,
        detach=True,
        volumes={'numnum_data': {'bind': '/root/.ollama', 'mode': 'rw'}},
        mem_limit="8g",
        cap_drop=["ALL"],
        security_opt=["no-new-privileges"],
        name="numnum-llm",
        # GPU Support (Agar system mein GPU hai toh use karega)
        device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    )
    
    # 4. Download model securely
    print(f"Downloading model {model_name}...")
    exit_code, output = container.exec_run(["ollama", "pull", model_name])
    if exit_code != 0:
        container.remove(force=True)
        raise Exception(f"Model pull failed: {output.decode('utf-8')}")
    
    # 5. Disconnect from Internet, Connect to Internal Network
    client.networks.get(bridge_net_name).disconnect(container)
    internal_net.connect(container)
    
    # 6. Start Proxy on Host
    proxy_port = get_free_port()
    
    # Get Container IP for proxy to connect to
    container.reload()
    internal_ip = container.attrs['NetworkSettings']['Networks'][internal_net_name]['IPAddress']
    upstream_url = f"http://{internal_ip}:11434"
    
    return container.id, proxy_port, upstream_url