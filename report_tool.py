
import sqlite3
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_customer_report():
    # Read unfinished customer requests from SQLite
    conn = sqlite3.connect("customers.db")

    try:
        customers = conn.execute(
            "SELECT id, name, status FROM customers WHERE status != ?",
            ("Completed",)
        ).fetchall()
    finally:
        conn.close()

    # Create PDF
    filename = "customer_report.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = [
        Paragraph("Customer Status Report", styles["Title"]),
        Paragraph(
            f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
            styles["Normal"]
        ),
        Spacer(1, 20),
    ]

    data = [["Customer ID", "Name", "Status"]]
    data.extend([list(customer) for customer in customers])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
    ]))

    elements.append(table)
    doc.build(elements)

    return filename


if __name__ == "__main__":
    print("Report created:", generate_customer_report())

