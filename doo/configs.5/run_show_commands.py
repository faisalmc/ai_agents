#!/usr/bin/env python3
import yaml
import os
import argparse
from datetime import datetime
from netmiko import ConnectHandler

# ---------------------------
# Parse CLI arguments
# ---------------------------
parser = argparse.ArgumentParser(
    description="Run show commands for a given task (full logs + grading logs)")
parser.add_argument(
    "--task",
    required=True,
    help="Task folder name (e.g., taREMOVED1, taREMOVED2B, misc) under configs/")
parser.add_argument(
    "--devices",
    nargs="+",
    help="Optional list of device names to include (if omitted, runs on all)")
parser.add_argument(
    "--ini",
    default=None,
    help="Alternate path to show_cmds.ini. If relative, it is resolved under the task folder."
)
parser.add_argument(
    "--out-subdir",
    default=None,
    help="Optional subfolder under the task where outputs are written (e.g., 'agent7')."
)
parser.add_argument(
    "--no-grading-logs",
    action="store_true",
    help="If set, skip writing grading_logs (only write show_logs)."
)
args = parser.parse_args()

# ---------------------------
# Directory setup
# ---------------------------
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
TASK_FOLDER  = os.path.join(BASE_DIR, args.task)
DEVICES_FILE = os.path.join(BASE_DIR, "devices.yaml")

# Resolve INI path (relative values are under the task folder)
if args.ini:
    SHOW_CMDS_FILE = args.ini if os.path.isabs(args.ini) else os.path.join(TASK_FOLDER, args.ini)
else:
    SHOW_CMDS_FILE = os.path.join(TASK_FOLDER, "show_cmds.ini")

base_out = os.path.join(TASK_FOLDER, args.out_subdir) if args.out_subdir else TASK_FOLDER
SHOW_LOGS_DIR    = os.path.join(base_out, "show_logs")
GRADING_LOGS_DIR = os.path.join(base_out, "grading_logs")
os.makedirs(SHOW_LOGS_DIR, exist_ok=True)
if not args.no_grading_logs:
    os.makedirs(GRADING_LOGS_DIR, exist_ok=True)

# ---------------------------
# Load devices.yaml
# ---------------------------
with open(DEVICES_FILE) as f:
    devices = yaml.safe_load(f)["devices"]

# ---------------------------
# Load show_cmds.ini
# ---------------------------
def load_show_commands(path):
    sections     = {}
    current_name = None
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

show_cmds = load_show_commands(SHOW_CMDS_FILE)

# ---------------------------
# Main loop
# ---------------------------
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
        print(f"Skipping {name}: unsupported platform {plat}")
        continue

    cmds = show_cmds.get(section, []) + show_cmds.get(name, [])
    if not cmds:
        print(f"Skipping {name}: no commands defined")
        continue

    grade_cmds = [c for c in cmds if not c.lower().startswith("show run")]

    cfg_file = os.path.join(TASK_FOLDER, f"{name}.txt")
    if args.task != "misc" and not os.path.isfile(cfg_file):
        print(f"Skipping {name}: missing config for task {args.task}")
        continue

    full_log  = os.path.join(SHOW_LOGS_DIR,    f"{name}.md")
    grade_log = os.path.join(GRADING_LOGS_DIR, f"{name}.md")

    print(f"Connecting to {name} ({dev.get('hostname')})…")
    try:
        params = {k: v for k, v in dev.items()
                  if k in ("host", "hostname", "username", "password", "device_type")}
        if "hostname" in params:
            params["host"] = params.pop("hostname")

        # SSH, with Telnet fallback for IOS
        try:
            conn = ConnectHandler(**params)
        except Exception:
            if plat == "cisco_ios":
                params["device_type"] = "cisco_ios_telnet"
                conn = ConnectHandler(**params)
            else:
                raise

        # Turn off paging
        conn.send_command("terminal length 0",
                          strip_prompt=False, strip_command=False)
        conn.send_command("terminal no monitor",
                          strip_prompt=False, strip_command=False)

        # Define long‑running IOS shows
        long_ios = (
            "show ip pim",
            "show ip igmp",
        )

        # --- FULL LOG ---
        with open(full_log, "w", encoding="utf-8") as lg:
            lg.write(f"# Full Output for Task {args.task}\n")
            lg.write(f"**Device:** {name} ({params['host']})\n")
            lg.write(f"_Generated: {datetime.now()}_\n\n")

            for cmd in cmds:
                lg.write(f"## {cmd}\n\n")
                verb = cmd.split()[0].lower()

                if plat == "cisco_ios":
                    conn.clear_buffer()                                           # **CHANGED FOR IOS**
                    if verb in ("ping", "traceroute") \
                       or any(cmd.startswith(pref) for pref in long_ios):       # **CHANGED FOR IOS**
                        out = conn.send_command_timing(
                            cmd,
                            strip_prompt=False,
                            strip_command=False,
                            delay_factor=2.0
                        )
                    else:
                        out = conn.send_command(
                            cmd,
                            expect_string=r"#",                                 # **CHANGED FOR IOS**
                            strip_prompt=False,
                            strip_command=False,
                            delay_factor=2.0
                        )

                elif verb in ("ping", "traceroute"):
                    out = conn.send_command_timing(
                        cmd,
                        strip_prompt=False,
                        strip_command=False,
                        delay_factor=2.0
                    )
                else:
                    out = conn.send_command(
                        cmd,
                        strip_prompt=False,
                        strip_command=False,
                        delay_factor=2.0
                    )

                lg.write(f"```\n{out.strip()}\n```\n\n")

        # --- GRADING LOG ---
        if (not args.no_grading_logs) and grade_cmds:
            with open(grade_log, "w", encoding="utf-8") as gl:
                gl.write(f"# Grading Output for Task {args.task}\n")
                gl.write(f"**Device:** {name} ({params['host']})\n")
                gl.write(f"_Generated: {datetime.now()}_\n\n")

                for cmd in grade_cmds:
                    gl.write(f"## {cmd}\n\n")
                    verb = cmd.split()[0].lower()

                    if plat == "cisco_ios":
                        conn.clear_buffer()                                       # **CHANGED FOR IOS**
                        if verb in ("ping", "traceroute") \
                           or any(cmd.startswith(pref) for pref in long_ios):   # **CHANGED FOR IOS**
                            out = conn.send_command_timing(
                                cmd,
                                strip_prompt=False,
                                strip_command=False,
                                delay_factor=2.0
                            )
                        else:
                            out = conn.send_command(
                                cmd,
                                expect_string=r"#",                             # **CHANGED FOR IOS**
                                strip_prompt=False,
                                strip_command=False,
                                delay_factor=2.0
                            )

                    elif verb in ("ping", "traceroute"):
                        out = conn.send_command_timing(
                            cmd,
                            strip_prompt=False,
                            strip_command=False,
                            delay_factor=2.0
                        )
                    else:
                        out = conn.send_command(
                            cmd,
                            strip_prompt=False,
                            strip_command=False,
                            delay_factor=2.0
                        )

                    gl.write(f"```\n{out.strip()}\n```\n\n")

        conn.disconnect()
        print(f"  full  : {full_log}")
        if not args.no_grading_logs:
            print(f"  grade : {grade_log}")

    except Exception as e:
        err = str(e)
        print(f"[ERROR] on {name}: {err}")
        error_targets = [full_log]
        if not args.no_grading_logs:
            error_targets.append(grade_log)
        for path in error_targets:
            with open(path, "w", encoding="utf-8") as lg:
                lg.write(f"# ERROR for {name}\n")
                lg.write(f"_Time: {datetime.now()}_\n\n")
                lg.write(f"```\n{err}\n```")
