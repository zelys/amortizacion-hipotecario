from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDF:
    def __init__(self, filename):
        self.filename = filename
        self.styles = self._get_styles()
        self.elements = []

    def _get_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Header',
            fontSize=16,
            leading=20,
            alignment=1,  # centro
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            name='Body',
            fontSize=10,
            leading=14,
            alignment=1, 
            textColor=colors.HexColor('#2C3E50'),
            fontName='Helvetica'
        ))
        styles.add(ParagraphStyle(
            name='Footer',
            fontSize=8,
            leading=10,
            alignment=1,  # center
            textColor=colors.HexColor('#7F8C8D'),
            fontName='Helvetica'
        ))
        return styles

    def add_title(self, title):
        self.elements.append(Paragraph(title, self.styles['Header']))
        self.elements.append(Spacer(1, 12))

    def add_paragraph(self, text):
        self.elements.append(Paragraph(text, self.styles['Body']))
        self.elements.append(Spacer(1, 12))

    def add_table(self, data, col_widths=None):
        table = Table(data, colWidths=col_widths)
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
        ])
        table.setStyle(style)
        self.elements.append(table)

    def build(self):
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        doc.build(self.elements)
