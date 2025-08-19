# # ============================================================================
# # agents/document_filling_agent.py (NEW - Integrated from doc1.py + doc4.py)
# # ============================================================================
# from utils.ai_helper import AIHelper
# from docx import Document
# import tempfile
# import os
# from datetime import datetime
# import re
# from io import BytesIO

# class DocumentFillingAgent:
#     def __init__(self):
#         self.ai_helper = AIHelper()
    
#     def analyze_rd_priority(self, business_idea):
#         """Analyze business idea and select appropriate R&D priority"""
#         prompt = f"""
#         Analyze this business idea and select the most appropriate Lithuanian R&D priority:
        
#         Business Idea: {business_idea}
        
#         Available priorities:
#         1. "Health technologies and biotechnologies" - for medical, healthcare, biotech projects
#         2. "New production processes, materials and technologies" - for manufacturing, materials, energy projects  
#         3. "Information and communication technologies" - for AI, software, ICT projects
        
#         For the selected category, also choose the most appropriate subtopic:
        
#         Health subtopics:
#         - "Molecular technologies for medicine and biopharmaceuticals"
#         - "Advanced applied technologies for personal and public health"
#         - "Advanced medical engineering for early diagnosis and treatment"
#         - "Safe food and sustainable agro-biological resources"
        
#         Production subtopics:
#         - "Photonics and laser technologies"
#         - "Advanced materials and structures"
#         - "Flexible technologies for product development"
#         - "Energy efficiency, smartness"
#         - "Renewable energy sources"
        
#         ICT subtopics:
#         - "Artificial intelligence, big and distributed data"
#         - "Internet of Things"
#         - "Cyber security"
#         - "Financial technologies and blockchains"
#         - "Audiovisual media technologies and social innovation"
#         - "Intelligent transport systems"
        
#         Return exactly this format:
#         PROJECT_TYPE: [chosen main category]
#         PROJECT_SUBTOPIC: [chosen subtopic]
#         """
        
#         response = self.ai_helper.generate_response(prompt)
        
#         # Parse response
#         project_type = "Information and communication technologies"  # Default
#         project_subtopic = "Artificial intelligence, big and distributed data"  # Default
        
#         lines = response.split('\n')
#         for line in lines:
#             if 'PROJECT_TYPE:' in line:
#                 project_type = line.split('PROJECT_TYPE:')[1].strip()
#             elif 'PROJECT_SUBTOPIC:' in line:
#                 project_subtopic = line.split('PROJECT_SUBTOPIC:')[1].strip()
        
#         return {
#             'PROJECT_TYPE': project_type,
#             'PROJECT_SUBTOPIC': project_subtopic
#         }
    
#     def fill_declaration_document(self, uploaded_file, company_data):
#         """Fill Document 1: Declaration Form (using doc1.py logic)"""
#         # Save uploaded file temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             tmp_path = tmp_file.name
        
#         try:
#             # Load the existing document
#             doc = Document(tmp_path)
            
#             # Extract company information
#             company_name = company_data.get('company_name', 'TechInnovate Solutions Ltd')
#             company_code = company_data.get('registration_number', '123456789')
#             completion_date = datetime.now().strftime("%d.%m.%Y")
            
#             # Fill the date at the top
#             date_filled = False
#             for paragraph in doc.paragraphs:
#                 text = paragraph.text
#                 if "date of completion" in text.lower():
#                     # Replace underscores with the date
#                     new_text = re.sub(r'_{3,}', completion_date, text)
#                     if new_text != text:
#                         paragraph.text = new_text
#                         date_filled = True
#                         break
            
#             # If not found, look for any paragraph with multiple underscores near the top
#             if not date_filled:
#                 for i, paragraph in enumerate(doc.paragraphs[:10]):
#                     text = paragraph.text
#                     if re.search(r'_{10,}', text) and len(text.strip()) < 100:
#                         new_text = re.sub(r'_{10,}', completion_date, text)
#                         paragraph.text = new_text
#                         date_filled = True
#                         break
            
#             # Fill the table with company information
#             for table in doc.tables:
#                 rows_list = list(table.rows)
                
#                 for row_idx, row in enumerate(rows_list):
#                     row_text = ' '.join([cell.text for cell in row.cells]).strip()
                    
#                     # Company name field
#                     if "Name of the declaring undertaking" in row_text:
#                         if row_idx + 1 < len(rows_list):
#                             next_row = rows_list[row_idx + 1]
#                             for cell in next_row.cells:
#                                 if cell.text.strip() == "" or len(cell.text.strip()) < 5:
#                                     cell.text = "      " + company_name
#                                     break
                    
#                     # Company code field
#                     elif "Code of the declaring company" in row_text:
#                         if row_idx + 1 < len(rows_list):
#                             next_row = rows_list[row_idx + 1]
#                             for cell in next_row.cells:
#                                 if cell.text.strip() == "" or len(cell.text.strip()) < 5:
#                                     cell.text = "      " + company_code
#                                     break
            
#             # Fill signature area
#             for paragraph in doc.paragraphs:
#                 text = paragraph.text
#                 if "position of the manager" in text.lower() or ("signature" in text.lower() and "_" in text):
#                     manager_position = "CEO"
#                     manager_name = "John Smith"
#                     signature_line = f"{manager_position}                                    {manager_name}"
#                     new_text = re.sub(r'_{20,}.*?_{10,}', signature_line, text)
#                     if new_text != text:
#                         paragraph.text = new_text
            
#             # Save to BytesIO
#             doc_bytes = BytesIO()
#             doc.save(doc_bytes)
#             doc_bytes.seek(0)
            
#             return {
#                 "success": True,
#                 "filled_document": doc_bytes,
#                 "filename": f"filled_declaration_{company_name.replace(' ', '_')}.docx",
#                 "preview": f"Declaration filled for {company_name} (Code: {company_code})"
#             }
            
#         except Exception as e:
#             return {
#                 "success": False,
#                 "error": f"Error filling declaration document: {str(e)}"
#             }
#         finally:
#             # Clean up
#             try:
#                 os.unlink(tmp_path)
#             except:
#                 pass
    
#     def fill_assessment_document(self, uploaded_file, business_idea, company_data):
#         """Fill Document 2: R&D Assessment Form (using doc4.py logic)"""
#         # Save uploaded file temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             tmp_path = tmp_file.name
        
#         try:
#             # Load the existing document
#             doc = Document(tmp_path)
            
#             # Analyze R&D priority
#             priority_data = self.analyze_rd_priority(business_idea)
#             project_type = priority_data['PROJECT_TYPE']
#             project_subtopic = priority_data['PROJECT_SUBTOPIC']
            
#             # Calculate values based on company data
#             employee_count = company_data.get('employees', 45)
#             research_jobs_total = max(1, int(employee_count * 0.15))
#             jobs_during_project = max(1, int(research_jobs_total * 0.6))
#             jobs_after_project = research_jobs_total - jobs_during_project
            
#             # Estimate R&D expenditure
#             if employee_count < 20:
#                 rd_2022, rd_2023 = "50000", "75000"
#             elif employee_count < 50:
#                 rd_2022, rd_2023 = "150000", "200000"
#             else:
#                 rd_2022, rd_2023 = "300000", "400000"
            
#             # Fill tables with data
#             for table in doc.tables:
#                 rows_list = list(table.rows)
                
#                 # Handle R&D priority selection (checkboxes)
#                 for row_idx, row in enumerate(rows_list):
#                     row_text = ' '.join([cell.text for cell in row.cells]).strip()
                    
#                     # Mark main priority checkbox
#                     if project_type in row_text and any(x in row_text for x in ["1.1.", "1.2.", "1.3."]):
#                         for cell in row.cells:
#                             if '□' in cell.text and len(cell.text.strip()) < 5:
#                                 cell.text = '☑'
#                                 break
                    
#                     # Mark subtopic checkbox
#                     elif project_subtopic.lower() in row_text.lower():
#                         for cell in row.cells:
#                             if '□' in cell.text and len(cell.text.strip()) < 5:
#                                 cell.text = '☑'
#                                 break
                
#                 # Handle R&D expenditure table
#                 for row_idx, row in enumerate(rows_list):
#                     row_text = ' '.join([cell.text for cell in row.cells]).strip()
                    
#                     if "For 2022" in row_text and "For 2023" in row_text:
#                         if row_idx + 1 < len(rows_list):
#                             data_row = rows_list[row_idx + 1]
#                             cells = list(data_row.cells)
#                             if len(cells) >= 2:
#                                 if cells[0].text.strip() == "":
#                                     cells[0].text = rd_2022
#                                 if cells[1].text.strip() == "":
#                                     cells[1].text = rd_2023
                
#                 # Handle research jobs table
#                 for row_idx, row in enumerate(rows_list):
#                     row_text = ' '.join([cell.text for cell in row.cells]).strip()
                    
#                     if "Total number of research jobs created" in row_text:
#                         if row_idx + 1 < len(rows_list):
#                             data_row = rows_list[row_idx + 1]
#                             cells = list(data_row.cells)
#                             if len(cells) >= 3:
#                                 if cells[0].text.strip() == "":
#                                     cells[0].text = str(research_jobs_total)
#                                 if cells[1].text.strip() == "":
#                                     cells[1].text = str(jobs_during_project)
#                                 if cells[2].text.strip() == "":
#                                     cells[2].text = str(jobs_after_project)
            
#             # Fill signature area
#             for paragraph in doc.paragraphs:
#                 text = paragraph.text
#                 if "title of manager" in text.lower() and "signature" in text.lower():
#                     manager_title = "CEO"
#                     manager_name = "John Smith"
#                     new_text = text.replace("(title of manager or person authorised by him/her)", manager_title)
#                     new_text = new_text.replace("(name and surname)", manager_name)
#                     new_text = new_text.replace("(signature)", "[Signature]")
#                     paragraph.text = new_text
            
#             # Save to BytesIO
#             doc_bytes = BytesIO()
#             doc.save(doc_bytes)
#             doc_bytes.seek(0)
            
#             return {
#                 "success": True,
#                 "filled_document": doc_bytes,
#                 "filename": f"filled_assessment_{project_type.replace(' ', '_')}.docx",
#                 "preview": f"R&D Priority: {project_subtopic}, Research Jobs: {research_jobs_total}, R&D 2023: €{rd_2023}"
#             }
            
#         except Exception as e:
#             return {
#                 "success": False,
#                 "error": f"Error filling assessment document: {str(e)}"
#             }
#         finally:
#             # Clean up
#             try:
#                 os.unlink(tmp_path)
#             except:
#                 pass
    
#     def process_documents(self, declaration_file, assessment_file, business_idea, company_data):
#         """Process both documents"""
#         results = {}
        
#         # Fill declaration document
#         if declaration_file:
#             results["declaration_result"] = self.fill_declaration_document(declaration_file, company_data)
        
#         # Fill assessment document
#         if assessment_file:
#             results["assessment_result"] = self.fill_assessment_document(assessment_file, business_idea, company_data)
        
#         return results