from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

# Initialiser les styles
styles = getSampleStyleSheet()

# Définir les styles une seule fois en constantes
HEADER_STYLE = ParagraphStyle(
    'HeaderStyle',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.whitesmoke,
    alignment=1,
    spaceAfter=6,
    spaceBefore=6,
    leading=12
)

def generate_inventory_pdf(materials, output_file):
    # Création du document avec des marges réduites
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=30,  # Réduire les marges
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Centre
    )
    
    # Contenu du document
    elements = []
    
    # Titre
    title = Paragraph("Inventaire du Matériel", title_style)
    elements.append(title)
    
    # Date de génération
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        alignment=1
    )
    date_text = f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
    elements.append(Paragraph(date_text, date_style))
    elements.append(Spacer(1, 20))
    
    # Style pour les en-têtes de colonnes
    header_style = HEADER_STYLE
    
    # Données pour le tableau avec Paragraph pour les en-têtes
    data = [[
        Paragraph("Nom", header_style),
        Paragraph("N° Série", header_style),
        Paragraph("Caté-<br/>gorie", header_style),
        Paragraph("Adresse<br/>MAC", header_style),
        Paragraph("Marque/<br/>Modèle", header_style),
        Paragraph("Locali-<br/>sation", header_style),
        Paragraph("Utilisa-<br/>teur", header_style),
        Paragraph("Date<br/>d'attrib.", header_style)
    ]]
    
    for material in materials:
        data.append([
            material.name,
            material.serial_number or "",
            material.category or "",
            material.mac_address or "",
            material.brand_model or "",
            material.location or "",
            material.assigned_user or "",
            material.assignment_date.strftime("%d/%m/%Y") if material.assignment_date else ""
        ])
    
    # Définir les largeurs relatives des colonnes (ajustées)
    col_widths = [
        doc.width * p for p in [
            0.12,  # Nom (12%)
            0.12,  # N° Série (12%)
            0.11,  # Catégorie (11%)
            0.15,  # Adresse MAC (15%)
            0.14,  # Marque/Modèle (14%)
            0.13,  # Localisation (13%)
            0.12,  # Utilisateur (12%)
            0.11   # Date d'attribution (11%)
        ]
    ]
    
    # Création du tableau avec les largeurs définies
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        # Style de l'en-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),  # Ajout de padding en haut
        # Style du contenu
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        # Bordures
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        # Alternance des couleurs des lignes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f6fa')]),
        # Gestion du texte long
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))
    
    elements.append(table)
    
    # Ajout du pied de page
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=1
    )
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Document généré par GestCharge V1.0", footer_style))
    
    # Génération du PDF
    doc.build(elements)
