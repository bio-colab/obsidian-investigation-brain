from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional


def run_skill_audit(vault: Path, audit_script: Path) -> Optional[dict[str, Any]]:
    """Run skill scripts/audit_vault.py --json and return parsed result."""
    vault = Path(vault)
    audit_script = Path(audit_script)
    if not audit_script.is_file():
        return None
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "audit.json"
        cmd = [sys.executable, str(audit_script), str(vault), "--json", str(out)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except Exception as e:
            return {"error": str(e), "issues": []}
        if out.is_file():
            try:
                return json.loads(out.read_text(encoding="utf-8"))
            except Exception as e:
                return {"error": f"json parse: {e}", "issues": [], "stderr": proc.stderr}
        return {
            "error": "no json produced",
            "returncode": proc.returncode,
            "stderr": proc.stderr[-2000:] if proc.stderr else "",
            "issues": [],
        }
