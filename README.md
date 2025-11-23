https://gamma.app/docs/Vibe-Refinery-jp25cumonwb0pdr

# Vibe Refinery

**Automated Technical Debt Prevention for AI-Assisted Development Teams**

Vibe Refinery is a White Box Verification Engine that transforms AI-generated code into production-ready, maintainable software. Built as a Git pre-commit hook, it automatically refactors code to CPython standards, adds engineering-grade documentation, and generates detailed change reports—ensuring that even rapidly prototyped code meets senior architect standards before it enters your repository.

## The Problem

Modern development teams are using AI to write code faster than ever, but they're shipping messy, undocumented logic with hallucinated imports and redundant patterns—technical debt on steroids. AI-generated code often passes unit tests but fails code reviews. The "Vibe Coding" trap creates codebases that are difficult to maintain, understand, and scale.

## The Solution

Vibe Refinery acts as a silent code guardian that lives where developers live: in the terminal. It intercepts code at the Git commit level and applies systematic improvements without requiring context switching or manual intervention.

**Key Features:**
- **Zero-Friction Integration**: Runs automatically as a pre-commit hook
- **Surgical Diff Analysis**: Modifies only changed lines, preserving legacy code integrity
- **Intelligent Documentation**: Adds concise inline comments tagged with `[Auto Updated]`
- **White Box Analysis**: Generates detailed reports explaining exactly what changed and why
- **Self-Protection**: Never modifies core system files
- **CPython Standards**: Ensures code adheres to Python best practices

## Architecture Overview

Vibe Refinery uses LangChain and LangGraph to create a sophisticated state machine that processes code through multiple refinement stages.

### Core Components

**graph.py - LangGraph Workflow Engine**

Defines two separate state graphs:

1. **UI Workflow** (Streamlit interface):
   - `refine_code_node`: Modernizes syntax and fixes bugs
   - `pass_through_node`: Skips refinement in "comments_only" mode
   - `add_comments_node`: Adds concise inline comments
   - `summarize_node`: Generates White Box analysis report

2. **Git Hook Workflow** (pre-commit automation):
   - `diff_commenter_node`: Analyzes git diff and adds comments only to modified lines

Both workflows use GPT-4o via Azure OpenAI (authenticated through GitHub Models API).

**main.py - Git Hook Entry Point**

Executes automatically on `git commit`:
1. Retrieves staged Python files via `git diff --cached`
2. Filters out protected system files
3. Extracts file content and diff context
4. Invokes the hook graph to add documentation
5. Performs safety checks on output
6. Re-stages modified files for commit

**utils.py - Helper Functions**
- `extract_code()`: Strips markdown formatting from LLM responses
- `generate_markdown_report()`: Compiles chat history into formatted reports

**app.py - Streamlit UI**

Interactive dashboard featuring:
- Split-pane editor with live preview
- Mode toggle: "Just Comments" vs "Fix Bugs & Refactor"
- Real-time auto-update as you type
- Documentation preview with White Box analysis
- Export functionality for complete reports

## Installation

### Quick Setup (One-Line Install)

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Psri-01/Australia-AI-Research-Hackathon/main/install.py" -OutFile "install.py"; python install.py
```

**Linux/Mac:**
```bash
curl -O https://raw.githubusercontent.com/Psri-01/Australia-AI-Research-Hackathon/main/install.py && python3 install.py
```

This bootstrapper automatically:
- Creates `.vibe_refinery/` directory
- Downloads all required files from the repository
- Installs Python dependencies
- Creates and configures the `.git/hooks/pre-commit` script
- Sets correct permissions (Linux/Mac)

### Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/Psri-01/Australia-AI-Research-Hackathon.git
cd Australia-AI-Research-Hackathon

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e .

# 4. Configure pre-commit (optional)
pre-commit install
```

## Configuration

### Authentication Setup

Vibe Refinery uses the GitHub Models API for free access to GPT-4o. Set your GitHub Personal Access Token:

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="github_pat_YOUR_TOKEN_HERE"
```

**Linux/Mac:**
```bash
export GITHUB_TOKEN="github_pat_YOUR_TOKEN_HERE"
```

To create a GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Generate new token with appropriate permissions
3. Copy the token and set it as shown above

**Important**: Add `.env` to `.gitignore` to protect your token from being committed.

## Usage

### Automatic Enhancement (Git Hook)

Once installed, Vibe Refinery runs automatically on every commit:

```bash
# 1. Write or modify Python code
echo "def calculate(x, y): return x + y" > calculator.py

# 2. Stage the file
git add calculator.py

# 3. Commit (hook runs automatically)
git commit -m "Add calculation function"
```

The system will:
- Analyze your changes
- Add inline documentation
- Tag modifications with `[Auto Updated]`
- Re-stage the enhanced file
- Complete the commit with improved code

### Interactive UI Mode

Launch the Streamlit interface for manual code refinement:

```bash
vibe-ui
```

Features:
- Write code in the left pane
- See refined output in the right pane
- Toggle between comment-only and full refactor modes
- View White Box analysis for each iteration
- Download complete documentation reports

## Code Flow Diagram

```
Developer writes code
         ↓
    git add file.py
         ↓
 git commit -m "message"
         ↓
.git/hooks/pre-commit triggers
         ↓
    main.py executes
         ↓
  git diff --cached
         ↓
  Safety check (filter system files)
         ↓
  AI Processing (LangGraph)
         ↓
  File overwrite with documentation
         ↓
   git add (re-stage)
         ↓
  Commit completes with enhanced code
```

## File Structure

```
vibe_refinery/
├── main.py                    # Git hook entry point
├── graph.py                   # LangGraph workflow definitions
├── utils.py                   # Helper functions
├── app.py                     # Streamlit UI
├── setup.py                   # Package configuration
├── install.py                 # One-line installer
├── requirements.txt           # Python dependencies
├── .pre-commit-hooks.yaml     # Pre-commit framework config
├── .env                       # Environment variables (gitignored)
├── .gitignore                 # Protected files
└── test_reverse.py            # Example test file
```

## Protected Files

The following system files are automatically excluded from modification:
- `main.py`
- `graph.py`
- `utils.py`
- `app.py`
- `setup.py`
- `install.py`

This prevents the bot from modifying itself and ensures system stability.

## Command Reference

### Git Commands

- `git add .`: Stage files for commit
- `git commit -m "message"`: Trigger automatic enhancement
- `git push`: Sync refined code to remote repository

### Package Commands

- `vibe-check`: Run Git hook manually
- `vibe-ui`: Launch Streamlit interface

## Technical Requirements

**Dependencies:**
- Python 3.8+
- streamlit
- langgraph
- langchain-openai
- python-dotenv
- tqdm

**External Requirements:**
- Git repository (requires `.git/` directory)
- GitHub Personal Access Token (for GPT-4o access)
- Active internet connection (for API calls)

## Important Notes

**GitHub Token Security**: The `.env` file contains sensitive credentials. Ensure it's listed in `.gitignore` and regenerate tokens immediately if exposed.

**Azure OpenAI Access**: This project uses GitHub Models API for free GPT-4o access, not standard OpenAI endpoints. Authentication is handled via `GITHUB_TOKEN`.

**Safety Mechanisms**: 
- Output validation ensures generated code isn't empty or drastically smaller
- System files are protected from modification
- Diff-based commenting targets only modified lines

**Git Repository Requirement**: The hook must run within a Git repository. It will not function in non-Git directories.

## Development Workflow

### For New Developers

```bash
# Clone and setup
git clone <repo-url>
cd vibe_refinery
python -m venv venv
source venv/bin/activate
pip install -e .

# Set authentication
export GITHUB_TOKEN="your_token_here"

# Test the system
echo "def test(): pass" > test.py
git add test.py
git commit -m "Test commit"
```

### Testing Changes

Use `test_reverse.py` as a reference for how the bot auto-updates code:

```bash
git add test_reverse.py
git commit -m "Test auto-documentation"
```

Check the file to see inline comments tagged with `[Auto Updated]`.

## Why Vibe Refinery?

**For Teams:**
- Maintains consistent code quality across varying skill levels
- Reduces code review burden
- Prevents technical debt accumulation
- Enables faster development without sacrificing quality

**For Individuals:**
- Learn best practices from AI-generated documentation
- Improve code readability automatically
- Build maintainable projects from day one
- Focus on logic while automation handles documentation

## Philosophy

We're not building another AI chat window. Vibe Refinery is a tool that respects legacy code, fixes only what you touch, and ensures that even if a junior developer writes the code, senior architect standards are committed to the repository. It's about turning "vibes" into engineering.

## Contributing

This project was developed during a weekend hackathon. Contributions are welcome! Please ensure:
- New features don't modify protected system files
- Tests are included for significant changes
- Documentation is updated accordingly

## License

This project is part of the Australia AI Research Hackathon submission.

## Acknowledgments

Built with:
- LangChain & LangGraph for workflow orchestration
- Azure OpenAI (via GitHub Models) for GPT-4o access
- Streamlit for interactive UI
- The Git ecosystem for seamless integration
- Gemini 3 for debugging and improvising code

---

**Remember**: This isn't just a wrapper; it's a self-healing repository that turns rapid prototypes into production-ready code, one commit at a time.
