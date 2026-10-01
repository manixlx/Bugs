# Lab 3.1 — Vulnerabilities vs Bugs

This repository simulates a small API with several modules so the analysis feels closer to a real project.

## Main rule

Do not run Semgrep at the start.

First complete the manual review described in `LAB_WORKSHEET.md`.

Then install Semgrep (see [Installing Semgrep](#installing-semgrep)) and run, from the project folder:

```bash
semgrep --config=auto src
```

Compare the human review against the findings.

## Viewing and saving the results

The terminal output is hard to read with many findings. Save the results to files instead:

```bash
semgrep --config=auto src --json-output=semgrep-results.json --sarif-output=semgrep-results.sarif --text-output=semgrep-results.txt
```

Then generate a readable report (uses only Python, no extra packages):

```bash
python3 tools/semgrep_report.py semgrep-results.json
```

This creates two files:

* `semgrep-report.html`: open it in any browser. Findings are grouped by file, with severity, code snippet, CWE and OWASP category.
* `semgrep-report.md`: a table with the same columns as section 4 of `PROJECT_SCAN_REPORT_TEMPLATE.md`, ready to paste into your report.

Other options:

* `semgrep-results.txt`: the same view as the terminal, useful as raw evidence.
* `semgrep-results.sarif`: if you use VS Code, install Microsoft's "SARIF Viewer" extension and open this file to click through each finding to its exact line of code.

For the before-and-after evidence in Part D, run the scan again after your fix and save it with different names, for example `semgrep-results-after.json`.

## Installing Semgrep

Semgrep requires Python 3.9 or newer and an internet connection (`--config=auto` downloads rules from the Semgrep registry).

### macOS

```bash
python3 -m pip install --user semgrep
```

pip installs the `semgrep` command in a folder that is not on your PATH, so running it gives `zsh: command not found: semgrep`. Fix it permanently (run once):

```bash
echo 'export PATH="$(python3 -m site --user-base)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
semgrep --version
```

If you use Homebrew, `brew install semgrep` also works and skips the PATH step.

With the Python that comes with macOS, Semgrep may print `NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+`. It is harmless and the scan still works.

### Linux

On most recent distributions (Ubuntu 23.04+, Debian 12+), `pip install` is blocked with an `externally-managed-environment` error. Use pipx instead:

```bash
sudo apt install pipx     # Debian/Ubuntu; use your distro's package manager otherwise
pipx install semgrep
pipx ensurepath
```

Close and reopen the terminal, then check with `semgrep --version`.

### Windows

The most reliable option is WSL (Windows Subsystem for Linux):

1. In PowerShell as administrator, run `wsl --install` and restart.
2. Open the Ubuntu app and follow the Linux steps above.
3. Scan the lab from inside WSL. Windows drives are available under `/mnt/c/...`, for example `cd /mnt/c/Users/<you>/cetys_unit3_semgrep_lab`.

Native Windows support (`py -m pip install semgrep` in PowerShell) is newer and may behave differently; use WSL if it gives errors.

## Main files

* `src/routes/accountRoutes.js`
* `src/routes/searchRoutes.js`
* `src/routes/projectRoutes.js`
* `src/routes/diagnosticsRoutes.js`
* `src/routes/fileRoutes.js`
* `src/routes/reportRoutes.js`

There are also reference implementations in `src/safe/`.

## Key ideas

Not every problem will be detected by Semgrep.

Not every finding is automatically a real vulnerability.

Not every functional bug is a security vulnerability.

0 findings does not mean the system is secure.
