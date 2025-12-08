"""PDF Export Utility using ReportLab"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO


class PDFExporter:
    """Class untuk generate PDF reports"""
    
    def __init__(self, title="Laporan", orientation='portrait'):
        self.title = title
        self.orientation = orientation
        self.buffer = BytesIO()
        
        # Page size
        if orientation == 'landscape':
            self.pagesize = landscape(A4)
        else:
            self.pagesize = A4
        
        # Create document
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=self.pagesize,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Story (content)
        self.story = []
        
        # Styles
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#366092'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        self.subtitle_style = ParagraphStyle(
            'CustomSubTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#366092'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
    
    def add_title(self, title, subtitle=None):
        """Tambah judul laporan"""
        self.story.append(Paragraph(title, self.title_style))
        if subtitle:
            self.story.append(Paragraph(subtitle, self.subtitle_style))
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_paragraph(self, text, style=None):
        """Tambah paragraf"""
        if style is None:
            style = self.styles['Normal']
        self.story.append(Paragraph(text, style))
        self.story.append(Spacer(1, 0.3*cm))
    
    def add_table(self, data, col_widths=None, with_header=True):
        """Tambah tabel"""
        # Create table
        table = Table(data, colWidths=col_widths)
        
        # Table style
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]
        
        table.setStyle(TableStyle(table_style))
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_spacer(self, height=0.5):
        """Tambah space"""
        self.story.append(Spacer(1, height*cm))
    
    def add_page_break(self):
        """Tambah page break"""
        self.story.append(PageBreak())
    
    def build(self):
        """Build PDF"""
        self.doc.build(self.story)
        self.buffer.seek(0)
        return self.buffer
    
    def save(self, filename):
        """Save to file"""
        pdf_buffer = self.build()
        with open(filename, 'wb') as f:
            f.write(pdf_buffer.read())


# Helper functions untuk laporan spesifik
def export_barang_to_pdf(barang_list, filename=None):
    """Export daftar barang ke PDF"""
    pdf = PDFExporter(orientation='landscape')
    
    # Title
    pdf.add_title(
        "LAPORAN DAFTAR BARANG",
        f"Per {datetime.now().strftime('%d %B %Y')}"
    )
    
    # Info
    info_text = f"Total Barang: <b>{len(barang_list)} item</b> | Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    pdf.add_paragraph(info_text)
    
    # Table data
    table_data = [['No', 'Kode Barang', 'Nama Barang', 'Kategori', 'Merk', 'Satuan', 'Stok Awal', 'Stok Akhir', 'Status']]
    
    for idx, item in enumerate(barang_list, 1):
        barang = item['barang']
        stok_akhir = item['stok_akhir']
        
        # Status stok
        if stok_akhir < 10:
            status = "RENDAH"
        elif stok_akhir < 50:
            status = "SEDANG"
        else:
            status = "AMAN"
        
        table_data.append([
            str(idx),
            barang.kode_barang,
            barang.nama_barang,
            barang.kategori.nama_kategori if barang.kategori else '-',
            barang.merk.nama_merk if barang.merk else '-',
            barang.satuan,
            str(barang.stok_awal),
            str(stok_akhir),
            status
        ])
    
    # Add table
    pdf.add_table(table_data)
    
    # Footer
    pdf.add_paragraph(f"<i>Dibuat oleh Inven-Go System</i>", pdf.styles['Normal'])
    
    if filename:
        pdf.save(filename)
    
    return pdf.build()


def export_kontrak_to_pdf(kontrak_list, filename=None):
    """Export daftar kontrak ke PDF"""
    pdf = PDFExporter()
    
    # Title
    pdf.add_title(
        "LAPORAN DAFTAR KONTRAK/SPK",
        f"Per {datetime.now().strftime('%d %B %Y')}"
    )
    
    # Info
    info_text = f"Total Kontrak: <b>{len(kontrak_list)} kontrak</b> | Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    pdf.add_paragraph(info_text)
    
    # Table data
    table_data = [['No', 'Nomor Kontrak', 'Tanggal', 'Jumlah Barang', 'Total Qty', 'Total Nilai (Rp)']]
    
    total_nilai = 0
    for idx, kontrak in enumerate(kontrak_list, 1):
        nilai_kontrak = kontrak.get_total_nilai()
        total_nilai += nilai_kontrak
        
        table_data.append([
            str(idx),
            kontrak.nomor_kontrak,
            kontrak.tanggal_kontrak.strftime('%d/%m/%Y'),
            str(kontrak.barang_kontrak.count()),
            str(kontrak.get_total_qty()),
            f"Rp {nilai_kontrak:,.0f}" if nilai_kontrak > 0 else '-'
        ])
    
    # Summary row
    table_data.append(['', '', '', '', 'TOTAL:', f"Rp {total_nilai:,.0f}"])
    
    # Add table
    col_widths = [1*cm, 4*cm, 3*cm, 3*cm, 2*cm, 4*cm]
    pdf.add_table(table_data, col_widths=col_widths)
    
    # Footer
    pdf.add_paragraph(f"<i>Dibuat oleh Inven-Go System</i>", pdf.styles['Normal'])
    
    if filename:
        pdf.save(filename)
    
    return pdf.build()


def export_transaksi_to_pdf(transaksi_list, jenis, tanggal_awal=None, tanggal_akhir=None, filename=None):
    """Export transaksi masuk/keluar ke PDF"""
    pdf = PDFExporter(orientation='landscape')
    
    # Title
    title = f"LAPORAN BARANG {jenis.upper()}"
    if tanggal_awal and tanggal_akhir:
        subtitle = f"Periode: {tanggal_awal.strftime('%d/%m/%Y')} - {tanggal_akhir.strftime('%d/%m/%Y')}"
    else:
        subtitle = f"Per {datetime.now().strftime('%d %B %Y')}"
    
    pdf.add_title(title, subtitle)
    
    # Info
    info_text = f"Total Transaksi: <b>{len(transaksi_list)} transaksi</b> | Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    pdf.add_paragraph(info_text)
    
    # Table data
    table_data = [['No', 'Tanggal', 'Kode Barang', 'Nama Barang', 'Qty', 'Satuan', 'Keterangan']]
    
    total_qty = 0
    for idx, transaksi in enumerate(transaksi_list, 1):
        total_qty += transaksi.qty
        
        table_data.append([
            str(idx),
            transaksi.tanggal.strftime('%d/%m/%Y'),
            transaksi.kode_barang,
            transaksi.barang.nama_barang if transaksi.barang else '-',
            str(transaksi.qty),
            transaksi.barang.satuan if transaksi.barang else '-',
            transaksi.keterangan or '-'
        ])
    
    # Summary row
    table_data.append(['', '', '', 'TOTAL:', str(total_qty), '', ''])
    
    # Add table
    pdf.add_table(table_data)
    
    # Footer
    pdf.add_paragraph(f"<i>Dibuat oleh Inven-Go System</i>", pdf.styles['Normal'])
    
    if filename:
        pdf.save(filename)
    
    return pdf.build()
