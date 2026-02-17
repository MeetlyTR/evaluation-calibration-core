# Security Policy

## Public Repository Security

This repository is intended for public release. **No secrets, keys, or sensitive data should be committed.**

### What to Never Commit

- API keys, private keys, secrets
- Environment files (`.env`, `.env.local`, `.env.*`)
- Credentials files (`*.secrets*`, `secrets*.yaml`)
- Run artifacts (`reports/`, `*.log`)
- Private implementations (if using `_private/` hook, ensure it's gitignored)

### Git History

**⚠️ WARNING**: If this repository's git history contains secrets or sensitive data, do NOT rewrite history automatically. Instead:

1. Add this warning section (done)
2. Rotate any exposed credentials immediately
3. Consider using `git filter-branch` or BFG Repo-Cleaner only after careful review
4. Document any known exposures in this file

### .gitignore

The `.gitignore` file includes:
- `.env*`, `*.local`, `*.secrets*`
- `reports/`, `*.log`
- `eval_calibration_core/_private/` (private hook directory, if used)

### Secret Scanning

**Pre-push checks** (recommended):

- Use [gitleaks](https://github.com/gitleaks/gitleaks) or [trufflehog](https://github.com/trufflesecurity/trufflehog) to scan commits before pushing
- Example: `gitleaks detect --source . --verbose`
- Add to pre-commit hook or CI pipeline

**GitHub Security Settings**:

- Enable [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) (automatically scans for secrets in code)
- Enable [Dependabot](https://docs.github.com/en/code-security/dependabot) for dependency vulnerability alerts
- Review security alerts regularly

### Reporting Security Issues

[Add your security contact process]
