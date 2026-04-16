# ============================================================
#  Topic 5: Virtual Environments
#  This file explains venv, pip, requirements.txt in detail.
#  Run commands in your terminal (not as Python script).
# ============================================================

"""
╔══════════════════════════════════════════════════════════╗
║         PYTHON VIRTUAL ENVIRONMENTS — FULL GUIDE         ║
╚══════════════════════════════════════════════════════════╝

WHY VIRTUAL ENVIRONMENTS?
──────────────────────────
Without venv, all packages install globally.
Problems:
  • Project A needs requests==2.25, Project B needs requests==2.31
  • Installing for one breaks the other
  • You can't share exact dependencies easily

Solution: Each project gets its OWN isolated Python + packages.


══════════════════════════════════════════════════════════════
  STEP 1 — CREATE A VIRTUAL ENVIRONMENT
══════════════════════════════════════════════════════════════

# Navigate to your project folder
  cd my_project

# Create virtual environment (named 'venv' by convention)
  python -m venv venv

# What this creates:
  my_project/
  └── venv/
      ├── bin/       (Linux/Mac) → python, pip executables
      ├── Scripts/   (Windows)   → python.exe, pip.exe
      ├── lib/                   → installed packages go here
      └── pyvenv.cfg             → config file


══════════════════════════════════════════════════════════════
  STEP 2 — ACTIVATE THE VIRTUAL ENVIRONMENT
══════════════════════════════════════════════════════════════

# Windows (Command Prompt):
  venv\\Scripts\\activate

# Windows (PowerShell):
  venv\\Scripts\\Activate.ps1

# Linux / Mac:
  source venv/bin/activate

# After activation, your prompt changes:
  (venv) PS C:\\my_project>       ← Windows
  (venv) alice@pc:~/my_project$   ← Linux/Mac

# Verify you're using the venv Python:
  python --version
  which python       (Linux/Mac)
  where python       (Windows)


══════════════════════════════════════════════════════════════
  STEP 3 — INSTALL PACKAGES
══════════════════════════════════════════════════════════════

# Install a package
  pip install requests

# Install specific version
  pip install requests==2.31.0

# Install multiple packages
  pip install flask pandas numpy matplotlib

# Install from requirements.txt
  pip install -r requirements.txt

# List installed packages
  pip list

# See info about a specific package
  pip show requests


══════════════════════════════════════════════════════════════
  STEP 4 — SAVE & SHARE DEPENDENCIES
══════════════════════════════════════════════════════════════

# Save current packages to requirements.txt
  pip freeze > requirements.txt

# requirements.txt looks like:
  Flask==3.0.0
  pandas==2.1.0
  numpy==1.26.0
  requests==2.31.0
  Werkzeug==3.0.1

# Someone else clones your repo and runs:
  python -m venv venv
  source venv/bin/activate       (or venv\\Scripts\\activate)
  pip install -r requirements.txt
  # → They get exactly the same environment!


══════════════════════════════════════════════════════════════
  STEP 5 — DEACTIVATE
══════════════════════════════════════════════════════════════

# Deactivate when done
  deactivate

# Your prompt returns to normal


══════════════════════════════════════════════════════════════
  .gitignore — NEVER commit your venv folder!
══════════════════════════════════════════════════════════════

# Add this to .gitignore:
  venv/
  __pycache__/
  *.pyc
  *.pyo
  .env
  *.egg-info/
  dist/
  build/


══════════════════════════════════════════════════════════════
  COMMON COMMANDS CHEAT SHEET
══════════════════════════════════════════════════════════════

  python -m venv venv              Create venv
  source venv/bin/activate         Activate (Mac/Linux)
  venv\\Scripts\\activate            Activate (Windows)
  deactivate                       Deactivate
  pip install <package>            Install package
  pip install -r requirements.txt  Install from file
  pip freeze > requirements.txt    Save all packages
  pip list                         List installed packages
  pip uninstall <package>          Remove a package
  pip show <package>               Package info


══════════════════════════════════════════════════════════════
  ALTERNATIVE: pipenv (more modern)
══════════════════════════════════════════════════════════════

  pip install pipenv

  pipenv install requests          Install & create venv
  pipenv shell                     Activate venv
  pipenv install --dev pytest      Install dev dependency
  pipenv lock                      Lock dependencies (like freeze)
  Pipfile and Pipfile.lock → equivalent of requirements.txt

"""

# ── Python code to demonstrate venv concepts ──────────────

import sys
import os

print("=" * 55)
print("  VIRTUAL ENVIRONMENT INFO (current Python)")
print("=" * 55)

print(f"\n  Python executable : {sys.executable}")
print(f"  Python version    : {sys.version[:6]}")
print(f"  Running in venv   : {'venv' in sys.prefix.lower() or 'env' in sys.prefix.lower()}")
print(f"  sys.prefix        : {sys.prefix}")

# Check if venv is active
in_venv = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
)
print(f"  venv active       : {in_venv}")

print(f"\n  Installed packages:")
try:
    import pkg_resources
    packages = sorted([(p.project_name, p.version) for p in pkg_resources.working_set])
    for name, version in packages[:10]:
        print(f"    {name:<25} {version}")
    if len(packages) > 10:
        print(f"    ... and {len(packages)-10} more")
except Exception:
    print("    Run: pip list")

print(f"""
  ─────────────────────────────────────────
  Quick start for YOUR project:

    mkdir my_project && cd my_project
    python -m venv venv
    source venv/bin/activate   # or venv\\Scripts\\activate on Windows
    pip install flask pandas
    pip freeze > requirements.txt
    echo "venv/" >> .gitignore
  ─────────────────────────────────────────
""")
