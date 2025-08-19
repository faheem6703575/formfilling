import PyPDF2
import docx
from io import BytesIO

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(uploaded_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(uploaded_file):
        """Extract text from Word document"""
        try:
            doc = docx.Document(BytesIO(uploaded_file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    @staticmethod
    def extract_text_from_file(uploaded_file):
        """Extract text based on file type"""
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            return DocumentProcessor.extract_text_from_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DocumentProcessor.extract_text_from_docx(uploaded_file)
        elif file_type == "text/plain":
            return uploaded_file.read().decode('utf-8')
        else:
            return f"Unsupported file type: {file_type}"
