import os
from datetime import datetime
from fpdf import FPDF

class ComicPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'ComicCraft - AI Generated Comic', 0, 1, 'C')
        self.ln(5)

def save_pdf(layout):
    export_folder = os.path.join("static", "exports")
    os.makedirs(export_folder, exist_ok=True)

    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        
        # Panel Title
        pdf.set_font("Arial", "B", 14)
        title_text = f"Panel {panel.get('panel')}: {panel.get('title', '')}"
        safe_title = title_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 10, safe_title, ln=True, align="L")
        pdf.ln(3)

        # Panel Image
        image_path = panel.get("image_path", "")
        if image_path.startswith("/"):
            clean_img_path = image_path[1:].split("?")[0]
        else:
            clean_img_path = image_path.split("?")[0]

        if os.path.exists(clean_img_path):
            pdf.image(clean_img_path, x=15, y=30, w=180, h=120)
            pdf.set_y(155)
        else:
            pdf.set_y(40)

        # Scene Description
        scene_desc = panel.get("scene_description", "")
        if scene_desc:
            pdf.set_font("Arial", "I", 10)
            safe_scene = scene_desc.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, safe_scene)
            pdf.ln(3)

        # Narration / Dialogue
        story_text = panel.get("text", "")
        pdf.set_font("Arial", "", 11)
        safe_text = story_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 7, safe_text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(export_folder, filename)
    
    pdf.output(pdf_path)
    return pdf_path