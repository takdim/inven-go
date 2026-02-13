"""PDF Export Utility using ReportLab"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
import os

try:
    from PIL import Image as PILImage
except Exception:
    PILImage = None


def _build_logo_flowable(logo_path, width_cm=2.6, height_cm=2.6):
    """Build a ReportLab Image flowable and normalize transparent PNGs."""
    if not logo_path or not os.path.exists(logo_path):
        return None

    width = width_cm * cm
    height = height_cm * cm

    if PILImage is not None:
        try:
            with PILImage.open(logo_path) as pil_logo:
                has_alpha = pil_logo.mode in ('RGBA', 'LA') or 'transparency' in pil_logo.info

                if has_alpha:
                    rgba_logo = pil_logo.convert('RGBA')
                    white_bg = PILImage.new('RGB', rgba_logo.size, (255, 255, 255))
                    white_bg.paste(rgba_logo, mask=rgba_logo.split()[-1])

                    logo_buffer = BytesIO()
                    white_bg.save(logo_buffer, format='PNG')
                    logo_buffer.seek(0)

                    logo = Image(logo_buffer, width=width, height=height)
                    logo._source_buffer = logo_buffer
                    return logo

                if pil_logo.mode != 'RGB':
                    rgb_logo = pil_logo.convert('RGB')
                    logo_buffer = BytesIO()
                    rgb_logo.save(logo_buffer, format='PNG')
                    logo_buffer.seek(0)

                    logo = Image(logo_buffer, width=width, height=height)
                    logo._source_buffer = logo_buffer
                    return logo
        except Exception:
            pass

    return Image(logo_path, width=width, height=height)


def _draw_logo_on_canvas(canvas, doc, logo_path, width_cm=2.6, height_cm=2.6):
    """Draw logo at the left side of kop surat directly on canvas."""
    if not logo_path or not os.path.exists(logo_path):
        return

    width = width_cm * cm
    height = height_cm * cm
    x_pos = doc.leftMargin
    y_pos = A4[1] - doc.topMargin - height

    if PILImage is not None:
        try:
            with PILImage.open(logo_path) as pil_logo_raw:
                has_alpha = pil_logo_raw.mode in ('RGBA', 'LA') or 'transparency' in pil_logo_raw.info
                if has_alpha:
                    rgba_logo = pil_logo_raw.convert('RGBA')
                    white_bg = PILImage.new('RGB', rgba_logo.size, (255, 255, 255))
                    white_bg.paste(rgba_logo, mask=rgba_logo.split()[-1])
                    render_logo = white_bg
                else:
                    render_logo = pil_logo_raw.convert('RGB')

                canvas.drawInlineImage(render_logo, x_pos, y_pos, width=width, height=height)
                return
        except Exception:
            pass

    canvas.drawImage(
        logo_path,
        x_pos,
        y_pos,
        width=width,
        height=height,
        preserveAspectRatio=True,
        mask='auto'
    )


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
        "LAPORAN DAFTAR BARANG PERPUSTAKAAN UNIVERSITAS HASANUDDIN",
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
        "LAPORAN DAFTAR KONTRAK/SPK PERPUSTAKAAN UNIVERSITAS HASANUDDIN",
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


def export_laporan_kerusakan_to_pdf(laporan, logo_path=None):
    """Export surat laporan kerusakan per aset ke PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    header_bold = ParagraphStyle(
        'HeaderBold',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=11,
        leading=13,
        fontName='Helvetica-Bold'
    )
    header_normal = ParagraphStyle(
        'HeaderNormal',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=9.5,
        leading=12
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14
    )

    header_lines = [
        "KEMENTERIAN PENDIDIKAN TINGGI, SAINS,",
        "DAN TEKNOLOGI",
        "UNIVERSITAS HASANUDDIN",
        "PERPUSTAKAAN",
        "Jalan Perintis Kemerdekaan Km. 10, Makassar 90245",
        "Telepon (0411) 586200, FAX (0411) 585188",
        "Laman https://library.unhas.ac.id    email : library@unhas.ac.id"
    ]

    elements = []

    for idx, line in enumerate(header_lines):
        style = header_bold if idx <= 3 else header_normal
        elements.append(Paragraph(line, style))

    elements.append(Spacer(1, 0.2*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 0.5*cm))

    salam_pembuka = (
        "Kepada Yth.<br/>"
        "Kepala Sub Bagian (Kasubag) Perpustakaan<br/>"
        "Universitas Hasanuddin<br/>"
        "Di Tempat<br/><br/>"
        "Dengan hormat,"
    )
    elements.append(Paragraph(salam_pembuka, body_style))
    elements.append(Spacer(1, 0.3*cm))

    pembuka = (
        "Bersama ini kami sampaikan laporan kerusakan komputer yang terdapat di "
        "lingkungan Perpustakaan Universitas Hasanuddin sebagai bahan pertimbangan "
        "untuk dilakukan tindak lanjut perbaikan atau penggantian perangkat."
    )
    elements.append(Paragraph(pembuka, body_style))
    elements.append(Spacer(1, 0.4*cm))

    aset = laporan.aset_tetap
    table_data = [
        ['Keterangan', 'Detail'],
        ['Nama Perangkat', aset.nama_aset],
        ['Nama Pengguna', laporan.nama_pengguna],
        ['Jumlah', f"{laporan.jumlah} Unit"],
        ['Lokasi', laporan.lokasi],
        ['Tanggal Diketahui Rusak', laporan.tanggal_diketahui_rusak.strftime('%d %B %Y')],
        ['Jenis Kerusakan', laporan.jenis_kerusakan],
        ['Penyebab (jika diketahui)', laporan.penyebab or '-'],
        ['Tindakan yang sudah dilakukan', laporan.tindakan or '-'],
        ['Kondisi Saat Ini', laporan.kondisi_saat_ini or '-'],
        ['Dampak', laporan.dampak or '-']
    ]

    table = Table(table_data, colWidths=[6*cm, 10*cm])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f2f2f2')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6)
    ]))
    elements.append(table)

    elements.append(Spacer(1, 0.4*cm))
    penutup = (
        "Demikian laporan kerusakan komputer ini kami sampaikan. "
        "Atas perhatian dan tindak lanjut Bapak/Ibu, kami ucapkan terima kasih."
    )
    elements.append(Paragraph(penutup, body_style))
    elements.append(Spacer(1, 0.6*cm))

    tanggal_surat = laporan.created_at.strftime('%d %B %Y') if laporan.created_at else datetime.now().strftime('%d %B %Y')
    elements.append(Paragraph(f"Makassar, {tanggal_surat}", body_style))
    elements.append(Spacer(1, 0.6*cm))
    elements.append(Paragraph("Hormat kami,", body_style))
    elements.append(Spacer(1, 1.2*cm))

    pelapor_nama = laporan.pelapor.nama_lengkap if laporan.pelapor else "...................................."
    elements.append(Paragraph(f"({pelapor_nama})<br/>Petugas / Pelapor", body_style))

    def _on_first_page(canvas, doc_obj):
        _draw_logo_on_canvas(canvas, doc_obj, logo_path, width_cm=2.6, height_cm=2.6)

    doc.build(elements, onFirstPage=_on_first_page)
    buffer.seek(0)
    return buffer


def export_transaksi_to_pdf(transaksi_list, jenis, tanggal_awal=None, tanggal_akhir=None, filename=None):
    """Export transaksi masuk/keluar ke PDF"""
    pdf = PDFExporter(orientation='landscape')
    
    # Title
    title = f"LAPORAN BARANG {jenis.upper()} PERPUSTAKAAN UNIVERSITAS HASANUDDIN"
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


def export_merk_aset_tetap_to_pdf(merk_list, filename=None):
    """Export daftar merk aset tetap ke PDF"""
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from io import BytesIO
    from xml.sax.saxutils import escape
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#366092'),
        spaceAfter=6,
        alignment=1  # Center
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=12,
        alignment=1  # Center
    )
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        spaceAfter=12,
        alignment=0  # Left
    )
    header_cell_style = ParagraphStyle(
        'MerkHeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.whitesmoke,
        alignment=1
    )
    cell_left_style = ParagraphStyle(
        'MerkCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=0,
        wordWrap='LTR',
        splitLongWords=1
    )
    cell_center_style = ParagraphStyle(
        'MerkCellCenter',
        parent=cell_left_style,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph('LAPORAN DATA MERK ASET TETAP PERPUSTAKAAN UNIVERSITAS HASANUDDIN', title_style))
    elements.append(Paragraph(f'Per {datetime.now().strftime("%d %B %Y")}', subtitle_style))
    elements.append(Paragraph(f'Total Merk: <b>{len(merk_list)} item</b> | Dicetak pada: {datetime.now().strftime("%d/%m/%Y %H:%M")}', info_style))
    
    def normalize_pdf_text(value):
        if value is None:
            return '-'

        text = str(value)
        replacements = {
            '\u200b': '',   # zero-width space
            '\ufeff': '',   # byte order mark
            '\u00ad': '',   # soft hyphen
            '™': '(TM)',
            '®': '(R)',
            '©': '(C)',
            '–': '-',
            '—': '-',
            '“': '"',
            '”': '"',
            '‘': "'",
            '’': "'",
            '•': '-',
            '\xa0': ' ',
        }
        for src, dst in replacements.items():
            text = text.replace(src, dst)

        # Avoid glyph issues with base PDF fonts.
        text = ''.join(ch if ord(ch) <= 255 else '?' for ch in text)
        return text.strip() or '-'

    def truncate_pdf_text(value, max_len):
        text = normalize_pdf_text(value).replace('\n', ' ')
        text = ' '.join(text.split())
        if len(text) > max_len:
            return text[:max_len - 3] + '...'
        return text

    def p(text, style):
        safe = escape(normalize_pdf_text(text)).replace('\n', ' ')
        return Paragraph(safe, style)

    # Table data
    table_data = [[
        p('No', header_cell_style),
        p('Nama Merk', header_cell_style),
        p('Tipe', header_cell_style),
        p('Spesifikasi', header_cell_style),
        p('Tanggal Pengadaan', header_cell_style),
        p('Kontrak/SPK', header_cell_style),
        p('Jumlah Aset', header_cell_style),
    ]]
    
    for idx, merk in enumerate(merk_list, 1):
        table_data.append([
            p(idx, cell_center_style),
            p(truncate_pdf_text(merk.nama_merk, 60), cell_left_style),
            p(truncate_pdf_text(merk.tipe or '-', 60), cell_center_style),
            p(truncate_pdf_text(merk.spesifikasi or '-', 160), cell_left_style),
            p(merk.tanggal_pengadaan.strftime('%d/%m/%Y') if merk.tanggal_pengadaan else '-', cell_center_style),
            p(truncate_pdf_text(merk.nomor_kontrak or '-', 80), cell_center_style),
            p(merk.get_total_aset_by_criteria(), cell_center_style),
        ])
    
    # Use nearly full printable width to avoid cramped columns.
    table = Table(
        table_data,
        colWidths=[0.45*inch, 1.4*inch, 1.2*inch, 2.8*inch, 1.25*inch, 1.9*inch, 1.0*inch],
        repeatRows=1
    )
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f'<i>Dibuat oleh Inven-Go System</i>', info_style))
    
    doc.build(elements)
    buffer.seek(0)
    
    return buffer
