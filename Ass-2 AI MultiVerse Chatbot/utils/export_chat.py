import os
from fpdf import FPDF
from datetime import datetime
from config import EXPORTS_DIR

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def export_to_txt(messages, persona):
    """Exports the chat history to a TXT file."""
    timestamp = get_timestamp()
    filename = f"chat_{persona.replace(' ', '_')}_{timestamp}.txt"
    filepath = os.path.join(EXPORTS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"--- Chat with {persona} ---\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for msg in messages:
            if msg["role"] != "system":
                role = "User" if msg["role"] == "user" else persona
                f.write(f"{role}:\n{msg['content']}\n\n")
                
    return filepath

def export_to_pdf(messages, persona):
    """Exports the chat history to a PDF file."""
    timestamp = get_timestamp()
    filename = f"chat_{persona.replace(' ', '_')}_{timestamp}.pdf"
    filepath = os.path.join(EXPORTS_DIR, filename)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(200, 10, txt=f"Chat with {persona}", ln=True, align='C')
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    for msg in messages:
        if msg["role"] != "system":
            role = "User" if msg["role"] == "user" else persona
            # Role Header
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, txt=f"{role}:", ln=True)
            
            # Content
            pdf.set_font("Helvetica", "", 11)
            # Replace unsupported characters if needed or use simple string encoding
            # Multi_cell handles wrapping
            content = msg['content'].encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 8, txt=content)
            pdf.ln(5)
            
    pdf.output(filepath)
    return filepath
