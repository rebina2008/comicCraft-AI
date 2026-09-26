import os
from fpdf import FPDF

def save_pdf(layout: list) -> str:
    pdf_dir = os.path.join("static", "exports")
    os.makedirs(pdf_dir, exist_ok=True)
    
    pdf_path = os.path.join(pdf_dir, "comic_export.pdf")
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Cover / Header
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=22)
    pdf.cell(0, 15, txt="ComicCraft AI - Anime Edition", ln=True, align="C")
    pdf.ln(10)
    
    # Iterate through exact layout items
    for panel in layout:
        panel_num = panel.get("panel", 1)
        title = panel.get("title", f"Panel {panel_num}")
        image_path = panel.get("image_path", "")
        description = panel.get("scene_description", "")
        
        pdf.add_page()
        pdf.set_font("Helvetica", style="B", size=15)
        pdf.cell(0, 10, txt=f"Panel {panel_num}: {title}", ln=True, align="L")
        pdf.ln(5)
        
        # Exact rendered image path from web preview is embedded here directly
        if image_path and os.path.exists(image_path):
            try:
                pdf.image(image_path, x=20, y=pdf.get_y(), w=170)
                pdf.ln(120)
            except Exception as e:
                print(f"Error adding image to PDF: {e}")
                pdf.ln(10)
        
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 7, txt=description)
        pdf.ln(5)

    pdf.output(pdf_path)
    return pdf_path