import os
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader

# -------------------------
# Argument Parsing
# -------------------------
parser = argparse.ArgumentParser(description="Generate CLI configs for a given SP and task")
parser.add_argument("--sp", required=True, help="Service Provider name (e.g. alpha, bravo, charlie)")
parser.add_argument("--taREMOVEDdir", required=True, help="Path to task directory under configs.2")
parser.add_argument("--template", required=True, help="Path to Jinja2 template file")
args = parser.parse_args()

sp_name = args.sp.lower()
task_dir = args.task_dir.rstrip("/")
template_file = args.template

# -------------------------
# Path Definitions
# -------------------------
startup_file = os.path.join("..", "startup", f"{sp_name}.yaml")
task_vars_file = os.path.join(task_dir, "taREMOVEDvars.yaml")
task_devices_file = os.path.join(task_dir, "taREMOVEDdevices.yaml")
template_dir = os.path.dirname(template_file)
template_name = os.path.basename(template_file)

# -------------------------
# Load YAMLs
# -------------------------
with open(startup_file) as f:
    startup_yaml = yaml.safe_load(f)
    sp_data = startup_yaml.get("routers", [])  # Updated to support 'routers' root

if os.path.exists(task_vars_file):
    with open(task_vars_file) as f:
        task_vars = yaml.safe_load(f)
else:
    task_vars = {}

if os.path.exists(task_devices_file):
    with open(task_devices_file) as f:
        allowed_devices = set(yaml.safe_load(f).get("devices", []))
else:
    allowed_devices = None  # If file doesn't exist, generate for all

# -------------------------
# Setup Jinja2 Environment
# -------------------------
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(template_name)

# -------------------------
# Generate Configs
# -------------------------
print(f"[INFO] Generating configs for SP: {sp_name}, taREMOVEDdir: {task_dir}, template: {template_name}")

for node in sp_data:
    if allowed_devices and node["name"] not in allowed_devices:
        print(f"[DEBUG] Skipping {node['name']} (not in taREMOVEDdevices.yaml)")
        continue  # Skip devices not in taREMOVEDdevices.yaml

    context = {**node, **task_vars}  # Pass everything to template
    output = template.render(context)

    filename = os.path.join(task_dir, f"{node['name']}.txt")
    with open(filename, "w") as f:
        f.write(output)

    print(f"[+] Generated: {filename}")
