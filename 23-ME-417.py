import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# =========================
# 🔐 LOAD ENV FILE
# =========================
load_dotenv()

# =========================
# 🔐 GET API KEY FROM ENV
# =========================
api_key = os.getenv("groq_api_key")

# Safety check (important)
if not api_key:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

client = Groq(api_key=api_key)

# =========================
# 🎓 UI
# =========================
st.set_page_config(page_title="RCET Mechanical AI Assistant", layout="centered")

st.title("⚙️ RCET Mechanical Engineering AI Assistant")
st.caption("Ask about Engineering, Career, or Faculty Members")

# =========================
# 📚 FACULTY DATA
# =========================
faculty_data = """
Prof. Dr. Muhammad Salman Abbasi - Chairman, PhD SKKU Korea, Email: m.salman@uet.edu.pk, Research: Heat Transfer, CFD
Dr. Qasim Ali Ranjha - Assistant Professor, PhD USA, Email: qasim.ali@uet.edu.pk, Research: CFD, FEM
Dr. Ali Akbar - Lecturer, PhD Korea, Email: ali.akbar@uet.edu.pk, Research: Fuel Cells
Dr. Tariq Nawaz - Assistant Professor, PhD UK, Email: Tariq.Nawaz@uet.edu.pk, Research: CFD, Solar Energy
Dr. Anas Rao - Lecturer, PhD Tsinghua, Email: ansrao@uet.edu.pk, Research: AI, Hydrogen Engines
Mr. Mushtaq Ahmad - Assistant Professor
Mr. Muhammad Kashif Jamil - Lecturer
Engr. Aaqib Imdad - Lecturer
Engr. Hafiz Muhammad Suleman - Lecturer
"""

# =========================
# 🧠 SYSTEM PROMPT
# =========================
system_prompt = """
You are RCET Mechanical Engineering AI Assistant.

Answer:
- Engineering concepts
- Career guidance
- Faculty information

Rules:
- English only
- Simple and clear answers
"""

# =========================
# 🤖 AI FUNCTION
# =========================
def ask_ai(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Faculty Data:\n{faculty_data}\n\nQuestion:\n{question}"}
        ]
    )
    return response.choices[0].message.content

# =========================
# 💾 SESSION STATE
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# =========================
# 💬 INPUT
# =========================
def submit():
    question = st.session_state.user_input

    if question:
        answer = ask_ai(question)
        st.session_state.chat_history.append((question, answer))
        st.session_state.user_input = ""

st.text_input(
    "Ask anything (Engineering / Career / Faculty):",
    key="user_input",
    on_change=submit
)

# =========================
# 📜 CHAT HISTORY
# =========================
st.markdown("---")
st.subheader("📜 Chat History")

for q, a in reversed(st.session_state.chat_history):
    st.markdown("### ❓ Question")
    st.write(q)
    st.markdown("### 🤖 Answer")
    st.success(a)
    st.markdown("---")

st.info("Ask anything about Mechanical Engineering or Faculty 👆")