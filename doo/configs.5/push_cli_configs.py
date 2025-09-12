import yaml
import os
import argparse
from netmiko import ConnectHandler
from datetime import datetime

# ---------------------------
# Parse CLI arguments
# ---------------------------
parser = argparse.ArgumentParser(description="Push CLI configs to devices for a given task.")
parser.add_argument(
    "--task",
    required=True,
    help="Task folder name (e.g., taREMOVED1, taREMOVED2B) under configs/",
)
parser.add_argument(
    "--no-commit",
    action="store_true",
    help="Disable automatic 'commit' for IOS-XR devices",
)
args = parser.parse_args()

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICES_FILE = os.path.join(BASE_DIR, "devices.yaml")
TASK_FOLDER = os.path.join(BASE_DIR, args.task)
LOGS_DIR = os.path.join(TASK_FOLDER, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# ---------------------------
# Load device inventory
# ---------------------------
with open(DEVICES_FILE) as f:
    devices_data = yaml.safe_load(f)["devices"]

# ---------------------------
# Loop through devices
# ---------------------------
for device in devices_data:
    name = device["name"]
    config_file = os.path.join(TASK_FOLDER, f"{name}.txt")
    log_file = os.path.join(LOGS_DIR, f"{name}.log")

    if not os.path.isfile(config_file):
        print(f"[SKIP] No config found for {name} under {TASK_FOLDER}.")
        continue

    print(f"[INFO] Pushing config to {name} ({device['hostname']}) for task: {args.task}...")

    try:
        # Strip out unsupported Netmiko parameters
        netmiko_device = {
            k: v for k, v in device.items() if k in ["host", "hostname", "username", "password", "device_type"]
        }

        if "hostname" in netmiko_device:
            netmiko_device["host"] = netmiko_device.pop("hostname")

        try:
            conn = ConnectHandler(**netmiko_device)
        except Exception as ssh_error:
            if device["device_type"] == "cisco_ios":
                print(f"[WARN] SSH failed on {name}. Trying Telnet fallback...")
                netmiko_device["device_type"] = "cisco_ios_telnet"
                try:
                    conn = ConnectHandler(**netmiko_device)
                except Exception as telnet_error:
                    raise Exception(f"[FAIL] Both SSH and Telnet failed for {name}: {telnet_error}")
            else:
                raise Exception(f"[FAIL] SSH failed for {name} and Telnet not applicable: {ssh_error}")

        with open(config_file) as f:
            commands = f.read().splitlines()

        if (
            device["device_type"] == "cisco_xr"
            and not args.no_commit
            and "commit" not in [cmd.strip().lower() for cmd in commands]
        ):
            commands.append("commit")

        output = conn.send_config_set(commands)

        with open(log_file, "w") as log:
            log.write(f"--- Config Push Log for {name} ---\n")
            log.write(f"Timestamp: {datetime.now()}\n\n")
            log.write(output)

        print(f"[SUCCESS] Config pushed to {name}. Log saved to {log_file}")
        conn.disconnect()

    except Exception as e:
        error_msg = f"[ERROR] Config push failed for {name}: {e}"
        print(error_msg)
        with open(log_file, "w") as log:
            log.write(f"--- ERROR Log for {name} ---\n")
            log.write(f"Timestamp: {datetime.now()}\n\n")
            log.write(error_msg)
