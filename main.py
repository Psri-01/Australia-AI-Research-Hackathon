import subprocess
import sys
import os
import warnings

# Suppress warnings
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")

# Import only after suppressing warnings
from graph import hook_app 

# --- CRITICAL: DO NOT LET THE BOT TOUCH THESE FILES ---
SYSTEM_FILES = {"main.py", "graph.py", "utils.py", "app.py", "setup.py", "install.py"}

def run_command(command):
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',       
            errors='replace'        
        )
        return result.stdout.strip()
    except Exception as e:
        return None

def get_staged_files():
    output = run_command(["git", "diff", "--name-only", "--cached"])
    if not output:
        return []
    files = output.split('\n')
    # Filter out non-python files AND system files
    return [f for f in files if f.endswith('.py') and f not in SYSTEM_FILES]

def get_file_content(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def get_git_diff(filename):
    return run_command(["git", "diff", "--cached", filename])

def main():
    staged_files = get_staged_files()
    
    if not staged_files:
        sys.exit(0)

    print("Vibe Bot: Inspecting Staged Files...")

    for filename in staged_files:
        if not os.path.exists(filename):
            continue

        content = get_file_content(filename)
        diff = get_git_diff(filename)
        
        if not content or not diff:
            continue

        print(f"Analyzing changes in: {filename}")

        inputs = {
            "original_code": content,
            "diff_context": diff
        }
        
        try:
            result = hook_app.invoke(inputs)
            final_code = result.get("final_code")

            # SAFETY CHECK: 
            # 1. Must not be empty
            # 2. Must be roughly same size (prevents deletion)
            if final_code and len(final_code) > (len(content) * 0.5) and final_code != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(final_code)
                
                subprocess.run(["git", "add", filename])
                print(f"Vibe Comments Added to: {filename}")
            else:
                print(f"No updates needed (or safety check failed) for: {filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    print("Vibe Check Complete. Committing...")
    sys.exit(0)

if __name__ == "__main__":
    main()