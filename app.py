import streamlit as st
from graph import app
from utils import generate_markdown_report
import time
import uuid

# Configure Streamlit page layout
st.set_page_config(layout="wide", page_title="Vibe Coder MVP")

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "final_code" not in st.session_state:
    st.session_state.final_code = ""
if "user_code" not in st.session_state:
    st.session_state.user_code = "def hello():\n    print('world')"
if "last_run_input" not in st.session_state:
    st.session_state.last_run_input = None
if "last_run_mode" not in st.session_state:
    st.session_state.last_run_mode = None

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("🎛️ Settings")
    mode = st.radio("Agent Mode:", ["Just Comments (Keep Logic)", "Fix Bugs & Refactor"])
    graph_mode = "comments_only" if mode == "Just Comments (Keep Logic)" else "refactor"
    live_updates = st.checkbox("⚡ Live Auto-Update", value=False)

# --- AGENT EXECUTION LOGIC ---
def run_agent():
    user_text = st.session_state.user_code
    
    if not user_text or not user_text.strip():
        return

    if st.session_state.last_run_input == user_text and st.session_state.last_run_mode == graph_mode:
        return

    with st.spinner(f"Agent is processing ({graph_mode})..."):
        inputs = {
            "original_code": user_text,
            "mode": graph_mode,
            "run_id": f"{int(time.time()*1000)}-{uuid.uuid4().hex[:8]}"
        }
        
        try:
            result = app.invoke(inputs)
        except Exception as exc:
            st.error(f"Agent error: {exc}")
            return

        final = result.get('final_code')
        rich_summary = result.get('summary', 'Analysis complete.') 

        if not final:
            st.warning("Agent returned no final_code.")
            return

        st.session_state.final_code = final

        # Append to Chat History
        st.session_state.messages.append({
            "role": "user", "content": user_text
        })
        st.session_state.messages.append({
            "role": "assistant", 
            "content": final,
            "summary": rich_summary 
        })

        st.session_state.last_run_input = user_text
        st.session_state.last_run_mode = graph_mode

# --- MAIN UI LAYOUT ---
st.title("⚡ Vibe Coder: Live Companion")

# Layout: Two Columns for Input/Output
col1, col2 = st.columns(2)

# LEFT COLUMN: Input Editor
with col1:
    st.subheader("📝 Input / Editor")
    text_area_callback = run_agent if live_updates else None
    
    st.text_area(
        "Write your code here:", 
        height=500,
        key="user_code",
        on_change=text_area_callback 
    )
    if not live_updates:
        if st.button("✨ Vibe Check Now"):
            run_agent()

# RIGHT COLUMN: Output Display
with col2:
    st.subheader("✅ Vibe Output")
    if st.session_state.final_code:
        st.code(st.session_state.final_code, language="python")
    else:
        st.info("Waiting for code...")

# --- DOCUMENTATION PREVIEW SECTION (Full Width) ---
st.markdown("---") # Horizontal separator
st.subheader("📄 Generated Documentation Preview")

if st.session_state.messages:
    # 1. Group messages into iterations (Pairs of User Input + Assistant Output)
    iterations = []
    for i in range(0, len(st.session_state.messages), 2):
        if i + 1 < len(st.session_state.messages):
            iterations.append(st.session_state.messages[i:i+2])
    
    # 2. Create Dropdown Options (Reverse order so latest is first)
    if iterations:
        # Create labels like "Iteration 3", "Iteration 2"...
        options = [f"Iteration {k+1}" for k in range(len(iterations))]
        options.reverse() # Latest on top
        
        selected_option = st.selectbox("Select Version to Preview:", options, index=0)
        
        # 3. Find the correct iteration data based on selection
        selected_index = int(selected_option.split(" ")[1]) - 1
        selected_msgs = iterations[selected_index]
        
        # 4. Generate Preview for ONLY the selected iteration
        # We pass just this pair to the generator so the UI is clean
        preview_report = generate_markdown_report(selected_msgs)
        
        # Render inside an expander or direct markdown container
        with st.container():
            st.markdown(preview_report)
            
        # 5. Download Button for the COMPLETE history
        st.markdown("---")
        full_report = generate_markdown_report(st.session_state.messages)
        col_dl_1, col_dl_2 = st.columns([1, 4])
        with col_dl_1:
            st.download_button(
                "📥 Download Full Report (All Iterations)", 
                full_report, 
                file_name="vibe_report.md"
            )
else:
    st.info("Run the agent to see the White Box Analysis here.")