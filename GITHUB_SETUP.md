# GroceryPOS Pro — Complete GitHub Integration Guide

This guide walks you through **every step** to put GroceryPOS Pro on GitHub,
enable CI/CD (automatic testing + Windows EXE builds), and publish releases.

---

## Step 1 — Install Git (if not already installed)

Download from: https://git-scm.com/download/win  
Install with default options. Verify:

```bash
git --version
# should show: git version 2.x.x
```

---

## Step 2 — Create a GitHub Account & Repository

1. Go to https://github.com and sign in (or create a free account)
2. Click the **"+"** button → **"New repository"**
3. Fill in:
   - **Repository name**: `grocerypos-pro`
   - **Description**: `Professional POS System for Grocery & Retail`
   - **Visibility**: Public (free CI/CD minutes) or Private
   - ❌ Do NOT check "Add README" (we already have one)
4. Click **"Create repository"**
5. Copy the repository URL shown (e.g. `https://github.com/YOUR_USERNAME/grocerypos-pro.git`)

---

## Step 3 — Push the Project to GitHub

Open Command Prompt or PowerShell in your project folder:

```bash
# 1. Go into the project folder
cd path\to\pos_system

# 2. Initialise git
git init

# 3. Set your identity (one-time setup)
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"

# 4. Add all files
git add .

# 5. First commit
git commit -m "feat: initial release of GroceryPOS Pro v2.0.0"

# 6. Rename branch to 'main' (modern standard)
git branch -M main

# 7. Connect to GitHub (replace URL with yours)
git remote add origin https://github.com/YOUR_USERNAME/grocerypos-pro.git

# 8. Push to GitHub
git push -u origin main
```

> **Tip:** If GitHub asks for credentials, use your GitHub username and a
> **Personal Access Token** (PAT) as the password — not your account password.
> Create a PAT at: https://github.com/settings/tokens → "Generate new token (classic)"
> → check "repo" scope → Generate.

---

## Step 4 — Verify GitHub Actions Started

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see **"🚀 CI/CD — Test & Build"** running automatically
4. Click it to watch the live log

The workflow will:
- Run your 69 tests on Python 3.9, 3.10, 3.11, and 3.12 simultaneously
- Pass ✅ on all four versions (or show exactly which test failed)

---

## Step 5 — Create Your First Release (Builds the .exe)

The Windows EXE is only built when you push a **version tag**.

```bash
# In your project folder:

# 1. Tag the current commit as version 2.0.0
git tag -a v2.0.0 -m "GroceryPOS Pro v2.0.0 - Initial public release"

# 2. Push the tag to GitHub
git push origin v2.0.0
```

This triggers:
1. **Tests run** on all Python versions
2. **Windows EXE is built** on `windows-latest` GitHub runner
3. **GitHub Release is created** automatically with the `.zip` attached
4. Anyone can download `GroceryPOS_Pro_v2.0.0_Windows.zip` from the Releases page

View your release at:
`https://github.com/YOUR_USERNAME/grocerypos-pro/releases`

---

## Step 6 — Day-to-Day Workflow

### Making changes and pushing:

```bash
# Edit your code...

# Stage changes
git add .

# Commit with a descriptive message
git commit -m "fix: barcode scanner focus on POS load"

# Push to GitHub (triggers tests automatically)
git push origin main
```

### Releasing a new version:

```bash
git tag -a v2.1.0 -m "v2.1.0: Added SMS notifications, fixed tax rounding"
git push origin v2.1.0
```

---

## Step 7 — Recommended Branch Strategy

```
main          ← stable, production-ready code only
  ↑ merge via PR
develop       ← integration branch, daily work
  ↑ merge via PR
feature/xyz   ← individual features
hotfix/abc    ← urgent bug fixes → merge to main + develop
```

```bash
# Create and switch to a feature branch
git checkout -b feature/sms-notifications

# Work, commit...
git add .
git commit -m "feat: add SMS notification on low stock"

# Push feature branch
git push origin feature/sms-notifications

# Then open a Pull Request on GitHub: feature/... → develop
# After review, merge to develop, then develop → main for release
```

---

## Step 8 — Protect the main Branch (Recommended)

In your GitHub repo:
1. **Settings** → **Branches** → **Add branch ruleset** (or "Add rule")
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass (select the "test" job)
   - ✅ Require branches to be up to date before merging
4. Click **Save changes**

Now nobody (including you) can push directly to `main` — all changes go through PRs, and PRs can only be merged if all 69 tests pass.

---

## Step 9 — Add Repository Secrets (Optional)

If you want to add email notifications, Slack alerts, or code signing:

1. **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret Name | Value | Purpose |
|---|---|---|
| `SLACK_WEBHOOK` | Slack webhook URL | Notify on failed builds |
| `SIGNING_CERT` | Base64 certificate | Sign the .exe (advanced) |

Reference in workflow:
```yaml
- name: Notify Slack
  run: curl -X POST ${{ secrets.SLACK_WEBHOOK }} -d '{"text":"Build failed!"}'
```

---

## Step 10 — Manual Trigger (Build EXE Without a Tag)

1. Go to **Actions** tab on GitHub
2. Click **"🚀 CI/CD — Test & Build"** in the left sidebar
3. Click **"Run workflow"** (top right)
4. Set "Build Windows EXE?" to `true`
5. Click **"Run workflow"**

The EXE will be available as a downloadable **artifact** under the workflow run
(not a full Release — just a build artifact valid for 30 days).

---

## Workflow Summary

```
You push code
    │
    ▼
GitHub Actions starts automatically
    │
    ├─► JOB 1: Tests (Python 3.9/3.10/3.11/3.12) ──► ✅ All 69 pass?
    │                                                        │
    │                                          ┌────────────┘
    │                                          │  (if tag push or manual)
    │                                          ▼
    │                                   JOB 2: Build Windows EXE
    │                                          │
    │                                          ▼
    │                                   dist/GroceryPOS_Pro/
    │                                   GroceryPOS_Pro.exe ✅
    │                                          │
    │                                   (if tag push v*)
    │                                          ▼
    └──────────────────────────────────► JOB 3: GitHub Release
                                         with .zip attached 🎉
```

---

## Files Added for GitHub Integration

```
pos_system/
├── .gitignore                           ← excludes DB, logs, backups, __pycache__
├── .github/
│   └── workflows/
│       ├── build.yml                    ← main CI/CD: test + build + release
│       └── quality.yml                  ← PR checks + nightly test matrix
├── data/.gitkeep                        ← keeps empty dir in git
├── logs/.gitkeep
├── backups/.gitkeep
├── reports/.gitkeep
└── assets/.gitkeep
```

---

## Troubleshooting GitHub Actions

### "Tests fail on GitHub but pass locally"
- GitHub uses Ubuntu; tkinter needs `sudo apt-get install python3-tk` — already in workflow ✅

### "PyInstaller build fails"
- Check the Actions log for the exact error
- Most common: missing hidden import → add to `grocerypos.spec` hiddenimports list

### "Permission denied pushing tag"
- Make sure your PAT has `repo` scope
- Or use SSH: set up SSH key at https://github.com/settings/keys

### "Release not created"
- Check the `release` job logs in Actions
- Ensure the `softprops/action-gh-release` step has `contents: write` permission (already set in workflow ✅)

### View live build logs
Go to: `https://github.com/YOUR_USERNAME/grocerypos-pro/actions`
