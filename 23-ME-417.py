import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import os
import difflib
import re

# =========================
# 🔐 ENV
# =========================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# =========================
# 🎓 UI & CUSTOM COLOR THEME
# =========================
st.set_page_config(page_title="RCET Mechanical AI", layout="centered")

# 🎨 CUSTOM CSS FOR BACKGROUND IMAGE & STYLING
custom_css = """
<style>
/* 1. App Background Image with Transparency/Fade Overlay */
.stApp {
    /* 👇 Added linear-gradient to fade/reduce the intensity of the background image 👇 */
    /* 👇 JUST PASTE YOUR IMAGE LINK INSIDE THE QUOTES BELOW 👇 */
    background-image: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url("data:image/jpeg;base64,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");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* 2. Semi-transparent content box so text is readable over the image */
.block-container {
    background-color: rgba(255, 255, 255, 0.88) !important; /* 88% opaque white */
    padding: 2rem !important;
    border-radius: 15px;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
    /* 👇 These properties use Flexbox to center everything vertically 👇 */
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 85vh; 
    margin-top: auto;
    margin-bottom: auto;
}

/* 3. Colorful Gradient Title */
h1 {
    background: linear-gradient(to right, #FF512F, #DD2476, #3498DB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 900 !important;
    font-size: 2.8em !important;
    padding-bottom: 20px;
}

/* 4. Colorful Input Label */
label {
    color: #E67E22 !important; /* Vibrant Orange */
    font-weight: bold !important;
    font-size: 1.2em !important;
}

/* 5. Colorful Input Box */
.stTextInput input {
    background-color: #F9EBEA !important; /* Very light red/pink background */
    color: #8E44AD !important; /* Purple text when typing */
    border: 2px solid #3498DB !important; /* Blue border */
    border-radius: 8px;
    font-weight: bold;
}

/* 6. Custom colors for the Question blocks */
.question-box {
    color: #C0392B !important; /* Deep Red for questions */
    font-weight: 800;
    font-size: 1.2em;
    margin-top: 15px;
    margin-bottom: 5px;
}

/* 7. Standard text color for readability */
p, li {
    color: #2C3E50 !important; /* Dark Slate Blue */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1>⚙️ RCET Mechanical AI</h1>", unsafe_allow_html=True)

# =========================
# 👨‍🏫 FACULTY + LAB
# =========================
faculty = {
    "salman": "Prof. Dr. Muhammad Salman Abbasi\nAssociate Professor (Chairman)\nPhD: SKKU Korea\nResearch: Heat Transfer, CFD, COMSOL\nTeaching: Thermodynamics-II, Fluid Mechanics-I & II, RAC",
    "qasim": "Dr. Qasim Ali Ranjha\nAssistant Professor\nPhD USA (Fulbright Scholar)\nResearch: Thermal Systems, CFD\nTeaching: Engineering Mechanics, CFD, FEA",
    "ali akbar": "Dr. Ali Akbar\nLecturer\nPhD Korea\nResearch: Fuel Cells\nTeaching: Mechanics of Materials, Machine Design",
    "tariq": "Dr. Tariq Nawaz\nAssistant Professor\nPhD UK\nResearch: CFD, Turbines\nTeaching: Thermodynamics, Power Plants",
    "anas": "Dr. Anas Rao\nAssistant Professor\nPhD Tsinghua\nResearch: Hydrogen Engines, AI\nTeaching: Power Plants, IC Engines",
    "aaqib": "Engr. Aaqib Imdad\nLecturer\nMSc Thermal Power\nTeaching: HVAC, Fluid Mechanics",
    "kashif": "Engr. Kashif Jamil\nLecturer\nMS Thermal Power\nTeaching: Thermodynamics Lab, Machine Design",
    "mushtaq": "Engr. Mushtaq Ahmad\nAssistant Professor\nTeaching: TQM, Mechanics of Materials",
    "suleman": "Engr. Hafiz Suleman\nLecturer\nMSc Automotive\nTeaching: Energy Resources, Thermodynamics",
    "marium": "Engr. Marium Hameed\nTeaching Assistant\nMSc Automotive (Completed)",
    "waleed": "Waleed Raza - Lab Attendant",
    "naeem": "Naeem - Lab Attendant",
    "aziz": "Aziz Shah - Lab Attendant",
    "waqas": "Waqas - Lab Attendant",
    "ijaz": "Ijaz - Lab Attendant",
    "usman": "Usman - Lab Attendant"
}

# =========================
# 📚 SEMESTER DATA
# =========================
semesters = {
    "semester 1": [("HU-111L", "Communication Skills", "0+1.0", "None"), ("MA-113", "Calculus and Analytic Geometry", "3.0+0", "None"), ("CS-103", "Programming for Data Science", "2.0+1.0", "None"), ("ME-111", "Thermodynamics-I", "3.0+1.0", "None"), ("ME-121(22)", "Engineering Graphics & Drawing", "1.0+1.0", "None"), ("QT-101", "Translation of the Holy Quran - I", "1.0+0", "None"), ("ME-123(22)", "Engineering Mechanics-I", "2.0+0", "None"), ("PHY-119", "Engineering Physics", "2.0+0", "None"), ("ME-122", "Engineering Graphics", "2.0+0", "None"), ("SE-101", "Social Ethics-I", "1.0+0", "None")],
    "semester 2": [("ME-131(22)", "Materials and Manufacturing-I", "3.0+1.0", "None"), ("MA-225", "Differential Equations and Transforms", "3.0+0", "None"), ("IS-101", "Islamic & Pakistan Studies-I", "3.0+0", "None"), ("ME-100L", "Workshop Practice", "0+1.0", "None"), ("HU-221L", "Technical Writing & Presentation Skills", "0+1.0", "None"), ("ME-124(22)", "Engineering Mechanics-II", "2.0+0", "None"), ("ME-122(22)L", "Engineering Mechanics", "0+1.0", "None"), ("EE-101(22)", "Electrical Engineering and Electronics", "2.0+1.0", "None")],
    "semester 3": [("ME-221", "Mechanics of Materials-I", "3.0+1.0", "None"), ("IS-201", "Islamic & Pakistan Studies-II", "3.0+0", "None"), ("QT-201", "Translation of the Holy Quran - II", "1.0+0", "None"), ("HU-003", "International Language", "0.0+0", "None"), ("ME-251L", "Computer Aided Drawing", "0+1.0", "None"), ("ME-231(22)", "Materials and Manufacturing-II", "2.0+1.0", "ME-131(22) Materials and Manufacturing-I"), ("ME-211(22)", "Fluid Mechanics-I", "3.0+1.0", "None"), ("SE-201", "Social Ethics-II", "1.0+0", "None")],
    "semester 4": [("ME-212", "Thermodynamics-II", "3.0+1.0", "ME-111 Thermodynamics-I"), ("ME-222", "Mechanics of Materials-II", "3.0+1.0", "ME-221 Mechanics of Materials-I"), ("ME-272", "Engineering Project Management", "2.0+0", "None"), ("ME-273", "Engineering Entrepreneurship", "1.0+1.0", "None"), ("MA-241", "Applied Engineering Statistics", "2.0+0", "None"), ("ME-213(22)", "Fluid Mechanics-II", "3.0+1.0", "ME-211(22) Fluid Mechanics-I")],
    "semester 5": [("ME-381", "Health Safety and Industrial Env", "2.0+0", "None"), ("ME-321(22)", "Mechanics of Machines", "3.0+1.0", "None"), ("ME-312(22)", "Heat and Mass Transfer", "2.0+1.0", "None"), ("ME-341(22)", "Instrumentation and Control", "2.0+0", "None"), ("ME-322(22)", "Machine Design-I", "3.0+0", "None"), ("QT-301", "Translation of the Holy Quran - III", "1.0+0", "None"), ("ME-351L", "Computer Aided Design-I", "0+1.0", "None"), ("ME-399L", "Semester Design Project", "0+1.0", "None"), ("SE-301", "Social Ethics-III", "1.0+0", "None")],
    "semester 6": [("ME-332", "Metrology and Quality Assurance", "2.0+0", "MA-241 Applied Engineering Statistics"), ("ME-371", "Professional Ethics in Engineering", "2.0+0", "None"), ("ME-353", "Computational Engineering-I", "2.0+1.0", "None"), ("ME-382", "Engineering Data Analytics & AI", "2.0+1.0", "None"), ("ME-352L", "Computer Aided Design-II", "0+1.0", "None"), ("ME-342", "Robotics and Automation", "2.0+1.0", "ME-341(22) Instrumentation and Control"), ("ME-361(22)", "Energy Resources and Utilization", "2.0+0", "None"), ("ME-323(22)", "Machine Design-II", "2.0+0", "ME-322(22) Machine Design-I")],
    "semester 7": [("ME-496L", "FYDP-I", "0+3.0", "None")],
    "semester 8": [("ME-412(22)", "Refrigeration and Air Conditioning", "2.0+1.0", "ME-312(22) Heat and Mass Transfer"), ("ME-421(22)", "Mechanical Vibrations", "3.0+1.0", "ME-321(22) Mechanics of Machines"), ("ME-415(22)", "Power Plants Engineering", "2.0+0", "ME-212 Thermodynamics-II"), ("ME-424", "Advanced Mechanics of Materials", "2.0+0", "ME-222 Mechanics of Materials-II"), ("ME-472", "Supply Chain Management", "2.0+0", "None"), ("ME-464L", "Energy & Power Systems", "0+1.0", "None"), ("ME-497L", "FYDP-II", "0+3.0", "ME-496L FYDP-I")]
}

# =========================
# ⚡ SMART SEARCH SYSTEM
# =========================
def normalize_query(q):
    phrase_corrections = {
        "pre re": "prereq", "pre req": "prereq", "pre-req": "prereq", "prerequisite": "prereq",
        "cr hr": "credit", "credit hours": "credit", "credit hour": "credit",
        "md 1": "machine design-i", "md-1": "machine design-i", "md i": "machine design-i", "md-i": "machine design-i", "md1": "machine design-i",
        "md 2": "machine design-ii", "md-2": "machine design-ii", "md ii": "machine design-ii", "md-ii": "machine design-ii", "md2": "machine design-ii",
        "machine design 1": "machine design-i", "machine design 2": "machine design-ii",
        "machine design i": "machine design-i", "machine design ii": "machine design-ii",
        "fm 1": "fluid mechanics-i", "fm-1": "fluid mechanics-i", "fm i": "fluid mechanics-i", "fm1": "fluid mechanics-i",
        "fm 2": "fluid mechanics-ii", "fm-2": "fluid mechanics-ii", "fm ii": "fluid mechanics-ii", "fm2": "fluid mechanics-ii"
    }
    for typo, correct in phrase_corrections.items():
        q = q.replace(typo, correct)
        
    word_corrections = {
        "smester": "semester", "semster": "semester", "smstr": "semester", "sem": "semester",
        "crdit": "credit", "subjec": "subject",
        "waled": "waleed", "slman": "salman", "qasm": "qasim"
    }
    q = " ".join([word_corrections.get(w, w) for w in q.split()])
    return q

def calculate_credits(ch_string):
    try: return sum(float(x) for x in ch_string.split('+'))
    except: return 0.0

def fast_answer(q):
    q_clean = normalize_query(q.lower().strip())
    words = q_clean.replace("?", "").replace(".", "").split()
    
    if ("how many" in q_clean or "total" in q_clean) and ("subject" in q_clean or "course" in q_clean) and ("4" in q_clean or "year" in q_clean):
        total_subjects = sum(len(courses) for courses in semesters.values())
        return (True, f"🔢 There are a total of **{total_subjects} subjects** in the degree.")

    if "credit" in q_clean and "semester" in q_clean:
        sem_num = re.search(r'[1-8]', q_clean)
        if sem_num:
            i = sem_num.group()
            sem_key = f"semester {i}"
            total_credits = sum(calculate_credits(ch) for code, name, ch, req in semesters[sem_key])
            return (True, f"🕒 Semester {i} has **{total_credits} Credit Hours**.")

    if "prereq" in q_clean:
        target = q_clean.replace("prereq", "").replace("of", "").replace("for", "").replace("the", "").replace("is", "").replace("what", "").replace("?", "").strip()
        best_match = None
        highest_ratio = 0.0
        
        for sem in semesters:
            for code, name, ch, req in semesters[sem]:
                if target == code.lower():
                    return (True, f"📘 Prerequisite for **{code} ({name})** is: {req}")
                
                ratio = difflib.SequenceMatcher(None, target, name.lower()).ratio()
                if target in name.lower() and len(target) > 3:
                    ratio += 0.5 
                    
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = (code, name, req)

        if best_match and highest_ratio > 0.6: 
            code, name, req = best_match
            return (True, f"📘 Prerequisite for **{code} ({name})** is: {req}")

    if "semester" in q_clean and "credit" not in q_clean:
        sem_num = re.search(r'[1-8]', q_clean)
        if sem_num:
            i = sem_num.group()
            sem_key = f"semester {i}"
            result = f"📚 **{sem_key.title()} Subjects:**\n\n"
            for code, name, ch, req in semesters[sem_key]:
                result += f"- **{code}**: {name} | Cr: {ch}\n"
            return (True, result)

    contexts = []
    
    if "faculty" in q_clean or "teachers" in q_clean or "dr" in words or "professors" in q_clean:
        all_fac = "\n".join(faculty.values())
        contexts.append(f"RCET Faculty List:\n{all_fac}")
    else:
        faculty_keys = list(faculty.keys())
        ignore_words = ["what", "who", "how", "many", "this", "that", "the", "engr", "prof", "tell", "about", "some"]
        for word in words:
            if len(word) > 3 and word not in ignore_words:
                matches = difflib.get_close_matches(word, faculty_keys, n=1, cutoff=0.75)
                if matches and faculty[matches[0]] not in contexts:
                    contexts.append(faculty[matches[0]])

    target = q_clean.replace("?", "").replace(".", "").strip()
    best_course_match = None
    highest_course_ratio = 0.0

    for sem in semesters:
        for code, name, ch, req in semesters[sem]:
            if code.lower() == target:
                contexts.append(f"Course: {code} - {name} | Credits: {ch} | Semester: {sem.title()} | Prerequisite: {req}")
                continue
            
            ratio = difflib.SequenceMatcher(None, target, name.lower()).ratio()
            if target in name.lower() and len(target) > 3:
                ratio += 0.5
                
            if ratio > highest_course_ratio:
                highest_course_ratio = ratio
                best_course_match = f"Course: {code} - {name} | Credits: {ch} | Semester: {sem.title()} | Prerequisite: {req}"

    if best_course_match and highest_course_ratio > 0.65:
        if best_course_match not in contexts:
            contexts.append(best_course_match)

    all_context = "\n\n".join(contexts)

    if all_context:
        return (False, all_context)

    return (False, None)

# =========================
# 🤖 FALLBACK AI WITH CONTEXT
# =========================
def ask_ai(q, context):
    if not client: return "⚠️ API not configured"
    
    sys_prompt = "You are a helpful, conversational AI assistant for RCET's Mechanical Engineering department. Keep answers concise and friendly."
    
    if context:
        sys_prompt += f"\n\nCRITICAL INSTRUCTION: You have been provided with specific RCET database records below. You MUST read them and answer the user's specific question NATURALLY. Do NOT just copy and paste the raw text. For example, if asked 'Is he a Dr?', read the profile and say 'No, he is an Engr/Mr.' or similar.\n\nRCET DATABASE RECORDS:\n{context}"
        
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": q}
        ]
    )
    return res.choices[0].message.content

# =========================
# 💬 CHAT
# =========================
if "chat" not in st.session_state: st.session_state.chat = []
def submit():
    q = st.session_state.input
    if q:
        is_final, data = fast_answer(q)
        
        if is_final:
            ans = data
        else:
            ans = ask_ai(q, context=data)
            
        st.session_state.chat.append((q, ans))
        st.session_state.input = ""

st.text_input("Ask anything:", key="input", on_change=submit)

st.markdown("---")

for q, a in reversed(st.session_state.chat):
    st.markdown(f'<div class="question-box">❓ Question: {q}</div>', unsafe_allow_html=True)
    st.info(a)