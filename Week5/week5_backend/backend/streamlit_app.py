# Top of streamlit_app.py
import sys

# Trick pydub to skip importing pyaudioop
sys.modules['pyaudioop'] = None

import streamlit as st
import tempfile
import datetime

from pipeline import process_audio_file
from export_utils import export_to_md, export_to_pdf
from email_utils import send_email
from logger_utils import save_log

st.set_page_config(page_title="AI Meeting Summarizer", layout="wide")

st.title("🎤 AI Live Meeting Summarizer")

# ---------------- SESSION ----------------
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "recording" not in st.session_state:
    st.session_state.recording = False


# ---------------- RECORD BUTTONS ----------------
from streamlit_mic_recorder import mic_recorder
import tempfile

st.subheader("🎙 Live Recording")

audio = mic_recorder(
    start_prompt="▶ Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder"
)

if audio:
    st.success("Recording completed!")

    # Save audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio["bytes"])
        audio_path = tmp.name

    st.info("🔵 Processing audio...")

    transcript, summary = process_audio_file(audio_path)

    st.session_state.transcript = transcript
    st.session_state.summary = summary

    save_log(transcript, summary)


# ---------------- AUDIO INPUT ----------------
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

if audio_file is not None and "processed" not in st.session_state:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        audio_path = tmp.name

    st.info("🔵 Transcribing...")

    with st.spinner("Processing audio... please wait ⏳"):
        transcript, summary = process_audio_file(audio_path)

    st.session_state.transcript = transcript
    st.session_state.summary = summary
    st.session_state.processed = True

    save_log(transcript, summary)


# ---------------- OUTPUT ----------------
st.subheader("📝 Transcript")
# st.write(st.session_state.get("transcript", "No transcript available ❌"))
st.text_area("Transcript Output", st.session_state.transcript, height=200)

st.subheader("📌 Summary")
# st.write(st.session_state.get("summary", "No summary available ❌"))
st.text_area("Summary Output", st.session_state.summary, height=150)


# ---------------- DOWNLOAD ----------------
col3, col4 = st.columns(2)

with col3:
    md_data = export_to_md(
        st.session_state.transcript,
        st.session_state.summary
    )

    st.download_button(
        "⬇ Download Markdown",
        md_data,
        file_name="meeting.md"
    )

with col4:
    pdf_data = export_to_pdf(
        st.session_state.transcript,
        st.session_state.summary
    )

    st.download_button(
        "⬇ Download PDF",
        pdf_data,
        file_name="meeting.pdf"
    )


# ---------------- EMAIL ----------------
st.subheader("📧 Send Summary")

email_to = st.text_input("Enter Email")

if st.button("Send Email"):

    transcript = st.session_state.get("transcript")
    summary = st.session_state.get("summary")

    if transcript and summary and "failed" not in transcript.lower():

        body = f"""
📝 Transcript:
{transcript}

📊 Summary:
{summary}
"""

        success = send_email(
            email_to,
            "Meeting Summary",
            body
        )

        if success:
            st.success("✅ Email sent successfully")
        else:
            st.error("❌ Email failed. Check credentials.")

    else:
        st.error("❌ No valid transcript available")