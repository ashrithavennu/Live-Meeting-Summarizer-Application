from io import BytesIO
from fpdf import FPDF

def clean_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

def export_to_md(transcript, summary):
    return f"# Meeting Summary\n\n## Transcript\n{transcript}\n\n## Summary\n{summary}"

def export_to_pdf(transcript, summary):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, clean_text("Transcript:\n" + transcript))
    pdf.ln()
    pdf.multi_cell(0, 10, clean_text("Summary:\n" + summary))

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes