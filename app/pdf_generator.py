import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_comic_pdf(panels_data, output_filename="comic_book.pdf"):
    static_dir = "static"
    os.makedirs(static_dir, exist_ok=True)
    pdf_path = os.path.join(static_dir, output_filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ComicTitle', parent=styles['Heading1'], fontSize=24, alignment=1, textColor=colors.HexColor("#00D2FF"))
    panel_title_style = ParagraphStyle('PanelTitle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#00B4D8"))
    dialogue_style = ParagraphStyle('DialogueText', parent=styles['BodyText'], fontSize=10, textColor=colors.black)

    story.append(Paragraph("<b>ComicCraft AI - Anime Edition</b>", title_style))
    story.append(Spacer(1, 15))

    for item in panels_data:
        p_num = item["panel"]
        img_rel_path = item["image"].lstrip("/")
        
        if os.path.exists(img_rel_path):
            img_element = RLImage(img_rel_path, width=180, height=180)
        else:
            img_element = Paragraph("Image Loading...", dialogue_style)

        text_content = [
            Paragraph(f"<b>PANEL {p_num}</b>", panel_title_style),
            Spacer(1, 6),
            Paragraph(f"<b>Story:</b> {item.get('narration', '')}", dialogue_style),
            Spacer(1, 6),
            Paragraph(f"<b>Dialogue:</b> \"{item.get('dialogue', '')}\"", dialogue_style)
        ]

        table_data = [[img_element, text_content]]
        panel_table = Table(table_data, colWidths=[200, 310])
        panel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F4F7FC")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor("#00D2FF")),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor("#002B49")),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        story.append(panel_table)
        story.append(Spacer(1, 12))

    doc.build(story)
    return output_filename