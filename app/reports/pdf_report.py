from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from app.models import EPI

def generate_epi_report():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de EPIs")

    c.setFont("Helvetica", 12)
    y = height - 100
    total_valor = 0
    total_quantidade = 0

    epis = EPI.query.all()
    for epi in epis:
        linha = f"{epi.nome} - Quantidade: {epi.quantidade} - Valor: R${epi.valor:.2f}"
        c.drawString(50, y, linha)
        y -= 20
        total_valor += epi.valor
        total_quantidade += epi.quantidade

        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 30, f"TOTAL Quantidade: {total_quantidade}")
    c.drawString(50, y - 50, f"TOTAL Valor: R$ {total_valor:.2f}")

    c.save()
    buffer.seek(0)
    return buffer
