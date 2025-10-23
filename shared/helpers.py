# shared/helpers.py
import re

def extract_cmd_output(body: str, command: str) -> str:
    """
    Extract CLI output for a specific command from a markdown log body.
    Very simple:
      - Find '## <command>' header
      - Take text until the next header
      - Grab the first ``` block in that section
    """
    if not body:
        print(f"[DEBUG extract_cmd_output] Empty body for command={command}")
        return ""

    print(f"[DEBUG extract_cmd_output] Looking for command: {command!r}")

    # Find all headers like "## show ip bgp ..."
    headers = list(re.finditer(r"(?m)^##\s*(.+?)\s*$", body))
    print(f"[DEBUG extract_cmd_output] Found {len(headers)} headers in file")

    for i, m in enumerate(headers):
        line_no = body.count("\n", 0, m.start()) + 1
        print(f"  Header[{i}] at line {line_no}: {m.group(1)!r}")

    # Find the header that exactly matches
    match_idx = None
    for i, m in enumerate(headers):
        if m.group(1).strip() == command.strip():
            match_idx = i
            break

    if match_idx is None:
        print(f"[DEBUG extract_cmd_output] No exact header match for {command!r}")
        return ""

    # Slice section from this header to next header or EOF
    start = headers[match_idx].end()
    end = headers[match_idx + 1].start() if match_idx + 1 < len(headers) else len(body)
    section = body[start:end]

    # Look for fenced block inside that section
    m_block = re.search(r"(?s)```(.*?)```", section)
    if m_block:
        snippet = m_block.group(1).strip()
        print(f"[DEBUG extract_cmd_output] Matched header {headers[match_idx].group(1)!r}, block length={len(snippet)}")
        return snippet
    else:
        print(f"[DEBUG extract_cmd_output] Matched header {headers[match_idx].group(1)!r}, but no fenced block found")
        return ""