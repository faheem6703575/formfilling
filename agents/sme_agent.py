# ============================================================================
# Fixed agents/sme_agent.py
# ============================================================================
from utils.ai_helper import AIHelper
from utils.document_processor import DocumentProcessor
from config import SME_CRITERIA
import json
import re

class SMEAgent:
    def __init__(self):
        self.ai_helper = AIHelper()
        self.doc_processor = DocumentProcessor()
        self.criteria = SME_CRITERIA
    
    def extract_sme_data(self, document_text):
        """Extract SME data from uploaded document"""
        print(f"Extracting data from: {document_text[:200]}...")
        
        prompt = f"""
        Extract SME (Small and Medium Enterprise) information from this document text.
        
        Document content:
        {document_text}
        
        Extract these specific values:
        1. Company name
        2. Registration number  
        3. Number of employees (look for employees, staff, personnel, workforce)
        4. Annual turnover in EUR (look for turnover, revenue, sales)
        5. Annual balance sheet total in EUR
        6. Business activities or description
        
        IMPORTANT: Return ONLY this JSON format (no extra text):
        {{
            "company_name": "TechInnovate Solutions Ltd",
            "registration_number": "123456789", 
            "employees": 45,
            "annual_turnover": 2500000,
            "balance_sheet_total": 1800000,
            "business_activities": "Technology solutions"
        }}
        
        Rules:
        - Extract numbers only (remove €, EUR, commas)
        - If employees shows "(annual work units)", use the number before it
        - Convert €2,500,000 to 2500000
        - If information not found, use null
        """
        
        response = self.ai_helper.generate_response(prompt, max_tokens=500)
        print(f"AI Response: {response}")
        
        # Try to extract JSON
        result = self.extract_json_from_response(response)
        
        if result and self.validate_sme_data(result):
            return result
        else:
            # Fallback: manual text parsing
            print("JSON extraction failed, using manual parsing...")
            return self.manual_text_extraction(document_text)
    
    def extract_json_from_response(self, response_text):
        """Extract JSON data from AI response"""
        try:
            # Clean the response
            response_text = response_text.strip()
            
            # Try to find JSON content between ```json and ```
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                return json.loads(json_str)
            
            # Try to find JSON content between { and }
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # Try to parse entire response as JSON
            return json.loads(response_text)
            
        except Exception as e:
            print(f"JSON extraction error: {e}")
            return None
    
    def validate_sme_data(self, result):
        """Validate that the extracted data has the correct structure"""
        if not isinstance(result, dict):
            return False
        
        required_fields = ["company_name", "registration_number", "employees", 
                          "annual_turnover", "balance_sheet_total", "business_activities"]
        
        for field in required_fields:
            if field not in result:
                return False
        
        return True
    
    def manual_text_extraction(self, document_text):
        """Fallback: manually extract data using regex patterns"""
        print("Using manual extraction...")
        
        # Clean text for better parsing
        text = document_text.replace('\n', ' ').replace('\r', ' ')
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        
        # Extract company name
        company_name = self.extract_company_name(text)
        
        # Extract registration number
        registration_number = self.extract_registration_number(text)
        
        # Extract employees
        employees = self.extract_employees(text)
        
        # Extract turnover
        annual_turnover = self.extract_turnover(text)
        
        # Extract balance sheet
        balance_sheet_total = self.extract_balance_sheet(text)
        
        # Extract business activities
        business_activities = self.extract_business_activities(text)
        
        return {
            "company_name": company_name,
            "registration_number": registration_number,
            "employees": employees,
            "annual_turnover": annual_turnover,
            "balance_sheet_total": balance_sheet_total,
            "business_activities": business_activities
        }
    
    def extract_company_name(self, text):
        """Extract company name"""
        patterns = [
            r'Company Name:?\s*([^-\n]+)',
            r'Business Name:?\s*([^-\n]+)',
            r'Enterprise:?\s*([^-\n]+)',
            r'Company:?\s*([^-\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_registration_number(self, text):
        """Extract registration number"""
        patterns = [
            r'Registration Number:?\s*([A-Za-z0-9]+)',
            r'Registration:?\s*([A-Za-z0-9]+)',
            r'Number:?\s*([0-9]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_employees(self, text):
        """Extract number of employees"""
        patterns = [
            r'Number of Employees:?\s*(\d+)',
            r'Employees:?\s*(\d+)',
            r'Staff:?\s*(\d+)',
            r'Personnel:?\s*(\d+)',
            r'(\d+)\s*employees',
            r'(\d+)\s*people',
            r'(\d+)\s*staff',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def extract_turnover(self, text):
        """Extract annual turnover"""
        patterns = [
            r'Annual Turnover:?\s*€?([0-9,]+)',
            r'Turnover:?\s*€?([0-9,]+)',
            r'Revenue:?\s*€?([0-9,]+)',
            r'Sales:?\s*€?([0-9,]+)',
            r'€([0-9,]+,000)',
            r'([0-9,]+,000)\s*euros?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                number_str = match.group(1).replace(',', '')
                try:
                    return int(number_str)
                except:
                    continue
        
        return None
    
    def extract_balance_sheet(self, text):
        """Extract balance sheet total"""
        patterns = [
            r'Balance Sheet Total:?\s*€?([0-9,]+)',
            r'Balance Sheet:?\s*€?([0-9,]+)',
            r'Total Assets:?\s*€?([0-9,]+)',
            r'Assets:?\s*€?([0-9,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                number_str = match.group(1).replace(',', '')
                try:
                    return int(number_str)
                except:
                    continue
        
        return None
    
    def extract_business_activities(self, text):
        """Extract business activities"""
        patterns = [
            r'Business Activities:?\s*([^-\n]+)',
            r'Activities:?\s*([^-\n]+)',
            r'Industry:?\s*([^-\n]+)',
            r'Sector:?\s*([^-\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Technology solutions"  # Default
    
    def validate_sme_eligibility(self, sme_data):
        """Validate SME eligibility based on extracted data"""
        print(f"Validating SME data: {sme_data}")
        
        validation_result = {
            "eligible": True,
            "criteria_met": [],
            "criteria_failed": [],
            "missing_data": []
        }
        
        # Check employees
        if sme_data.get("employees") is not None:
            if sme_data["employees"] <= self.criteria["max_employees"]:
                validation_result["criteria_met"].append(f"Employees: {sme_data['employees']} ≤ {self.criteria['max_employees']}")
            else:
                validation_result["criteria_failed"].append(f"Too many employees: {sme_data['employees']} > {self.criteria['max_employees']}")
                validation_result["eligible"] = False
        else:
            validation_result["missing_data"].append("Number of employees")
        
        # Check turnover
        if sme_data.get("annual_turnover") is not None:
            if sme_data["annual_turnover"] <= self.criteria["max_turnover"]:
                validation_result["criteria_met"].append(f"Turnover: €{sme_data['annual_turnover']:,} ≤ €{self.criteria['max_turnover']:,}")
            else:
                validation_result["criteria_failed"].append(f"Turnover too high: €{sme_data['annual_turnover']:,} > €{self.criteria['max_turnover']:,}")
                validation_result["eligible"] = False
        else:
            validation_result["missing_data"].append("Annual turnover")
        
        # Check balance sheet
        if sme_data.get("balance_sheet_total") is not None:
            if sme_data["balance_sheet_total"] <= self.criteria["max_balance_sheet"]:
                validation_result["criteria_met"].append(f"Balance sheet: €{sme_data['balance_sheet_total']:,} ≤ €{self.criteria['max_balance_sheet']:,}")
            else:
                validation_result["criteria_failed"].append(f"Balance sheet too high: €{sme_data['balance_sheet_total']:,} > €{self.criteria['max_balance_sheet']:,}")
                validation_result["eligible"] = False
        else:
            validation_result["missing_data"].append("Balance sheet total")
        
        return validation_result
    
    def generate_eligibility_report(self, sme_data, validation_result):
        """Generate a comprehensive eligibility report"""
        report = {
            "company_info": sme_data,
            "eligibility_status": "ELIGIBLE" if validation_result["eligible"] else "NOT ELIGIBLE",
            "validation_details": validation_result,
            "recommendations": []
        }
        
        # Add recommendations based on results
        if validation_result["missing_data"]:
            report["recommendations"].append("Provide missing documentation for complete assessment")
        
        if validation_result["criteria_failed"]:
            report["recommendations"].append("Company does not meet SME criteria for this funding program")
        
        if validation_result["eligible"]:
            report["recommendations"].append("Company meets SME eligibility requirements - proceed with application")
        
        return report
    
    def process_document(self, uploaded_file):
        """Main SME processing function"""
        try:
            # Extract text from document
            document_text = self.doc_processor.extract_text_from_file(uploaded_file)
            print(f"Document text extracted: {document_text[:300]}...")
            
            if document_text.startswith("Error"):
                return {"error": document_text}
            
            # Extract SME data
            sme_data = self.extract_sme_data(document_text)
            print(f"Extracted SME data: {sme_data}")
            
            # Validate eligibility
            validation_result = self.validate_sme_eligibility(sme_data)
            
            # Generate report
            report = self.generate_eligibility_report(sme_data, validation_result)
            
            return {
                "success": True,
                "document_text": document_text[:500] + "..." if len(document_text) > 500 else document_text,
                "extracted_data": sme_data,
                "validation": validation_result,
                "report": report
            }
            
        except Exception as e:
            print(f"SME processing error: {e}")
            return {"error": f"Processing failed: {str(e)}"}