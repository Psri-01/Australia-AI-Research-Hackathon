import os
import urllib.request
import sys

REPO_URL = "https://raw.githubusercontent.com/Psri-01/Australia-AI-Research-Hackathon/main"
FILES = ["main.py", "graph.py", "utils.py", "requirements.txt"]
HOOK_DIR = ".git/hooks"

def install():
    print("✨ Installing Vibe Refinery...")
    
    # 1. Create hidden dir for the tool
    install_dir = ".vibe_refinery"
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)
    
    # 2. Download files
    for file in FILES:
        url = f"{REPO_URL}/{file}"
        print(f"⬇️ Downloading {file}...")
        try:
            urllib.request.urlretrieve(url, f"{install_dir}/{file}")
        except Exception as e:
            print(f"❌ Error downloading {file}: {e}")
            return

    # 3. Install Deps
    print("📦 Installing dependencies...")
    os.system(f"{sys.executable} -m pip install -r {install_dir}/requirements.txt")

    # 4. Create Git Hook (Sanitized for Windows Git Bash)
    hook_path = f"{HOOK_DIR}/pre-commit"
    
    # FIX: Convert backslashes to forward slashes
    python_exe = sys.executable.replace('\\', '/')
    script_path = os.path.abspath(f"{install_dir}/main.py").replace('\\', '/')

    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(f"#!/bin/sh\n")
        f.write(f"echo '🤖 Running Vibe Refinery...'\n")
        f.write(f'"{python_exe}" "{script_path}"\n')
    
    # Make executable (Linux/Mac)
    if os.name != 'nt':
        os.system(f"chmod +x {hook_path}")

    print("✅ Installed! Run 'git commit' to see it in action.")

if __name__ == "__main__":
    install()