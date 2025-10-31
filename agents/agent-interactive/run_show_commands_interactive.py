#!/usr/bin/env python3
"""
run_show_commands_interactive.py
--------------------------------
Simplified variant of run_show_commands.py for Agent-Interactive.

• No task/config directories.
• Uses --ini and --out-dir as required inputs.
• Devices loaded from /app/shared/system/reference/devices.yaml.
• Writes one Markdown log per device directly into --out-dir.
• No grading_logs created.

Usage example:
python /app/agents/agent-interactive/run_show_commands_interactive.py \
  --ini <plan.ini> \
  --out-dir <incident_path>/2-analyze/2-capture/


python3 /app/agents/agent-interactive/run_show_commands_interactive.py \
    --ini /app/agents/agent-interactive/incidents/INC123/2-analyze/plan.ini \
    --out-dir /app/agents/agent-interactive/incidents/INC123/2-analyze/2-capture/
"""

import os
import yaml
import argparse
from datetime import datetime
from netmiko import ConnectHandler

# ---------------------------------------------------------------------
# Load show_cmds.ini (same parser as before)
# ---------------------------------------------------------------------
def load_show_commands(path):
    sections, current_name = {}, None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current_name = line[1:-1].strip()
                sections[current_name] = []
            elif current_name:
                sections[current_name].append(line)
    return sections


def main():
    # ---------------------------------------------------------------------
    # CLI arguments
    # ---------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Run show commands for Agent-Interactive")
    parser.add_argument("--ini", required=True, help="Absolute path to show_cmds.ini (plan.ini)")
    parser.add_argument("--out-dir", required=True, help="Absolute directory for output logs")
    parser.add_argument("--devices", nargs="+", help="Optional list of device names to include")
    args = parser.parse_args()

    SHOW_CMDS_FILE = args.ini
    OUT_DIR = args.out_dir.rstrip("/")
    DEVICES_FILE = "/app/shared/system/reference/devices.yaml"

    os.makedirs(OUT_DIR, exist_ok=True)

    # ---------------------------------------------------------------------
    # Load devices.yaml
    # ---------------------------------------------------------------------
    with open(DEVICES_FILE) as f:
        devices = yaml.safe_load(f)["devices"]


    show_cmds = load_show_commands(SHOW_CMDS_FILE)

    # ---------------------------------------------------------------------
    # Execute commands per device
    # ---------------------------------------------------------------------
    for dev in devices:
        name = dev["name"]
        if args.devices and name not in args.devices:
            continue

        plat = dev["device_type"].lower()
        if plat == "cisco_ios":
            section = "common_IOS"
        elif plat == "cisco_xr":
            section = "common_IOSXR"
        else:
            print(f"[WARN] Skipping {name}: unsupported platform {plat}")
            continue

        cmds = show_cmds.get(section, []) + show_cmds.get(name, [])
        if not cmds:
            print(f"[WARN] Skipping {name}: no commands defined")
            continue

        log_path = os.path.join(OUT_DIR, f"{name}.md")
        print(f"[INFO] Connecting to {name} ({dev.get('hostname')}) …")

        try:
            params = {k: v for k, v in dev.items()
                    if k in ("host", "hostname", "username", "password", "device_type")}
            if "hostname" in params:
                params["host"] = params.pop("hostname")

            # SSH with Telnet fallback
            try:
                conn = ConnectHandler(**params)
            except Exception:
                if plat == "cisco_ios":
                    params["device_type"] = "cisco_ios_telnet"
                    conn = ConnectHandler(**params)
                else:
                    raise

            conn.send_command("terminal length 0", strip_prompt=False, strip_command=False)
            conn.send_command("terminal no monitor", strip_prompt=False, strip_command=False)

            long_ios = ("show ip pim", "show ip igmp")

            with open(log_path, "w", encoding="utf-8") as lg:
                lg.write(f"# Show Output for {name}\n")
                lg.write(f"**Host:** {params['host']}\n")
                lg.write(f"_Generated: {datetime.now()}_\n\n")

                for cmd in cmds:
                    lg.write(f"## {cmd}\n\n")
                    verb = cmd.split()[0].lower()

                    if plat == "cisco_ios":
                        conn.clear_buffer()
                        if verb in ("ping", "traceroute") or any(cmd.startswith(pref) for pref in long_ios):
                            out = conn.send_command_timing(cmd, strip_prompt=False, strip_command=False, delay_factor=2.0)
                        else:
                            out = conn.send_command(cmd, expect_string=r"#", strip_prompt=False, strip_command=False, delay_factor=2.0)
                    elif verb in ("ping", "traceroute"):
                        out = conn.send_command_timing(cmd, strip_prompt=False, strip_command=False, delay_factor=2.0)
                    else:
                        out = conn.send_command(cmd, strip_prompt=False, strip_command=False, delay_factor=2.0)

                    lg.write(f"```\n{out.strip()}\n```\n\n")

            conn.disconnect()
            print(f"[OK] Log written → {log_path}")

        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            with open(log_path, "w", encoding="utf-8") as lg:
                lg.write(f"# ERROR for {name}\n_Time: {datetime.now()}_\n\n```\n{e}\n```")



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] run_show_commands_interactive.py crashed: {e}", flush=True)
