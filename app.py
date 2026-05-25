import streamlit as st
from qna_bot import QnABot

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QnA Bot",
    page_icon="🤖",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── App background ── */
.stApp {
    background: #0d0f14;
    color: #e8e6e1;
}

/* ── Header ── */
.qna-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.qna-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.03em;
    color: #f0ede8;
    margin: 0 0 0.3rem;
}
.qna-header p {
    font-size: 0.95rem;
    color: #7a7870;
    font-weight: 300;
    margin: 0;
    letter-spacing: 0.02em;
}
.qna-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #c8a96e;
    margin-right: 0.5rem;
    vertical-align: middle;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.85); }
}

/* ── Divider ── */
.qna-divider {
    border: none;
    border-top: 1px solid #1e2029;
    margin: 0.5rem 0 1.5rem;
}

/* ── Chat bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.75rem 0;
}
.msg-user .bubble {
    background: #c8a96e;
    color: #0d0f14;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 78%;
    font-size: 0.93rem;
    font-weight: 500;
    line-height: 1.55;
    box-shadow: 0 2px 12px rgba(200,169,110,0.2);
}
.msg-bot {
    display: flex;
    justify-content: flex-start;
    margin: 0.75rem 0;
}
.msg-bot .bubble {
    background: #161820;
    border: 1px solid #2a2c36;
    color: #e8e6e1;
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.25rem;
    max-width: 85%;
    font-size: 0.93rem;
    line-height: 1.65;
}

/* ── Answer sections inside bot bubble ── */
.answer-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 0.35rem;
}
.answer-text {
    font-size: 0.95rem;
    color: #e8e6e1;
    margin-bottom: 0.9rem;
}
.meta-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
}
.meta-pill {
    background: #1e2029;
    border: 1px solid #2e3040;
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-size: 0.78rem;
    color: #9997a0;
}
.meta-pill span {
    color: #c8a96e;
    font-weight: 600;
}
.reasoning-block {
    background: #111318;
    border-left: 2px solid #c8a96e;
    border-radius: 0 6px 6px 0;
    padding: 0.6rem 0.9rem;
    font-size: 0.85rem;
    color: #7a7870;
    font-style: italic;
    line-height: 1.6;
}

/* ── Follow-up chips ── */
.followup-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a4a5a;
    margin: 1.2rem 0 0.55rem;
}
/* Streamlit button overrides for chips */
div[data-testid="stHorizontalBlock"] .stButton > button,
.followup-btn > button {
    background: #161820 !important;
    border: 1px solid #2a2c36 !important;
    border-radius: 20px !important;
    color: #b0aeb8 !important;
    font-size: 0.83rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s ease !important;
    white-space: normal !important;
    text-align: left !important;
    line-height: 1.4 !important;
    height: auto !important;
    min-height: 38px !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover,
.followup-btn > button:hover {
    background: #1e2029 !important;
    border-color: #c8a96e !important;
    color: #c8a96e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(200,169,110,0.12) !important;
}

/* ── Chat input ── */
.stChatInput textarea {
    background: #161820 !important;
    border: 1px solid #2a2c36 !important;
    border-radius: 12px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
}
.stChatInput textarea:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 2px rgba(200,169,110,0.15) !important;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 760px; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #c8a96e !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="qna-header">
    <h1><span class="qna-dot"></span>QnA Bot</h1>
    <p>Ask anything — I'll reason through it with you</p>
</div>
<hr class="qna-divider">
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "bot" not in st.session_state:
    st.session_state.bot = QnABot()

if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {role, content, result?}

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── Helper: render a single bot result bubble ─────────────────────────────────
def render_bot_bubble(result):
    sources_badge = "✓ Cited" if result.sources_needed else "✗ None"
    st.markdown(f"""
    <div class="msg-bot">
      <div class="bubble">
        <div class="answer-label">Answer</div>
        <div class="answer-text">{result.answer}</div>
        <div class="meta-row">
          <div class="meta-pill">Confidence <span>{result.confidence}</span></div>
          <div class="meta-pill">Sources <span>{sources_badge}</span></div>
        </div>
        <div class="answer-label">Reasoning</div>
        <div class="reasoning-block">{result.reasoning}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
          <div class="bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_bot_bubble(msg["result"])

# ── Follow-up chips (from last bot message, shown above input) ────────────────
last_followups = []
for msg in reversed(st.session_state.messages):
    if msg["role"] == "assistant" and msg.get("result"):
        last_followups = msg["result"].follow_up_questions or []
        break

if last_followups:
    st.markdown('<div class="followup-label">Suggested follow-ups</div>', unsafe_allow_html=True)
    cols = st.columns(len(last_followups))
    for i, q in enumerate(last_followups):
        with cols[i]:
            if st.button(q, key=f"followup_{i}_{q[:20]}"):
                st.session_state.pending_question = q
                st.rerun()

# ── Determine which question to process ──────────────────────────────────────
user_question = st.chat_input("Ask me anything…")

question_to_ask = None
if st.session_state.pending_question:
    question_to_ask = st.session_state.pending_question
    st.session_state.pending_question = None
elif user_question:
    question_to_ask = user_question

# ── Process question ──────────────────────────────────────────────────────────
if question_to_ask:
    # Show user bubble
    st.markdown(f"""
    <div class="msg-user">
      <div class="bubble">{question_to_ask}</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": question_to_ask})

    # Bot response
    with st.spinner("Thinking…"):
        result = st.session_state.bot.ask(question_to_ask)

    render_bot_bubble(result)
    st.session_state.messages.append({"role": "assistant", "result": result, "content": result.answer})

    st.rerun()