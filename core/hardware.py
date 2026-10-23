import subprocess

def get_hardware_info():
    info = {"gpu": False, "ram_gb": 8, "os": "Unknown"}
    try:
        subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        info["gpu"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        info["gpu"] = False
    return info

def get_recommended_model(hardware):
    if hardware["gpu"]:
        return "llama3.1:8b"
    else:
        return "llama3.2:1b"