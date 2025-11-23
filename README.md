https://gamma.app/docs/Vibe-Refinery-jp25cumonwb0pdr

Vibe Refinery: Complete Overview
Vibe Refinery is an AI-powered code review and documentation system that integrates with Git as a pre-commit hook. It uses LangChain + LangGraph to refactor code, add comments, and generate documentation.

🏗️ Architecture Overview
The project has two main workflows:

UI Agent (app.py) – Interactive Streamlit interface for live code refinement
Git Hook Agent (main.py) – Auto-runs on git commit to enhance staged files
Both workflows are defined in graph.py using LangGraph state machines.

Workflow for New Devs
# 1. Clone the repository
git clone <repo-url>
cd vibe_refinery

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install the package in development mode
pip install -e .

# 4. Configure pre-commit (optional but recommended)
pre-commit install

Use Git Hook (Auto-Enhancement)
# 1. Write/modify Python code
echo "def add(x, y): return x + y" > my_script.py

# 2. Stage the file
git add my_script.py

# 3. Commit (hook runs automatically)
git commit -m "Add math function"
# Vibe Bot automatically:
# - Adds inline comments
# - Tags changes with [Auto Updated]
# - Re-stages the modified file

⚠️ Important Notes
GitHub Token Exposure: The .env file contains a real token. Regenerate it immediately after this repository is public.
Azure OpenAI: Requires valid GITHUB_TOKEN for GPT-4o access (not standard OpenAI).
System Files Protected: The bot never modifies itself (main.py, graph.py, utils.py, app.py, setup.py, install.py).
Git Hooks: Must run in a Git repository (requires .git/ directory).

📁 File Breakdown
Core Logic Files
graph.py – LangGraph Workflow Engine
Defines two separate state graphs:

UI Workflow (for Streamlit):

refine_code_node → Modernizes syntax, fixes bugs
pass_through_node → Skips refinement if in "comments_only" mode
add_comments_node → Adds concise inline comments
summarize_node → Generates White Box analysis report
Git Hook Workflow (for pre-commit):

diff_commenter_node → Analyzes git diff and adds comments only to modified lines (tagged with [Auto Updated])
Both use GPT-4o via Azure (configured via GITHUB_TOKEN).

main.py – Git Hook Entry Point
Runs automatically on git commit:

Gets staged Python files via git diff --cached
Filters out system files (main.py, graph.py, utils.py, etc.)
Extracts file content and diff context
Invokes the hook graph to add comments
Safety check: Ensures output isn't empty or drastically smaller
Stages modified files back to Git
Key Protection: SYSTEM_FILES constant prevents the bot from modifying core files.

utils.py – Helper Functions
extract_code() → Strips markdown filler from LLM responses using regex
generate_markdown_report() → Compiles chat history into a formatted Markdown report

app.py – Streamlit UI
Interactive dashboard with:

Input Editor (left) – Write Python code
Output Display (right) – Shows refined code
Mode Toggle – "Just Comments" vs "Fix Bugs & Refactor"
Live Auto-Update – Runs agent as you type
Documentation Preview – Shows White Box analysis per iteration
Download Button – Export full report as Markdown
Session state manages messages, code history, and execution tracking.

Configuration & Setup Files
setup.py
Installs the package with two CLI commands:

vibe-check → Runs main.py as a Git hook
vibe-ui → Launches Streamlit UI
requirements.txt
Dependencies: streamlit, langgraph, langchain-openai, python-dotenv, tqdm

.pre-commit-hooks.yaml
Registers the vibe-check hook with pre-commit framework (identifies Python files, doesn't pass filenames)

.env
Stores GITHUB_TOKEN for Azure OpenAI authentication (⚠️ should be in .gitignore)

.gitignore
Protects secrets, Python caches, virtual envs, and temp files

Installation Script
One-time setup that:

Creates .vibe_refinery/ directory
Downloads files from GitHub repository
Installs dependencies via pip
Creates .git/hooks/pre-commit script (Windows-compatible with forward slashes)
Makes hook executable on Linux/Mac

test_reverse.py
Simple test file showing the bot's auto-update capability (comments tagged with [Auto Updated])
