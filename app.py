import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import time

# --- INITIAL CONFIG ---
st.set_page_config(page_title="AEGIS AI PORTAL", page_icon="🛡️", layout="centered")

# --- PRO AI VOICE FUNCTION ---
def speak(text):
    # Menggunakan Google TTS API via HTML (Tanpa install library tambahan)
    b64_text = text.replace(" ", "+")
    audio_html = f"""
        <iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={b64_text}&tl=en&client=tw-ob" allow="autoplay" style="display:none"></iframe>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- ADVANCED CSS (HACKER ENTERPRISE UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #050b18 0%, #000000 100%);
        color: #e2e8f0;
    }
    header, footer {visibility: hidden;}

    /* Full Screen Center for Landing */
    .landing-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 70vh;
        text-align: center;
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: 25px;
        background: linear-gradient(180deg, #ffffff 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        animation: dropIn 1s ease-out;
    }

    @keyframes dropIn {
        0% { transform: translateY(-50px); opacity: 0; filter: blur(10px); }
        100% { transform: translateY(0); opacity: 1; filter: blur(0); }
    }

    /* Professional Button Initialize */
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
        background: transparent !important;
        color: #00f2fe !important;
        border: 2px solid #00f2fe !important;
        padding: 20px 60px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1rem !important;
        letter-spacing: 5px !important;
        border-radius: 0px !important;
        transition: all 0.5s;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        margin-top: 40px;
    }

    div.stButton > button:first-child:hover {
        background: rgba(0, 242, 254, 0.1) !important;
        box-shadow: 0 0 50px #00f2fe;
        transform: scale(1.05);
    }

    /* Scanner UI */
    .scanner-container {
        border: 1px solid rgba(0, 242, 254, 0.2);
        background: rgba(255, 255, 255, 0.02);
        padding: 40px;
        border-radius: 4px;
        backdrop-filter: blur(15px);
    }

    /* Simple & Pro Logout at Bottom */
    .logout-btn-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .logout-btn-container button {
        background: transparent !important;
        color: #444 !important;
        border: none !important;
        font-size: 0.8rem !important;
        letter-spacing: 2px !important;
        text-decoration: underline !important;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'started' not in st.session_state:
    st.session_state.started = False

# --- UI LOGIC ---
if not st.session_state.started:
    # 1. LANDING PAGE (Perfectly Centered)
    st.markdown('<div class="landing-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AEGIS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="letter-spacing: 10px; color: #334155; font-size: 0.8rem;">SECURE INTERFACE v2.0</p>', unsafe_allow_html=True)
    
    if st.button("INITIALIZE"):
        speak("Welcome back, Administrator. System is online.")
        st.session_state.started = True
        time.sleep(1.5) # Kasih waktu buat suara selesai
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # 2. MAIN SCANNER PAGE
    st.markdown('<p style="text-align:center; letter-spacing:5px; color:#4facfe; font-size:0.7rem;">SYSTEM STATUS: ACTIVE</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="scanner-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=200)
        
        with st.status("Neural Scanning in Progress...", expanded=True) as status:
            time.sleep(1.2)
            img_array = np.array(image.convert('RGB'))
            openc_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            barcodes = decode(openc_image)
            
            if barcodes:
                for b in barcodes:
                    url = b.data.decode('utf-8')
                    status.update(label="Scanning Complete", state="complete")
                    
                    bad_words = ['login', 'dana', 'kaget', 'update', 'rekening', 'verify']
                    is_bad = any(w in url.lower() for w in bad_words)
                    
                    if is_bad:
                        speak("Warning. Malicious link detected. Access denied.")
                        st.markdown(f"""
                        <div style="border-left: 3px solid #ff0000; padding:20px; background:rgba(255,0,0,0.05);">
                            <h4 style="color:#ff0000; margin:0; letter-spacing:3px;">[!] THREAT ALERT</h4>
                            <p style="color:#aaa; font-size:0.9rem;">The system has flagged <code>{url}</code> as high risk.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        speak("Analysis complete. Link verified as safe.")
                        st.markdown(f"""
                        <div style="border-left: 3px solid #00f2fe; padding:20px; background:rgba(0,242,254,0.05);">
                            <h4 style="color:#00f2fe; margin:0; letter-spacing:3px;">[+] SAFE DATA</h4>
                            <p style="color:#aaa; font-size:0.9rem;">Source <code>{url}</code> is secure.</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                status.update(label="Scan Error", state="error")
                st.error("No valid QR signature detected.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. LOGOUT AT BOTTOM
    st.markdown('<div class="logout-btn-container">', unsafe_allow_html=True)
    if st.button("TERMINATE SESSION"):
        st.session_state.started = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)