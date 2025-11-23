import os
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Literal, Optional
from langchain_openai import ChatOpenAI 
from langgraph.graph import StateGraph, END
from utils import extract_code

# --- CONFIGURATION ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 

llm = ChatOpenAI(
    model="gpt-4o", 
    openai_api_key=GITHUB_TOKEN,
    openai_api_base="https://models.inference.ai.azure.com", 
    temperature=0
)

# --- UNIFIED STATE DEFINITION ---
class AgentState(TypedDict):
    original_code: str
    refined_code: Optional[str]
    final_code: str
    summary: Optional[str]
    mode: Optional[Literal["refactor", "comments_only"]]
    diff_context: Optional[str] 

# ==========================================
#  PART 1: UI AGENT NODES (Streamlit)
# ==========================================

def refine_code_node(state: AgentState):
    prompt = f"""
    You are a Senior Python Architect. Refactor the code for production.
    RULES:
    1. Modernize syntax (f-strings, type hints).
    2. Fix logical bugs.
    3. DO NOT change output format.
    4. Return ONLY code wrapped in ```python```.
    CODE: {state['original_code']}
    """
    response = llm.invoke(prompt)
    return {"refined_code": extract_code(response.content)}

def pass_through_node(state: AgentState):
    return {"refined_code": state['original_code']}

def add_comments_node(state: AgentState):
    instruction = "Do NOT change executable logic." if state['mode'] == 'comments_only' else "Ensure logic is optimized."
    prompt = f"""
    You are a Python Code Style Enforcer. Update comments to be concise.
    STRICT RULES:
    1. {instruction}
    2. NO DOCSTRINGS inside logic blocks.
    3. Limit comments to 1-2 lines.
    4. Return ONLY code wrapped in ```python```.
    CODE: {state['refined_code']}
    """
    response = llm.invoke(prompt)
    return {"final_code": extract_code(response.content)}

def summarize_node(state: AgentState):
    prompt = f"""
    You are a Technical Lead writing a 'White Box' Report.
    Analyze the diff between Original and Final code.
    OUTPUT: Markdown format with sections: Technical Context, Refactoring Logic (with code snippet), Impact Analysis, Developer Note.
    Original: {state['original_code'][:800]}
    Final: {state['final_code'][:800]}
    """
    response = llm.invoke(prompt)
    return {"summary": response.content}

# --- UI GRAPH CONSTRUCTION ---
ui_workflow = StateGraph(AgentState)
ui_workflow.add_node("refiner", refine_code_node)
ui_workflow.add_node("passthrough", pass_through_node)
ui_workflow.add_node("commenter", add_comments_node)
ui_workflow.add_node("summarizer", summarize_node)

def route_mode(state: AgentState):
    return "passthrough" if state['mode'] == "comments_only" else "refiner"

ui_workflow.set_conditional_entry_point(route_mode, {"passthrough": "passthrough", "refiner": "refiner"})
ui_workflow.add_edge("refiner", "commenter")
ui_workflow.add_edge("passthrough", "commenter")
ui_workflow.add_edge("commenter", "summarizer")
ui_workflow.add_edge("summarizer", END)

app = ui_workflow.compile()

# ==========================================
#  PART 2: GIT HOOK AGENT NODES (Pre-Commit)
# ==========================================

# --- NODE: THE DIFF AWARE BOT ---
def diff_commenter_node(state: AgentState):
    print("  --> Vibe Bot: Analyzing Diff...")
    prompt = f"""
    You are a Senior Code Review Bot. 
    A developer has modified this file. Use the GIT DIFF to identify changes.
    
    YOUR TASK:
    1. Analyze the GIT DIFF to find exactly which lines were added or modified.
    2. **UNTOUCHED CODE:** Output it exactly as is. Do NOT add comments to code that does not appear in the diff.
    3. **MODIFIED CODE:** Add concise inline comments explaining the logic.
    4. **TAGGING:** Start every NEW comment you add with `[Auto Updated]`.
    5. **Docstrings:** You may add a standard docstring to new functions, but do not prefix docstrings with the tag.

    Git Diff:
    {state['diff_context']}

    Current File Content:
    {state['original_code']}
    """
    response = llm.invoke(prompt)
    return {"final_code": extract_code(response.content)}

# --- HOOK GRAPH CONSTRUCTION ---
hook_workflow = StateGraph(AgentState)
hook_workflow.add_node("diff_bot", diff_commenter_node)
hook_workflow.set_entry_point("diff_bot")
hook_workflow.add_edge("diff_bot", END)

hook_app = hook_workflow.compile()