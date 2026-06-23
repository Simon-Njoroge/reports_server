from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

class PDFStyles:
    """Naks Yetu brand styling for PDF reports"""
    
    # Brand Colors (matching your React component)
    BRAND_PRIMARY = '#C94A2B'  # Orange-red
    BRAND_SECONDARY = '#C0168A'  # Magenta/pink
    BRAND_DARK = '#33001A'  # Dark purple
    BRAND_GRADIENT_START = '#33001A'
    BRAND_GRADIENT_END = '#C94A2B'
    
    # UI Colors
    SUCCESS = '#10B981'
    WARNING = '#F59E0B'
    INFO = '#3B82F6'
    DANGER = '#EF4444'
    
    # Text Colors
    TEXT_PRIMARY = '#111827'
    TEXT_SECONDARY = '#4B5563'
    TEXT_MUTED = '#9CA3AF'
    TEXT_WHITE = '#FFFFFF'
    
    # Background Colors
    BG_HEADER = '#F9FAFB'
    BG_ROW_ALT = '#F3F4F6'
    BG_TABLE_HEADER = '#F1F0EE'
    
    @classmethod
    def register_fonts(cls):
        """Register custom fonts if available, else use default"""
        try:
            # Try to register Ubuntu font (similar to your component)
            pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('Ubuntu-Bold', 'Ubuntu-Bold.ttf'))
            addMapping('Ubuntu', 0, 0, 'Ubuntu')  # normal
            addMapping('Ubuntu', 1, 0, 'Ubuntu-Bold')  # bold
            return True
        except:
            return False
    
    @classmethod
    def get_styles(cls):
        """Get all paragraph styles"""
        styles = getSampleStyleSheet()
        
        # Register fonts if available
        cls.register_fonts()
        
        # Title style
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            fontName='Ubuntu-Bold',
            fontSize=28,
            textColor=colors.HexColor(cls.BRAND_DARK),
            alignment=TA_CENTER,
            spaceAfter=0.3*inch,
            leading=34
        ))
        
        # Subtitle style
        styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=styles['Normal'],
            fontName='Ubuntu',
            fontSize=14,
            textColor=colors.HexColor(cls.TEXT_SECONDARY),
            alignment=TA_CENTER,
            spaceAfter=0.5*inch,
            leading=18
        ))
        
        # Section header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontName='Ubuntu-Bold',
            fontSize=18,
            textColor=colors.HexColor(cls.BRAND_PRIMARY),
            spaceAfter=0.2*inch,
            leading=22
        ))
        
        # Table header style
        styles.add(ParagraphStyle(
            name='TableHeader',
            parent=styles['Normal'],
            fontName='Ubuntu-Bold',
            fontSize=9,
            textColor=colors.HexColor(cls.TEXT_PRIMARY),
            alignment=TA_LEFT,
            leading=12
        ))
        
        # Table cell style
        styles.add(ParagraphStyle(
            name='TableCell',
            parent=styles['Normal'],
            fontName='Ubuntu',
            fontSize=8.5,
            textColor=colors.HexColor(cls.TEXT_SECONDARY),
            alignment=TA_LEFT,
            leading=11
        ))
        
        # Table cell right aligned
        styles.add(ParagraphStyle(
            name='TableCellRight',
            parent=styles['TableCell'],
            alignment=TA_RIGHT
        ))
        
        # Table cell center aligned
        styles.add(ParagraphStyle(
            name='TableCellCenter',
            parent=styles['TableCell'],
            alignment=TA_CENTER
        ))
        
        # Summary number style
        styles.add(ParagraphStyle(
            name='SummaryNumber',
            parent=styles['Normal'],
            fontName='Ubuntu-Bold',
            fontSize=24,
            textColor=colors.HexColor(cls.BRAND_SECONDARY),
            alignment=TA_CENTER,
            leading=28
        ))
        
        # Summary label style
        styles.add(ParagraphStyle(
            name='SummaryLabel',
            parent=styles['Normal'],
            fontName='Ubuntu',
            fontSize=10,
            textColor=colors.HexColor(cls.TEXT_MUTED),
            alignment=TA_CENTER,
            leading=12
        ))
        
        # Footer style
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontName='Ubuntu',
            fontSize=8,
            textColor=colors.HexColor(cls.TEXT_MUTED),
            alignment=TA_CENTER,
            leading=10
        ))
        
        # Status styles
        styles.add(ParagraphStyle(
            name='StatusSuccess',
            parent=styles['TableCell'],
            fontName='Ubuntu-Bold',
            fontSize=8.5,
            textColor=colors.HexColor(cls.SUCCESS),
        ))
        
        styles.add(ParagraphStyle(
            name='StatusFailed',
            parent=styles['TableCell'],
            fontName='Ubuntu-Bold',
            fontSize=8.5,
            textColor=colors.HexColor(cls.DANGER),
        ))
        
        styles.add(ParagraphStyle(
            name='StatusPending',
            parent=styles['TableCell'],
            fontName='Ubuntu-Bold',
            fontSize=8.5,
            textColor=colors.HexColor(cls.WARNING),
        ))
        
        return styles