# Version

### configs: v1

* task3-v1 - enable `route-policy SID(8)` to apply SID under `bgp` configurations on all routers except RR-1 & RR-2

### configs: v2 (TBC) - workaround for issue with BGP-LU label

* task1-v2: need to enable LDP all routers (except RR-1 & RR-2)

```
mpls ldp
group CCIE-ISIS
router isis '.*'
!
interface 'GigabitEthernet.*'
point-to-point
address-family ipv4 unicast
metric 100 level 2
mpls ldp sync level 2
!
address-family ipv6 unicast
metric 200 level 2
mpls ldp sync level 2
!
```

## Startup
### alpha-v1.yaml
* adding RR-1 with IOS-XR

---
# Task Automation

This repo contains automation scripts to configure Cisco devices and collect verification outputs as part of taREMOVEDbased workflows (e.g., TaREMOVED1, TaREMOVED2B)

## Directory Structure

```
configs/
├── devices.yaml              # Device inventory (name, platform, IP, credentials)
├── taREMOVED1/                   # Folder for a specific task
│   ├── A-P-1.txt             # Config file for device A-P-1
│   ├── A-P-2.txt             # Config file for device A-P-2
│   ├── logs/                 # Output logs from config push
│   │   ├── A-P-1.log
│   │   └── A-P-2.log
│   ├── show_cmds.ini         # Show command definitions (platform- and device-specific)
│   └── show_logs/            # Output logs from show command collection
│       ├── A-P-1.log
│       └── A-P-2.log
```

---

## Script: `push_cli_configs.py`

Pushes configuration commands from `taREMOVEDx/*.txt` files into routers listed in `devices.yaml`.

### Usage:

```bash
python3 push_cli_configs.py --task taREMOVED1
```

* The config files (for each device with `{device_name}.txt`) for each task must be within respective task directory.

### Optional Flags:
- `--no-commit`: Disable automatic `commit` for IOS-XR devices

### Behavior:
- Skips routers not present in the task folder
- Automatically appends `commit` to IOS-XR configs unless `--no-commit` is used
- Logs the output per device to: `taREMOVEDx/logs/{device}.log`

---

## Script: `run_show_commands.py`

Connects to each configured device and runs appropriate `show` commands, then logs the output.

### Usage-1: for all devices in `taREMOVEDx` directory

```bash
python3 run_show_commands.py --task taREMOVED1
```

### Usage-2: run show commands for few devices only

```bash
python3 run_show_commands.py --task misc --devices A-P-1 A-P-2
```

### Command Definition Format: `show_cmds.ini`
```ini
[common_IOS]
show version
show ip route

[common_IOSXR]
show version
show isis neighbors

[A-P-1]
show run router isis
```

### Behavior:
- Executes `[common_IOS]` or `[common_IOSXR]` depending on platform
- Appends commands from a `[device]` section if it exists
- Saves each device's output to: `taREMOVEDx/show_logs/{device}.log`

---

## Requirements
- Python 3.x
- `netmiko` and `pyyaml`

```bash
pip3 install netmiko pyyaml
```

---

## Summary
| Script                | Purpose                          | Output Location             |
|----------------------|----------------------------------|-----------------------------|
| `push_cli_configs.py`| Push config to devices           | `taREMOVEDx/logs/{device}.log`  |
| `run_show_commands.py`| Collect show command output      | `taREMOVEDx/show_logs/{device}.log` |

