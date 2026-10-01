# Worksheet — Lab 3.1

## Part A. Manual review

Before running Semgrep, review the project's main files.

| File | Bug? | Vulnerability? | Affected asset | Threat or impact | Proposed control |
|---|---|---|---|---|---|
| accountRoutes.js | | | | | |
| searchRoutes.js | | | | | |
| projectRoutes.js | | | | | |
| diagnosticsRoutes.js | | | | | |
| fileRoutes.js | | | | | |
| reportRoutes.js | | | | | |

## Part B. Automated scan

Run:

```bash
semgrep --config=auto src
```

| Finding | File | Rule or category | Did we find it manually? | Is it relevant? |
|---|---|---|---|---|
| | | | | |
| | | | | |

## Part C. Comparison

1. What did Semgrep find that the team had not identified?
2. What did the team find that Semgrep did not report?
3. Were there findings you consider false positives or not applicable?
4. Which finding do you consider the highest risk, and why?
5. Which control would you implement first?

## Part D. Remediation

Select at least one relevant finding.

1. Document the original code.
2. Explain the risk.
3. Implement or propose the control.
4. Run Semgrep again.
5. Keep before-and-after evidence.
