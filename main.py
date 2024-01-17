import subprocess
import speedtest
import platform
import socket
import psutil
import uuid
import GPUtil
from screeninfo import get_monitors

def get_installed_software():
    try:
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        installed_packages = result.stdout.split('\n')[2:]
        return [package.split()[0] for package in installed_packages if package]
    except Exception as e:
        return f"Error retrieving installed software: {str(e)}"

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download()
    upload_speed = st.upload()
    return f"Download Speed: {download_speed / 10**6} Mbps, Upload Speed: {upload_speed / 10**6} Mbps"

def get_gpu_model():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].name  # Assuming there is at least one GPU
        else:
            return "No GPU detected"
    except Exception as e:
        return f"Error retrieving GPU information: {str(e)}"

def get_system_info():
    system_info = {
        "Screen Resolution": f"{psutil.cpu_count(logical=False)}x{psutil.cpu_count(logical=True)}",
        "CPU Model": platform.processor(),
        "Number of Cores": psutil.cpu_count(logical=False),
        "Number of Threads": psutil.cpu_count(logical=True),
        "GPU Model": get_gpu_model(),
        "RAM Size": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "Screen Size": get_screen_size(),
        "WiFi/Ethernet MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)]),
        "Public IP Address": get_public_ip(),
        "Windows Version": platform.version(),
    }
    return system_info

def get_public_ip():
    try:
        response = subprocess.run(['curl', 'https://ipinfo.io/ip'], capture_output=True, text=True)
        return response.stdout.strip()
    except Exception as e:
        return f"Error retrieving public IP address: {str(e)}"

def get_screen_size():
    try:
        monitors = get_monitors()
        if monitors:
            return f"{monitors[0].width}x{monitors[0].height} pixels"
        else:
            return "Screen size not available"
    except Exception as e:
        return f"Error retrieving screen size: {str(e)}"

if __name__ == "__main__":
    print("Installed Software:", get_installed_software())
    print("Internet Speed:", get_internet_speed())
    print("System Information:")
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")
