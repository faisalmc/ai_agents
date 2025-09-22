# shared/helpers.py
import re

def extract_cmd_output(body: str, command: str) -> str:
    """
    Extract the CLI output for a specific command from a markdown log body.
    - First tries to find the section under '## <command>' with a fenced block.
    - Falls back to the last fenced block in the file.
    - Returns empty string if nothing found.
    """
    if not body:
        return ""
    pat = rf"(?mis)^##\s*{re.escape(command)}\s*\n+```(.*?)```"
    m = re.search(pat, body)
    if m:
        return m.group(1).strip()

    blocks = re.findall(r"(?s)```(.*?)```", body)
    if blocks:
        return blocks[-1].strip()

    return ""