import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_comic_pdf(title: str, panels: list, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ComicTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        alignment=1,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=15
    )
    
    panel_title_style = ParagraphStyle(
        'PanelTitle',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )
    
    text_style = ParagraphStyle(
        'ComicText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 10))

    for panel in panels:
        story.append(Paragraph(panel['title'], panel_title_style))
        
        # Check local file path first for PDF inclusion
        img_file = panel.get('local_filepath', '')
        if img_file and os.path.exists(img_file):
            try:
                img = RLImage(img_file, width=400, height=250)
                story.append(img)
                story.append(Spacer(1, 8))
            except Exception as e:
                print(f"Error adding image to PDF: {e}")

        story.append(Paragraph(f"<b>Story:</b> {panel['story_text']}", text_style))
        story.append(Paragraph(f"<b>Dialogue:</b> {panel['dialogue']}", text_style))
        story.append(Spacer(1, 15))

    doc.build(story)