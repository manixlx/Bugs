#!/usr/bin/env python3
"""Turn Semgrep JSON output into a readable HTML page and a Markdown table.

Usage:
    semgrep --config=auto src --json-output=semgrep-results.json
    python3 tools/semgrep_report.py semgrep-results.json

Creates semgrep-report.html and semgrep-report.md next to the JSON file.
Uses only the Python standard library.
"""

import html
import json
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

SEVERITY_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}
SEVERITY_LABEL = {"ERROR": "High", "WARNING": "Medium", "INFO": "Low"}


def short_rule_name(check_id):
    return check_id.rsplit(".", 1)[-1]


def read_snippet(finding):
    """Read the flagged lines from the source file (the JSON may hide them)."""
    start = finding["start"]["line"]
    end = finding["end"]["line"]
    try:
        lines = Path(finding["path"]).read_text(encoding="utf-8").splitlines()
        return "\n".join(lines[start - 1:end])
    except OSError:
        return finding.get("extra", {}).get("lines", "")


def load_findings(json_path):
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    findings = []
    for r in data.get("results", []):
        extra = r.get("extra", {})
        meta = extra.get("metadata", {})
        severity = extra.get("severity", "INFO")
        findings.append({
            "rule": short_rule_name(r["check_id"]),
            "check_id": r["check_id"],
            "path": r["path"],
            "line": r["start"]["line"],
            "severity": severity,
            "risk": SEVERITY_LABEL.get(severity, severity),
            "message": " ".join(extra.get("message", "").split()),
            "cwe": ", ".join(meta.get("cwe", [])) if isinstance(meta.get("cwe"), list) else meta.get("cwe", ""),
            "owasp": ", ".join(meta.get("owasp", [])) if isinstance(meta.get("owasp"), list) else meta.get("owasp", ""),
            "confidence": meta.get("confidence", ""),
            "snippet": read_snippet(r),
        })
    findings.sort(key=lambda f: (f["path"], SEVERITY_ORDER.get(f["severity"], 9), f["line"]))
    return findings, data.get("errors", [])


def write_markdown(findings, out_path):
    def cell(text):
        return str(text).replace("|", "\\|").replace("\n", " ")

    rows = [
        "| Finding | File | Risk | Classification | Justification | Status |",
        "|---|---|---|---|---|---|",
    ]
    for f in findings:
        finding = f["rule"] + (" (" + f["cwe"].split(":")[0] + ")" if f["cwe"] else "")
        rows.append("| {} | {} | {} | Bug / Vulnerability / Needs review / Not applicable | | |".format(
            cell(finding), cell("{}:{}".format(f["path"], f["line"])), cell(f["risk"])))
    out_path.write_text(
        "# Semgrep findings\n\n"
        "Copy this table into section 4 of the project report. "
        "Choose one classification per row and fill in the justification and status.\n\n"
        + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


def write_html(findings, errors, source_name, out_path):
    e = html.escape
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_ORDER}
    by_file = OrderedDict()
    for f in findings:
        by_file.setdefault(f["path"], []).append(f)

    sections = []
    for path, items in by_file.items():
        cards = []
        for f in items:
            details = "".join(
                "<dt>{}</dt><dd>{}</dd>".format(label, e(value))
                for label, value in (("CWE", f["cwe"]), ("OWASP", f["owasp"]),
                                     ("Confidence", f["confidence"]), ("Rule", f["check_id"]))
                if value
            )
            cards.append(
                '<article class="finding sev-{sev}">'
                '<header><span class="badge">{risk}</span>'
                '<h3>{rule}</h3><span class="loc">line {line}</span></header>'
                '<p>{message}</p><pre><code>{snippet}</code></pre><dl>{details}</dl>'
                '</article>'.format(
                    sev=e(f["severity"].lower()), risk=e(f["risk"]), rule=e(f["rule"]),
                    line=f["line"], message=e(f["message"]), snippet=e(f["snippet"]),
                    details=details))
        sections.append('<section><h2>{} <span class="count">{} finding{}</span></h2>{}</section>'.format(
            e(path), len(items), "" if len(items) == 1 else "s", "".join(cards)))

    error_note = ""
    if errors:
        error_note = '<p class="note">Semgrep reported {} error(s) while scanning. Check the terminal output.</p>'.format(len(errors))
    empty_note = ""
    if not findings:
        empty_note = '<p class="note">No findings. Remember: 0 findings does not mean the code is secure.</p>'

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semgrep Report</title>
<style>
:root {{
  --bg: #f7f7f8; --card: #ffffff; --text: #1d1d1f; --muted: #6b6b73; --border: #e2e2e6;
  --code-bg: #f0f0f3; --high: #c62828; --medium: #b26a00; --low: #1565c0;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #161618; --card: #1f1f22; --text: #ececf0; --muted: #9a9aa3; --border: #34343a;
    --code-bg: #2a2a2e; --high: #ef5350; --medium: #ffb74d; --low: #64b5f6;
  }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 24px 16px; background: var(--bg); color: var(--text);
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
main {{ max-width: 960px; margin: 0 auto; }}
h1 {{ margin: 0 0 4px; font-size: 26px; }}
.meta {{ color: var(--muted); margin: 0 0 20px; }}
.summary {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px; }}
.tile {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px;
  padding: 12px 18px; min-width: 120px; }}
.tile strong {{ display: block; font-size: 24px; }}
.tile span {{ color: var(--muted); font-size: 13px; }}
.tile.high strong {{ color: var(--high); }} .tile.medium strong {{ color: var(--medium); }}
.tile.low strong {{ color: var(--low); }}
h2 {{ font-size: 17px; font-family: ui-monospace, Menlo, Consolas, monospace; margin: 28px 0 10px; }}
.count {{ font: 13px -apple-system, sans-serif; color: var(--muted); margin-left: 6px; }}
.finding {{ background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--low);
  border-radius: 8px; padding: 14px 16px; margin-bottom: 12px; }}
.finding.sev-error {{ border-left-color: var(--high); }}
.finding.sev-warning {{ border-left-color: var(--medium); }}
.finding header {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
.finding h3 {{ margin: 0; font-size: 15px; word-break: break-word; }}
.badge {{ font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 999px; color: #fff; background: var(--low); }}
.sev-error .badge {{ background: var(--high); }} .sev-warning .badge {{ background: var(--medium); }}
.loc {{ color: var(--muted); font-size: 13px; margin-left: auto; }}
pre {{ background: var(--code-bg); border-radius: 6px; padding: 10px 12px; overflow-x: auto; margin: 10px 0; }}
code {{ font: 13px/1.45 ui-monospace, Menlo, Consolas, monospace; }}
dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 2px 12px; margin: 0; font-size: 13px; }}
dt {{ color: var(--muted); }} dd {{ margin: 0; word-break: break-word; }}
.note {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; }}
</style>
</head>
<body>
<main>
<h1>Semgrep Report</h1>
<p class="meta">Source: {source} &middot; Generated {date}</p>
<div class="summary">
  <div class="tile"><strong>{total}</strong><span>Total findings</span></div>
  <div class="tile high"><strong>{high}</strong><span>High (ERROR)</span></div>
  <div class="tile medium"><strong>{medium}</strong><span>Medium (WARNING)</span></div>
  <div class="tile low"><strong>{low}</strong><span>Low (INFO)</span></div>
  <div class="tile"><strong>{files}</strong><span>Files affected</span></div>
</div>
{error_note}{empty_note}{sections}
</main>
</body>
</html>
""".format(
        source=e(source_name), date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        total=len(findings), high=counts["ERROR"], medium=counts["WARNING"], low=counts["INFO"],
        files=len(by_file), error_note=error_note, empty_note=empty_note, sections="".join(sections))
    out_path.write_text(page, encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tools/semgrep_report.py semgrep-results.json")
        sys.exit(1)
    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print("File not found: {}".format(json_path))
        sys.exit(1)

    findings, errors = load_findings(json_path)
    html_path = json_path.with_name("semgrep-report.html")
    md_path = json_path.with_name("semgrep-report.md")
    write_html(findings, errors, json_path.name, html_path)
    write_markdown(findings, md_path)
    print("{} findings".format(len(findings)))
    print("HTML report:     {}".format(html_path))
    print("Markdown table:  {}".format(md_path))


if __name__ == "__main__":
    main()
