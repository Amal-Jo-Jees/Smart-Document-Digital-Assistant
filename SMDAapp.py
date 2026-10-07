import pypdf
import streamlit as st
from groq import Groq

# 🔑 HARDCODE YOUR GROQ API KEY HERE
GROQ_API_KEY = "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"

st.set_page_config(page_title="Zero-Download Assistant", layout="wide", page_icon="📖")
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 50% 55%, rgba(22, 42, 82, 0.5), transparent 58%),
            linear-gradient(145deg, #080d1b 0%, #10162a 52%, #080d1b 100%);
        color: #f4f7ff;
    }
    div[data-testid="stAppViewContainer"] {
        background: transparent;
        isolation: isolate;
    }
    div[data-testid="stAppViewContainer"] .main {
        position: relative;
        z-index: 1;
        background: transparent;
    }
    div[data-testid="stAppViewContainer"] .block-container {
        padding-top: 2.5rem;
    }
    h1 {
        text-align: center;
        background: linear-gradient(90deg, #f5f7ff 15%, #8deaff 52%, #d8a4ff 85%);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        filter: drop-shadow(0 0 22px rgba(91, 204, 255, 0.24));
    }
    div[data-testid="stCaptionContainer"] {
        text-align: center;
        color: #b5c4df;
    }
    [data-testid="stFileUploader"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploader"] section {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.8rem;
        min-height: 0 !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0;
        box-shadow: none !important;
        color: #d9e8fa;
        padding: 0.35rem 0 !important;
    }
    [data-testid="stFileUploaderDropzone"] *,
    [data-testid="stFileUploader"] section > div {
        background-color: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploader"] section button {
        flex: 0 0 auto;
        min-height: 2.4rem;
        padding: 0.45rem 0.85rem !important;
        border: 1px solid rgba(141, 234, 255, 0.42) !important;
        border-radius: 8px !important;
        background: rgba(141, 234, 255, 0.1) !important;
        color: #e5f4ff !important;
        transition: background 160ms ease, border-color 160ms ease,
            box-shadow 160ms ease;
    }
    [data-testid="stFileUploaderDropzone"] button:hover,
    [data-testid="stFileUploader"] section button:hover {
        background: rgba(141, 234, 255, 0.18) !important;
        border-color: rgba(141, 234, 255, 0.72) !important;
        box-shadow: 0 0 14px rgba(91, 204, 255, 0.14);
    }
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploader"] section small {
        margin: 0 !important;
        color: #9eacc4 !important;
        font-size: 0.82rem;
    }
    @media (max-width: 480px) {
        [data-testid="stFileUploaderDropzone"],
        [data-testid="stFileUploader"] section {
            flex-wrap: wrap;
            gap: 0.45rem 0.7rem;
        }
    }
    
    div[data-testid="stFileUploaderFilesContainer"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    .holographic-book {
        position: fixed;
        inset: 12vh 0 0;
        z-index: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
        opacity: 0.38;
    }
    .holographic-book svg {
        width: min(100vw, 1120px);
        height: min(78vh, 720px);
        overflow: visible;
    }
    </style>
    <div class="holographic-book" aria-hidden="true">
      <svg viewBox="0 0 1200 700" fill="none" xmlns="http://w3.org">
        <defs>
          <linearGradient id="page-left" x1="180" y1="170" x2="600" y2="540" gradientUnits="userSpaceOnUse">
            <stop stop-color="#75F6FF" stop-opacity=".2"/>
            <stop offset=".52" stop-color="#9C8BFF" stop-opacity=".1"/>
            <stop offset="1" stop-color="#54DBFF" stop-opacity=".24"/>
          </linearGradient>
          <linearGradient id="page-right" x1="600" y1="170" x2="1020" y2="540" gradientUnits="userSpaceOnUse">
            <stop stop-color="#FF85E8" stop-opacity=".18"/>
            <stop offset=".5" stop-color="#9B8DFF" stop-opacity=".12"/>
            <stop offset="1" stop-color="#65E8FF" stop-opacity=".22"/>
          </linearGradient>
          <linearGradient id="book-edge" x1="150" y1="380" x2="1050" y2="380" gradientUnits="userSpaceOnUse">
            <stop stop-color="#67E8FF"/>
            <stop offset=".48" stop-color="#B5A0FF"/>
            <stop offset="1" stop-color="#FF8BEA"/>
          </linearGradient>
          <filter id="book-glow" x="40" y="70" width="1120" height="570" filterUnits="userSpaceOnUse">
            <feGaussianBlur stdDeviation="12" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
          </filter>
        </defs>
        <g filter="url(#book-glow)" stroke="url(#book-edge)" stroke-linecap="round" stroke-linejoin="round">
          <path d="M600 255C485 185 330 165 185 205V466C330 425 485 450 600 530V255Z"
                fill="url(#page-left)" stroke-width="3"/>
          <path d="M600 255C715 185 870 165 1015 205V466C870 425 715 450 600 530V255Z"
                fill="url(#page-right)" stroke-width="3"/>
          <path d="M600 257V530" stroke-width="4"/>
          <path d="M212 240C344 211 475 231 565 282M212 278C344 249 475 269 565 320M212 316C344 287 475 307 565 358M212 354C344 325 475 345 565 396M212 392C344 363 475 383 565 434"
                stroke-width="2" stroke-opacity=".68"/>
          <path d="M988 240C856 211 725 231 635 282M988 278C856 249 725 269 635 320M988 316C856 287 725 307 635 358M988 354C856 325 725 345 635 396M988 392C856 363 725 383 635 434"
                stroke-width="2" stroke-opacity=".68"/>
          <path d="M170 490C330 448 477 468 600 550C723 468 870 448 1030 490"
                stroke-width="2" stroke-opacity=".55"/>
          <ellipse cx="600" cy="363" rx="470" ry="235" stroke-width="1.5" stroke-opacity=".28"/>
          <path d="M160 555H1040" stroke-width="1.5" stroke-opacity=".38"/>
        </g>
        <g stroke="url(#book-edge)" stroke-width="2" stroke-opacity=".45">
          <path d="M600 115V165M600 560V605M300 160L328 198M900 160L872 198"/>
          <circle cx="600" cy="107" r="5" fill="#8DEAFF"/>
          <circle cx="300" cy="151" r="4" fill="#B5A0FF"/>
          <circle cx="900" cy="151" r="4" fill="#FF8BEA"/>
        </g>
      </svg>
    </div>
    """,
    unsafe_allow_html=True,
)
st.title("Zero-Download Knowledge Assistant")
st.caption("Runs entirely in the cloud. No local embedding files downloaded.")

# Initialize Session States
if "full_text" not in st.session_state:
    st.session_state.full_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 1. Simple memory-only text parser (No downloading required)
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file:
    if "last_file" not in st.session_state or st.session_state.last_file != uploaded_file.name:
        with st.spinner("Extracting text to cloud memory..."):
            reader = pypdf.PdfReader(uploaded_file)
            extracted = "".join([page.extract_text() or "" for page in reader.pages])
            st.session_state.full_text = extracted
            st.session_state.last_file = uploaded_file.name
            st.success("✅ Document loaded to memory!")

st.divider()
st.subheader("💬 Ask Your Document")

# Display Conversation
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if query := st.chat_input("What would you like to know from the document?"):
    if not st.session_state.full_text:
        st.error("Please upload a PDF first.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)
            
        with st.chat_message("assistant"):
            loading_status = st.empty()
            loading_status.markdown(
                """
                <style>
                @keyframes loading-dot {
                    0%, 20% { opacity: 0.18; transform: translateY(0); }
                    50% { opacity: 1; transform: translateY(-2px); }
                    80%, 100% { opacity: 0.18; transform: translateY(0); }
                }
                .answer-loading {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    width: fit-content;
                    padding: 0.7rem 1rem;
                    border: 1px solid rgba(141, 234, 255, 0.38);
                    border-radius: 10px;
                    background: rgba(8, 13, 27, 0.42);
                    color: #d9e8fa;
                    box-shadow: 0 0 18px rgba(91, 204, 255, 0.1);
                    font-size: 0.95rem;
                }
                .answer-loading-dot {
                    color: #8deaff;
                    animation: loading-dot 1.2s infinite ease-in-out;
                }
                .answer-loading-dot:nth-child(2) { animation-delay: 0.15s; }
                .answer-loading-dot:nth-child(3) { animation-delay: 0.3s; }
                .answer-loading-dot:nth-child(4) { animation-delay: 0.45s; }
                </style>
                <div class="answer-loading" role="status" aria-live="polite">
                    <span>Loading</span>
                    <span class="answer-loading-dot">.</span>
                    <span class="answer-loading-dot">.</span>
                    <span class="answer-loading-dot">.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            try:
                # Pass the entire text directly to the model's large context window
                system_prompt = (
                    "You are a precise document assistant. Read the document text below carefully "
                    "and answer the user prompt accurately. If it is not in the text, say you don't know.\n\n"
                    f"DOCUMENT CONTENT:\n{st.session_state.full_text}"
                )
                client = Groq(api_key=GROQ_API_KEY)
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.7,
                    extra_body={
                        "reasoning_effort": "medium"
                    }
                )

                answer = response.choices[0].message.content
                loading_status.empty()
                st.write(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                loading_status.empty()
                st.error(f"Groq Cloud Error: {str(e)}")
