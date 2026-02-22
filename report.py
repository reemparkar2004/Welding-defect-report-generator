from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Map defect types to causes
defect_causes = {
    "Porosity": "Gas trapped in the weld metal due to improper shielding.",
    "Crack": "Too much heat or rapid cooling causing cracks.",
    "Undercut": "Improper welding angle or speed.",
    "Good Weld": "No defect detected.",
    "None": "No defect detected."
}

def generate_pdf(data, output_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    content = []

    # Title
    content.append(Paragraph("Welding Inspection Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # Weld Image
    if data.get("image"):
        img = Image(data["image"])
        img.drawHeight = 6 * cm
        img.drawWidth = 12 * cm
        content.append(Paragraph("Weld Image:", styles["Heading2"]))
        content.append(img)
        content.append(Spacer(1, 12))

    # Defect Detected?
    defect_detected = "Yes" if data["defect"] not in ["None", "Good Weld"] else "No"
    content.append(Paragraph(f"Defect Detected? {defect_detected}", styles["Normal"]))
    content.append(Spacer(1, 6))

    # Type of Defect
    content.append(Paragraph(f"Type of Defect: {data['defect']}", styles["Normal"]))
    content.append(Spacer(1, 6))

    # Cause of Defect
    cause = defect_causes.get(data["defect"], "No detailed explanation available for this defect.")
    content.append(Paragraph(f"Cause of Defect: {cause}", styles["Normal"]))
    content.append(Spacer(1, 6))

    # Confidence (optional)
    content.append(Paragraph(f"Confidence: {round(data.get('confidence', 0), 2)}", styles["Normal"]))

    # Build PDF
    doc.build(content)
