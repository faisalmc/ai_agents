#!/usr/bin/env python3

import yaml
import subprocess
import sys
import os
import platform

# Correct path to your YAML file
DEVICE_FILE = "/home/labuser/sp-1/doo/configs.3/devices.yaml"

def load_devices(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
        if isinstance(data, dict) and "devices" in data:
            return data["devices"]
        return data  # assume it's already a list

def ping_device(ip):
    count = "1"
    cmd = ["ping", "-c", count, ip] if platform.system() != "Windows" else ["ping", "-n", count, ip]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL)
    return result.returncode == 0

def ssh_to_device(device):
    expect_script = f"""
    set timeout 10
    spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {device['username']}@{device['hostname']}
    expect {{
        "*assword:" {{
            send "{device['password']}\\r"
        }}
    }}
    interact
    """
    temp_script = "/tmp/ssh_expect_script.exp"
    with open(temp_script, "w") as f:
        f.write(expect_script)

    os.system(f"gnome-terminal -- bash -c 'expect {temp_script}; exec bash'")


def telnet_to_device(device):
    telnet_cmd = f"gnome-terminal -- bash -c 'telnet {device['hostname']}; exec bash'"
    os.system(telnet_cmd)

def connect_device(hostname, devices):
    for device in devices:
        if device["name"].lower() == hostname.lower():
            ip = device["hostname"]
            print(f"==> Connecting to {device['name']} ({ip}) via {device['device_type'].upper()}")
            if not ping_device(ip):
                print(f"✗ {device['name']} is NOT reachable.")
                return
            print(f"✓ {device['name']} is reachable.")
            if "xr" in device["device_type"].lower():
                ssh_to_device(device)
            else:
                telnet_to_device(device)
            return
    print(f"✗ Device '{hostname}' not found in devices.yaml.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 connect_devices.py <device-name>")
        sys.exit(1)

    hostname = sys.argv[1]
    devices = load_devices(DEVICE_FILE)
    connect_device(hostname, devices)
