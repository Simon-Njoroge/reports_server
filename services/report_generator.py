from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import io
import logging
from datetime import datetime
from typing import List, Dict, Any
from services.pdf_style import PDFStyles

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        self.styles = PDFStyles.get_styles()
        self.brand_colors = {
            'primary': PDFStyles.BRAND_PRIMARY,
            'secondary': PDFStyles.BRAND_SECONDARY,
            'dark': PDFStyles.BRAND_DARK,
        }
    
    def generate_payment_report(
        self,
        payments: List[Dict[str, Any]],
        event_title: str = "Event Report",
        report_title: str = "Payment Summary Report",
        include_summary: bool = True,
        is_preview: bool = False
    ) -> io.BytesIO:
        """Generate a styled payment report PDF"""
        try:
            buffer = io.BytesIO()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=0.6*inch,
                leftMargin=0.6*inch,
                topMargin=0.6*inch,
                bottomMargin=0.6*inch
            )
            
            story = []
            
            # 1. Add header with logo and title
            story.extend(self._create_header(report_title, event_title))
            
            # 2. Add summary cards
            if include_summary:
                story.extend(self._create_summary_section(payments))
            
            # 3. Add payment table
            story.extend(self._create_payment_table(payments))
            
            # 4. Add footer
            story.extend(self._create_footer())
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise
    
    def _create_header(self, title: str, subtitle: str) -> List:
        """Create report header with brand styling"""
        story = []
        
        # Brand header bar with gradient (simulated with two rectangles)
        story.append(Spacer(1, 0.1*inch))
        
        # Header with brand colors
        header_style = ParagraphStyle(
            'HeaderBar',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor(PDFStyles.TEXT_WHITE),
            alignment=TA_CENTER,
            backColor=colors.HexColor(PDFStyles.BRAND_DARK),
            spaceAfter=0
        )
        
        # Title
        story.append(Paragraph(title, self.styles['ReportTitle']))
        
        # Subtitle / event info
        story.append(Paragraph(
            f"Event: {subtitle} | Generated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M')}",
            self.styles['ReportSubtitle']
        ))
        
        # Decorative line
        story.append(Spacer(1, 0.1*inch))
        story.append(self._create_decorative_line())
        story.append(Spacer(1, 0.1*inch))
        
        return story
    
    def _create_summary_section(self, payments: List[Dict]) -> List:
        """Create summary cards with key metrics"""
        story = []
        
        story.append(Paragraph("Summary", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.1*inch))
        
        # Calculate metrics
        total_payments = len(payments)
        total_amount = sum(p.get('amount', 0) for p in payments)
        successful = sum(1 for p in payments if p.get('status') == 'successful')
        avg_amount = total_amount / total_payments if total_payments > 0 else 0
        
        # Create summary table
        summary_data = [
            [
                self._create_metric_card("Total Payments", str(total_payments)),
                self._create_metric_card("Total Amount", f"KES {total_amount:,.2f}"),
                self._create_metric_card("Successful", str(successful)),
                self._create_metric_card("Average", f"KES {avg_amount:,.2f}"),
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[1.8*inch]*4)
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _create_metric_card(self, label: str, value: str) -> Table:
        """Create a single metric card"""
        data = [
            [Paragraph(value, self.styles['SummaryNumber'])],
            [Paragraph(label, self.styles['SummaryLabel'])],
        ]
        
        table = Table(data, colWidths=1.8*inch)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(PDFStyles.BG_TABLE_HEADER)),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(PDFStyles.BG_HEADER)),
            ('ROUNDEDCORNERS', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return table
    
    def _create_payment_table(self, payments: List[Dict]) -> List:
        """Create detailed payment table"""
        story = []
        
        story.append(Paragraph("Payment Details", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.1*inch))
        
        # Table headers
        headers = [
            'Reference', 'Customer Name', 'Phone', 'Event', 
            'Amount (KES)', 'Status', 'Provider', 'Paid At'
        ]
        
        # Table data
        table_data = [headers]
        
        # Add payment rows (limit to 20 per page for readability)
        display_payments = payments[:50]  # Show max 50 payments
        
        for payment in display_payments:
            # Format status with color
            status = payment.get('status', 'unknown')
            status_style = self._get_status_style(status)
            
            row = [
                payment.get('reference', '')[:20],
                payment.get('customerName', '')[:25],
                payment.get('customerPhone', '')[:12],
                payment.get('eventTitle', '')[:20],
                f"{payment.get('amount', 0):,.2f}",
                Paragraph(status.upper(), status_style),
                payment.get('provider', ''),
                self._format_date(payment.get('paidAt', ''))
            ]
            table_data.append(row)
        
        # Create table
        col_widths = [1.2*inch, 1.5*inch, 0.8*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.6*inch, 1.0*inch]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Table styling
        table_style = [
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PDFStyles.BG_TABLE_HEADER)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(PDFStyles.TEXT_PRIMARY)),
            ('FONTNAME', (0, 0), (-1, 0), 'Ubuntu-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Row styling
            ('FONTNAME', (0, 1), (-1, -1), 'Ubuntu'),
            ('FONTSIZE', (0, 1), (-1, -1), 8.5),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor(PDFStyles.BRAND_PRIMARY)),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]
        
        # Alternating row colors
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F9FAFB')))
        
        table.setStyle(TableStyle(table_style))
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        
        # Add note about total records
        if len(payments) > 50:
            story.append(Paragraph(
                f"* Showing first 50 of {len(payments)} payments",
                self.styles['Footer']
            ))
        
        return story
    
    def _get_status_style(self, status: str):
        """Get appropriate style for status text"""
        if status.lower() == 'successful':
            return self.styles['StatusSuccess']
        elif status.lower() == 'failed':
            return self.styles['StatusFailed']
        else:
            return self.styles['StatusPending']
    
    def _format_date(self, date_str: str) -> str:
        """Format date string for display"""
        try:
            if date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%d %b %H:%M')
            return ''
        except:
            return date_str[:16] if date_str else ''
    
    def _create_decorative_line(self) -> Drawing:
        """Create a decorative line with brand colors"""
        from reportlab.graphics.shapes import Line, Drawing
        
        d = Drawing(400, 10)
        # Primary color line
        d.add(Line(0, 5, 200, 5, strokeColor=colors.HexColor(PDFStyles.BRAND_PRIMARY), strokeWidth=2))
        # Secondary color line
        d.add(Line(200, 5, 400, 5, strokeColor=colors.HexColor(PDFStyles.BRAND_SECONDARY), strokeWidth=2))
        return d
    
    def _create_footer(self) -> List:
        """Create report footer"""
        story = []
        story.append(Spacer(1, 0.2*inch))
        
        footer_text = f"""
        <para alignment="center" fontSize="8" textColor="#9CA3AF">
        Naks Yetu - Payment Report<br/>
        Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M')} | Page <pageNumber/>
        </para>
        """
        
        story.append(Paragraph(footer_text, self.styles['Footer']))
        
        return story