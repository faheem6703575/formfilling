import os
import json
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
from openpyxl import load_workbook
import streamlit as st
import zipfile
import io

class BusinessPlanPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=15,
            textColor=colors.darkblue
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        )
        
        self.bold_style = ParagraphStyle(
            'CustomBold',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
    
    def generate_business_plan_pdf(self, session_state):
        """Generate the complete business plan PDF"""
        try:
            # Create PDF buffer
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                                 topMargin=72, bottomMargin=18)
            
            # Build the PDF content
            story = []
            
            # Title page
            story.extend(self.create_title_page())
            story.append(PageBreak())
            
            # Executive Summary
            story.extend(self.create_executive_summary(session_state))
            story.append(PageBreak())
            
            # Technical Description
            story.extend(self.create_technical_description(session_state))
            story.append(PageBreak())
            
            # R&D Activities
            story.extend(self.create_rd_activities(session_state))
            story.append(PageBreak())
            
            # Market Analysis
            story.extend(self.create_market_analysis(session_state))
            story.append(PageBreak())
            
            # SME Eligibility
            story.extend(self.create_sme_eligibility(session_state))
            story.append(PageBreak())
            
            # Project Data Summary
            story.extend(self.create_project_data_summary(session_state))
            story.append(PageBreak())
            
            # Document Status
            story.extend(self.create_document_status(session_state))
            story.append(PageBreak())
            
            # Excel Files Summary
            story.extend(self.create_excel_summary(session_state))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            return None
    
    def create_title_page(self):
        """Create the title page"""
        story = []
        
        # Main title
        title = Paragraph("Business Plan AI Generator", self.title_style)
        story.append(title)
        story.append(Spacer(1, 50))
        
        # Subtitle
        subtitle = Paragraph("Complete Business Plan Report", self.heading_style)
        story.append(subtitle)
        story.append(Spacer(1, 30))
        
        # Generation date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        date_para = Paragraph(date_text, self.body_style)
        story.append(date_para)
        story.append(Spacer(1, 50))
        
        # Company/Project info placeholder
        company_info = Paragraph("AI-Powered Business Plan Generation", self.body_style)
        story.append(company_info)
        
        return story
    
    def create_executive_summary(self, session_state):
        """Create executive summary section"""
        story = []
        
        # Section title
        title = Paragraph("Executive Summary", self.heading_style)
        story.append(title)
        
        # Summary content
        if session_state.get('trl_result'):
            current_idea = session_state.trl_result.get("upgrade_result", {}).get("upgraded_idea", "No idea provided")
            summary_text = f"""
            This business plan presents a TRL {session_state.trl_result.get("trl_level", "4")} validated technology solution 
            with confirmed R&D activities and company eligibility as SME. The project meets all Frascati criteria 
            for R&D funding.
            
            <b>Core Innovation:</b> {current_idea[:300]}...
            """
        else:
            summary_text = "Executive summary will be generated after TRL analysis is completed."
        
        summary_para = Paragraph(summary_text, self.body_style)
        story.append(summary_para)
        
        return story
    
    def create_technical_description(self, session_state):
        """Create technical description section"""
        story = []
        
        # Section title
        title = Paragraph("Technical Description", self.heading_style)
        story.append(title)
        
        # Technical content
        if session_state.get('trl_result'):
            trl_data = session_state.trl_result.get("upgrade_result", {})
            current_idea = trl_data.get("upgraded_idea", "No technical description available")
            
            # TRL Analysis details
            trl_level = session_state.trl_result.get("trl_level", "N/A")
            trl_analysis = f"""
            <b>Technology Readiness Level (TRL):</b> {trl_level}
            
            <b>Technical Description:</b>
            {current_idea}
            """
            
            if trl_data.get("technical_risks"):
                trl_analysis += f"\n\n<b>Technical Risks Identified:</b>\n{trl_data['technical_risks']}"
            
            if trl_data.get("mitigation_strategies"):
                trl_analysis += f"\n\n<b>Risk Mitigation Strategies:</b>\n{trl_data['mitigation_strategies']}"
        else:
            trl_analysis = "Technical description will be generated after TRL analysis is completed."
        
        tech_para = Paragraph(trl_analysis, self.body_style)
        story.append(tech_para)
        
        return story
    
    def create_rd_activities(self, session_state):
        """Create R&D activities section"""
        story = []
        
        # Section title
        title = Paragraph("R&D Activities & Frascati Compliance", self.heading_style)
        story.append(title)
        
        # R&D content
        if session_state.get('frascati_result'):
            frascati_data = session_state.frascati_result
            rd_text = f"""
            <b>Frascati Criteria Assessment:</b>
            
            <b>Basic Research Score:</b> {frascati_data.get('basic_research_score', 'N/A')}
            <b>Applied Research Score:</b> {frascati_data.get('applied_research_score', 'N/A')}
            <b>Experimental Development Score:</b> {frascati_data.get('experimental_development_score', 'N/A')}
            
            <b>Overall R&D Classification:</b> {frascati_data.get('overall_classification', 'N/A')}
            <b>Confidence Level:</b> {frascati_data.get('confidence_level', 'N/A')}
            
            <b>R&D Activities Include:</b>
            • Laboratory validation and testing
            • Prototype development and refinement  
            • Technical risk assessment and mitigation
            • Performance optimization studies
            • Scalability analysis
            """
        else:
            rd_text = "R&D activities will be detailed after Frascati analysis is completed."
        
        rd_para = Paragraph(rd_text, self.body_style)
        story.append(rd_para)
        
        return story
    
    def create_market_analysis(self, session_state):
        """Create market analysis section"""
        story = []
        
        # Section title
        title = Paragraph("Market Analysis & Patent Research", self.heading_style)
        story.append(title)
        
        # Market content
        if session_state.get('market_result'):
            market_data = session_state.market_result
            market_text = f"""
            <b>Market Analysis Results:</b>
            
            <b>Patent Search Results:</b>
            {market_data.get('patent_summary', 'No patent data available')}
            
            <b>Market Saturation Analysis:</b>
            {market_data.get('market_saturation', 'No market saturation data available')}
            
            <b>Competitive Landscape:</b>
            {market_data.get('competitive_analysis', 'No competitive analysis available')}
            """
        else:
            market_text = "Market analysis will be detailed after market research is completed."
        
        market_para = Paragraph(market_text, self.body_style)
        story.append(market_para)
        
        return story
    
    def create_sme_eligibility(self, session_state):
        """Create SME eligibility section"""
        story = []
        
        # Section title
        title = Paragraph("SME Eligibility Assessment", self.heading_style)
        story.append(title)
        
        # SME content
        if session_state.get('sme_result'):
            sme_data = session_state.sme_result
            sme_text = f"""
            <b>SME Eligibility Results:</b>
            
            <b>Company Size Classification:</b> {sme_data.get('company_size', 'N/A')}
            <b>Employee Count:</b> {sme_data.get('employee_count', 'N/A')}
            <b>Annual Turnover:</b> {sme_data.get('annual_turnover', 'N/A')}
            <b>Balance Sheet Total:</b> {sme_data.get('balance_sheet_total', 'N/A')}
            
            <b>Eligibility Status:</b> {sme_data.get('eligibility_status', 'N/A')}
            <b>Confidence Level:</b> {sme_data.get('confidence_level', 'N/A')}
            """
        else:
            sme_text = "SME eligibility assessment will be detailed after SME analysis is completed."
        
        sme_para = Paragraph(sme_text, self.body_style)
        story.append(sme_para)
        
        return story
    
    def create_project_data_summary(self, session_state):
        """Create project data summary section"""
        story = []
        
        # Section title
        title = Paragraph("Project Data Summary", self.heading_style)
        story.append(title)
        
        # Project data content
        if session_state.get('comprehensive_data') and 'final_data' in session_state.comprehensive_data:
            comp_data = session_state.comprehensive_data
            final_data = comp_data.get('final_data', {})
            
            # Create a table of project data
            data_rows = [['Field', 'Value']]
            for field, value in final_data.items():
                if value and str(value).strip():
                    # Truncate long values for PDF
                    display_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    data_rows.append([field.replace('_', ' ').title(), display_value])
            
            if len(data_rows) > 1:  # More than just header
                data_table = Table(data_rows, colWidths=[2*inch, 4*inch])
                data_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(data_table)
            else:
                story.append(Paragraph("No project data available", self.body_style))
        else:
            story.append(Paragraph("Project data will be detailed after data extraction is completed.", self.body_style))
        
        return story
    
    def create_document_status(self, session_state):
        """Create document status section"""
        story = []
        
        # Section title
        title = Paragraph("Document Processing Status", self.heading_style)
        story.append(title)
        
        # Document status content
        if session_state.get('document_results'):
            results = session_state.document_results
            doc_text = """
            <b>Document Processing Results:</b>
            
            """
            
            if results.get("declaration_result", {}).get("success"):
                doc_text += "✅ Declaration Form - Successfully processed\n"
            else:
                doc_text += "❌ Declaration Form - Processing failed\n"
            
            if results.get("mtep_result", {}).get("success"):
                doc_text += "✅ MTEP Business Plan - Successfully processed\n"
            else:
                doc_text += "❌ MTEP Business Plan - Processing failed\n"
            
            if results.get("rd_assessment_result", {}).get("success"):
                doc_text += "✅ R&D Assessment Form - Successfully processed\n"
            else:
                doc_text += "❌ R&D Assessment Form - Processing failed\n"
            
            if results.get("passthrough_result", {}).get("success"):
                doc_text += "✅ Additional Document - Successfully processed\n"
            else:
                doc_text += "❌ Additional Document - Processing failed\n"
        else:
            doc_text = "Document processing status will be available after document filling is completed."
        
        doc_para = Paragraph(doc_text, self.body_style)
        story.append(doc_para)
        
        return story
    
    def create_excel_summary(self, session_state):
        """Create Excel files summary section"""
        story = []
        
        # Section title
        title = Paragraph("Excel Files Generation Summary", self.heading_style)
        story.append(title)
        
        # Excel summary content
        if session_state.get('excel_processing_result'):
            processing_data = session_state.excel_processing_result
            if processing_data.get("success"):
                output_files = processing_data.get("output_files", [])
                excel_text = f"""
                <b>Excel Files Generated Successfully:</b>
                
                """
                for file_info in output_files:
                    excel_text += f"✅ {file_info.get('description', 'Unknown file')}\n"
                    excel_text += f"   - File: {file_info.get('filename', 'N/A')}\n"
                    excel_text += f"   - Status: {file_info.get('status', 'N/A')}\n\n"
            else:
                excel_text = "Excel processing was not completed successfully."
        else:
            excel_text = "Excel files summary will be available after Excel processing is completed."
        
        excel_para = Paragraph(excel_text, self.body_style)
        story.append(excel_para)
        
        return story
    
    def create_zip_with_all_files(self, session_state):
        """Create a ZIP file containing the PDF and all generated Excel files"""
        try:
            # Create ZIP buffer
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add the business plan PDF
                pdf_buffer = self.generate_business_plan_pdf(session_state)
                if pdf_buffer:
                    zip_file.writestr("Business_Plan_Complete.pdf", pdf_buffer.getvalue())
                
                # Add Excel files from output directory
                output_dir = "code/output"
                if os.path.exists(output_dir):
                    for filename in os.listdir(output_dir):
                        if filename.endswith('.xlsx'):
                            file_path = os.path.join(output_dir, filename)
                            zip_file.write(file_path, f"Excel_Files/{filename}")
                
                # Add any other relevant files
                if session_state.get('document_results'):
                    # Add document processing results as JSON
                    doc_results = session_state.document_results
                    zip_file.writestr("Document_Results.json", json.dumps(doc_results, indent=2))
                
                if session_state.get('comprehensive_data'):
                    # Add project data as JSON
                    comp_data = session_state.comprehensive_data
                    zip_file.writestr("Project_Data.json", json.dumps(comp_data, indent=2))
            
            zip_buffer.seek(0)
            return zip_buffer
            
        except Exception as e:
            st.error(f"Error creating ZIP file: {str(e)}")
            return None

def download_button(label, data, file_name, mime_type):
    """Create a download button for Streamlit"""
    return st.download_button(
        label=label,
        data=data,
        file_name=file_name,
        mime=mime_type
    )

def main():
    """Main function for testing the PDF generator"""
    st.title("Business Plan PDF Generator")
    
    # Initialize generator
    generator = BusinessPlanPDFGenerator()
    
    # Create sample session state for testing
    sample_session = {
        'trl_result': {
            'trl_level': '4',
            'upgrade_result': {
                'upgraded_idea': 'Sample innovative technology solution for renewable energy optimization.'
            }
        },
        'frascati_result': {
            'basic_research_score': '85%',
            'applied_research_score': '90%',
            'experimental_development_score': '88%',
            'overall_classification': 'Applied Research',
            'confidence_level': 'High'
        }
    }
    
    # Generate PDF
    if st.button("Generate Sample PDF"):
        pdf_buffer = generator.generate_business_plan_pdf(sample_session)
        if pdf_buffer:
            download_button(
                "Download Sample PDF",
                pdf_buffer.getvalue(),
                "Sample_Business_Plan.pdf",
                "application/pdf"
            )
    
    # Generate ZIP
    if st.button("Generate Sample ZIP"):
        zip_buffer = generator.create_zip_with_all_files(sample_session)
        if zip_buffer:
            download_button(
                "Download Sample ZIP",
                zip_buffer.getvalue(),
                "Sample_Business_Plan_Complete.zip",
                "application/zip"
            )

if __name__ == "__main__":
    main()
