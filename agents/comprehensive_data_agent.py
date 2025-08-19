from utils.ai_helper import AIHelper
import json
import re
from datetime import datetime
import random

class ComprehensiveDataAgent:
    def __init__(self):
        self.ai_helper = AIHelper()
        
        # Define all required fields with categories (UPDATED)
        self.required_fields = {
        "company_info": [
            "COMPANY_NAME", "COMPANY_CODE", "MANAGER_POSITION", "MANAGER_NAME", 
            "COMPLETION_DATE", "MAIN_ACTIVITY", "ACTIVITY_PERCENTAGE", "CESE_CLASS",
            "N_L_E", "I_C", "Sharehol", "A_S_Ns", "SHARE_HS",
            "S_H", "S_I", "S_S", "MANAGER_TITLE","SUMMARY_1","INNOVATIVENESS","E_S_RES","E_S_R&D",
            "E_S_R", "A_S_RES", "A_S_R&D", "A_S_R", "A_S_P", "N_E", "N_R", "N_T", "N_W_T", "N_P_T", 
            "LITERATURE_REVIEW","IPR", "COMMERCIALIZATION", "COLLABORATION", "LITERATURE_SOURCES",
            # ADD MISSING FIELDS:
            "RD_JUSTIFICATION_1", "RD_JUSTIFICATION_2", "RD_JUSTIFICATION_3", "RD_JUSTIFICATION_4", "RD_JUSTIFICATION_5",
            "MARKET_ANALYSIS", "PRODUCT_PRICING", "PRICING_JUSTIFICATION", "RD_ACTIVITIES_PLAN"
        ],
        "project_details": [
            "PRODUCT_NAME", "JUS_PRO", "NOVELTY_LEVEL", "JUS_R_D_I", "RD_PRIORITY",
            "RESEARCH_AREA", "PROJECT_KEYWORDS","PROJECT_TYPE", "PROJECT_SUBTOPIC",
            "N_As", "F_Os", "S_Us", "W_R_Ds","PRODUCTS_OFFERED","PER_SALES"
        ],
        "financial_data": [
            "RD_BUDGET",  "REVENUE_PROJECTION", "REVENUE_RATIO",
            "RD_EXPENDITURE_2022", "RD_EXPENDITURE_2023"
        ],
        "technical_info": [
            "CURRENT_TPL", "TARGET_TPL", "TPL_JUSTIFICATION", "PROJECT_IMPACT_TITLE",
            "PROJECT_START_MONTH", "PROJECT_COMPLETION_MONTH", "PROJECT_IMPACT_DESCRIPTION"
        ],
        "competition_jobs": [
            "COMPETITOR_M", "COMPETITOR_MARKET_SHARE", "TOTAL_RESEARCH_JOBS", 
            "JOBS_DURING_PROJECT", "JOBS_AFTER_PROJECT"
        ],
        "risk_assessment": [
            "RISK_STAGE_1", "RISK_DESCRIPTION_1", "CRITICAL_POINT_1", "MITIGATION_ACTION_1",
            "RISK_STAGE_2", "RISK_DESCRIPTION_2", "CRITICAL_POINT_2", "MITIGATION_ACTION_2",
            "RISK_STAGE_3", "RISK_DESCRIPTION_3", "CRITICAL_POINT_3", "MITIGATION_ACTION_3",
            "RISK_STAGE_4", "RISK_DESCRIPTION_4", "CRITICAL_POINT_4", "MITIGATION_ACTION_4"
        ]
    }
    
    def extract_comprehensive_data(self, processed_business_idea):
        prompt = f"""
        Extract structured information from the business idea below and format responses exactly to match the document structure of the MTEP Business Plan.

        Business Idea: {processed_business_idea}

        CRITICAL INSTRUCTIONS:
        - You MUST extract ALL fields listed below
        - Use EXACTLY this format: FIELD_NAME: extracted_value
        - If information is not available, write "NOT_FOUND"
        - Do NOT skip any field
        - Do NOT add explanations or additional text
        
        MOST IMPORTANT POINT -> Do NOT skip any field
        
        Follow the logical sequence where Section 4.4 literature review forms the foundation for re-examining the idea according to the Frascati Manual, which then informs Section 4.3 justification of R&D activities, which subsequently guides Section 3.1 product descriptions and innovation analysis.

        ------------------------
        SECTION 4.4 An overview of national and international research on product development (FOUNDATION ANALYSIS - Complete this first as it forms the basis for formulating scientific problems, hypotheses and applications):
        ------------------------
        LITERATURE_REVIEW: [Extract and synthesize an overview of national and international research on product development up to 200 words. This analysis will be used to re-examine the idea according to the Frascati Manual and inform all subsequent sections.]

        ------------------------
        SECTION 4.3 Justification of the R&D activities required for product development/improvement (Based on 4.4 studies, develop the scientific problem, hypothesis, uncertainties, and systematic approach):
        ------------------------
        RD_JUSTIFICATION_1: [Extract justification of new or additional knowledge sought - what scientific/technological problems exist for which knowledge is not publicly available]
        RD_JUSTIFICATION_2: [Extract original ideas and hypotheses on which the project is based - what original, non-obvious hypothesis will be tested]
        RD_JUSTIFICATION_3: [Extract description of project uncertainties - likelihood of failing to generate sufficient knowledge, achieve planned results, or meet timeline]
        RD_JUSTIFICATION_4: [Extract systematic nature of planned activities - how activities are coherent, logical, and comply with SMART principles]
        RD_JUSTIFICATION_5: [Extract how results will be replicable and transferable - what documentation will enable knowledge transfer]

        ------------------------
        SECTION 3 PRODUCTS FOR WHICH FUNDING IS REQUESTED (Using knowledge from 4.3 about problems solved and technical solutions):
        ------------------------
            ------------------------
            3.1 Description of the new or substantially improved product to be developed:
            ------------------------
                ------------------------
                SECTION 3.1.1: Describe the product's unique features, technical solutions, and how it differs from similar products on the market. Use knowledge from 4.3 about what problems it solves and what technical solutions are needed:
                ------------------------
                INNOVATIVENESS: [Extract the innovative aspects of the product or service, how it differs from existing solutions, and its potential impact on the market. Base this on problems identified in 4.3.]

                ------------------------
                SECTION 3.1.2: The level of novelty of the product(s) created by the project (Determined by analysis from 4.4 and 3.1.1 on the Oslo Manual scale - justify that the idea is novel at the global level):
                ------------------------
                PRODUCT_NAME: [Extract product name or use "NOT_FOUND"]
                NOVELTY_LEVEL: [Determine: "company level", "market level", "global level" or "NOT_FOUND" - must justify global level novelty based on literature analysis]
                JUS_PRO: [Extract justification for product novelty using Oslo Manual criteria and literature analysis]

                ------------------------
                SECTION 3.1.3: Justify how the project supports the RDI (Smart Specialisation) Concept (Assignment to previously analysed area from 4.4, 4.3, 3.1 - use MTEPI priorities approved by Lithuanian Government Resolution No. 835 of 17 August 2022):
                ------------------------
                RD_PRIORITY: [Choose from Lithuanian priorities: "Health technologies", "Production processes", "Information and communication technologies" or "NOT_FOUND"]
                JUS_R_D_I: [Extract how the project matches any R&D&I priority and its theme, based on previous analysis]

                ------------------------
                SECTION 3.1.4: Research area(s) of the project (Classification from 3.1.1 analysis - choose according to Lithuanian Ministry Order No V-93 of 6 February 2019):
                ------------------------
                RESEARCH_AREA: [Extract research fields based on product classification or use "NOT_FOUND"]
                
                ------------------------
                SECTION 3.1.5: Project keywords (Derived from 3.1.1, 4.4 literature review and 4.3 R&D justification using NLP processing):
                ------------------------
                PROJECT_KEYWORDS: [Extract ALL relevant keywords from the text, especially technical terms from literature and R&D analysis, separated by commas]

        ------------------------
        SECTION 4.5 A plan of the R&D activities (Formulate based on 4.3 uncertainties and hypothesis testing, 4.4 literature, and 4.2 people - describe specific tasks and required hours):
        ------------------------
        PROJECT_IMPACT_TITLE: [Extract project impact title or use "NOT_FOUND"]
        PROJECT_START_MONTH: [Extract project start month or use "NOT_FOUND"]
        PROJECT_COMPLETION_MONTH: [Extract project completion month or use "NOT_FOUND"]      
        CURRENT_TPL: [Extract current Technology Readiness Level or use "NOT_FOUND"]
        TARGET_TPL: [Extract target Technology Readiness Level or use "NOT_FOUND"]
        RD_ACTIVITIES_PLAN: [Extract detailed R&D activities plan describing what tasks need to be performed and estimated hours required]

        ------------------------
        SECTION 4.2 Project implementation team (Based on 4.5 activities, determine what positions are needed, when, and how many working hours - fill iteratively with 4.5):
        ------------------------
            -------------------------
            SECTION 4.2.1: Existing staff of the applicant and the partner who will be responsible for carrying out the R&D activities:
            -------------------------
            E_S_RES: [Extract Responsibilities based on 4.5 activities]
            E_S_R&D: [Extract Responsibilities for R&D activities from 4.5 plan]
            E_S_R: [Extract Minimum qualification requirements for staff]

            -------------------------
            SECTION 4.2.2: Additional staff of the applicant and the partner are needed to carry out the R&D activities:
            -------------------------
            A_S_RES: [Extract Responsibilities for new staff based on 4.5]
            A_S_R&D: [Extract Responsibilities for R&D activities for new hires]
            A_S_R: [Extract Minimum qualification requirements for additional staff]
            A_S_P: [Extract Period (year and month) of planned recruitment]

            -------------------------
            SECTION 4.2.3: The tasks to be carried out by each R&D personnel (Take hours from 4.5 and allocate to specific personnel):
            -------------------------
            N_E: [Extract Name of employee Surname (if known)]
            N_R: [Extract Responsibilities from 4.5 activities]
            N_T: [Extract Task(s) to be carried out from 4.5 plan]
            N_W_T: [Extract Number of working hours per task from 4.5 estimates]
            N_P_T: [Extract Result of planned tasks from 4.5 outputs]

        ------------------------
        SECTION 4.6 Intellectual property issues (Evaluate after analysis of innovativeness 3.1.1 and literature 4.4):
        ------------------------
        IPR: [Extract Intellectual property issues for the products to be produced, including patenting details based on innovation and literature analysis]

        ------------------------
        SECTION 4.7 Product market development plan (Market readiness activities after R&D completion but before production start):
        ------------------------
        COMMERCIALIZATION: [Extract commercialization strategy focusing on testing, standardisation, production capacity design, user instructions - NOT product design or equipment acquisition]

        ------------------------
        SECTION 4.8 Risk assessment of the R&D project (Based on sequence of activities in 4.5 and uncertainties in 4.3):
        ------------------------
        RISK_STAGE_1: [Extract first risk stage/phase based on 4.5 sequence]
        RISK_DESCRIPTION_1: [Extract first risk description based on 4.3 uncertainties]
        CRITICAL_POINT_1: [Extract first critical point from 4.5 activities]
        MITIGATION_ACTION_1: [Extract first mitigation action]
        RISK_STAGE_2: [Extract second risk stage/phase based on 4.5 sequence]
        RISK_DESCRIPTION_2: [Extract second risk description based on 4.3 uncertainties]
        CRITICAL_POINT_2: [Extract second critical point from 4.5 activities]
        MITIGATION_ACTION_2: [Extract second mitigation action]
        RISK_STAGE_3: [Extract third risk stage/phase based on 4.5 sequence]
        RISK_DESCRIPTION_3: [Extract third risk description based on 4.3 uncertainties]
        CRITICAL_POINT_3: [Extract third critical point from 4.5 activities]
        MITIGATION_ACTION_3: [Extract third mitigation action]
        RISK_STAGE_4: [Extract fourth risk stage/phase based on 4.5 sequence]
        RISK_DESCRIPTION_4: [Extract fourth risk description based on 4.3 uncertainties]
        CRITICAL_POINT_4: [Extract fourth critical point from 4.5 activities]
        MITIGATION_ACTION_4: [Extract fourth mitigation action]

        ------------------------
        SECTION 4.9 The feasibility and benefits of the partnership (Define boundaries between applicant and partner work - basis for 4.2 staff listing):
        ------------------------
        COLLABORATION: [Extract the feasibility and benefits of the partnership, defining what applicant vs partner will do]

        ------------------------
        SECTION 5 DESCRIPTION OF HOW THE PRODUCT IS PLACED ON THE MARKET (Market study needed, possibly parallel with 4.4):
        ------------------------
            ------------------------
            SECTION 5.1 Market analysis (Conduct market study parallel with literature review):
            ------------------------
            MARKET_ANALYSIS: [Extract market demand forecast, target consumers, market characteristics including size, growth, seasonal changes, product cycles]
            
            ------------------------
            SECTION 5.2 Main competitors (From same sources as 5.1, plus 3.1.1 innovation analysis):
            ------------------------
            COMPETITOR_M: [Extract main competitor name based on market and innovation analysis]
            COMPETITOR_MARKET_SHARE: [Extract market share percentage from market study]
            
            ------------------------
            SECTION 5.3 Pricing strategy (Suggest pricing based on competitor info 5.2 and product specifics 3.1.1):
            ------------------------
            PRODUCT_PRICING: [Extract suggested pricing strategy based on competitors and product innovation]
            PRICING_JUSTIFICATION: [Extract pricing assumptions and main determining factors]
            
            ------------------------
            SECTION 5.4 Commercialisation potential (Summarise 4.5 TPL progression and evaluate activities):
            ------------------------
            PRODUCT_NAME: [Extract product name]
            CURRENT_TPL: [Extract current Technology Readiness Level from 4.5]
            TARGET_TPL: [Extract target Technology Readiness Level from 4.5]
            TPL_JUSTIFICATION: [Extract justification based on 4.5 activities evaluation]

        ------------------------
        SECTION 2: DESCRIPTION OF THE LEGAL ENTITY AND ITS ACTIVITIES (Actual data for SME verification - can be filled earlier):
        ------------------------
            ------------------------
            2.1 Information on shareholders: name, company code/name, number of shares held :
            ------------------------
                ------------------------
                SECTION 2.1.1: Information on the applicant's shareholders and shareholders' shareholders (up to natural persons):
                ------------------------
                A_S_Ns: [Extract Shareholder name]
                COMPANY_CODE: [Extract Company code*]
                SHARE_HS: [Extract Shareholding, %]

                ------------------------
                SECTION 2.1.2: Information on the legal entities in which the applicant holds shares:
                ------------------------                                       
                N_L_E: [Extract Name of the legal entity]
                I_C: [Extract Identification code]
                Sharehol: [Extract Shareholding, %]

                ------------------------
                SECTION 2.1.3: Information on the legal entities in which the applicant's shareholders hold shares:
                ------------------------                  
                S_H: [Extract Name of the legal entity]
                S_I: [Extract Identification code]
                S_S: [Extract Shareholding, %]

            ------------------------
            SECTION 2.2: The applicant must list their current business activities using ECC classification:
            ------------------------
            MAIN_ACTIVITY: [Extract Main business activity from ECC classification]
            ACTIVITY_PERCENTAGE: [Extract Share of activity (%) in total company activity]
            CESE_CLASS: [Extract Class of the CESE]
                
            ------------------------
            SECTION 2.3: The products offered by the applicant:
            ------------------------
            PRODUCTS_OFFERED: [Extract Products offered by the applicant]
            PER_SALES: [Extract Percentage of sales]

        ------------------------
        SECTION 6 RESOURCES NEEDED FOR PRODUCT DEVELOPMENT/IMPROVEMENT (Describe equipment, premises, materials needs from 4.5 and available enterprise resources):
        ------------------------
            ------------------------
            SECTION 6.1 A description of the main assets and resources (Most cases will be empty due to administrative burden and depreciation issues):
            ------------------------
            N_As: [Extract the name of the asset used in R&D activities from 4.5 needs]
            F_Os: [Extract the form of ownership for the asset]
            S_Us: [Extract the share or amount of the asset used for R&D]
            W_R_Ds: [Extract which R&D activities the asset will be used for from 4.5]

        ------------------------
        SECTION 7 FINANCIAL PLAN (Evaluate whether revenue achievement is treated as commitment and if priority points given for higher revenue/project ratio):
        ------------------------
            ------------------------
            SECTION 7.1 The ratio of enterprise's projected income (Take most optimistic option if priority points given):
            ------------------------
            REVENUE_PROJECTION: [Extract Planned revenue (P), EUR - use optimistic projection if priority points apply]
            RD_BUDGET: [Extract Eligible project costs (I), EUR]
            REVENUE_RATIO: [Extract Revenue to expenditure ratio (X)* - confirm if commitment required]

        ------------------------
        SECTION 1: SUMMARY (Complete last when all information has been gathered):
        ------------------------
        SUMMARY_1: [Extract and generate a 500 words never less about your company, your innovative product, its market potential, costs, and future plan. Complete this after all other sections are filled.]

        -----------------------
        SECTION 8 SOURCES OF LITERATURE (Generated automatically from 4.4 content):
        ------------------------
        LITERATURE_SOURCES: [Extract Literature sources - generate automatically from Section 4.4 literature review content]

        Now also extract these things for the purpose of the filling of the other documents:
        
        TOTAL_RESEARCH_JOBS: [EXTRACT the total number of research jobs/positions. Look for phrases like "Total Research Jobs:", "Current Research Jobs:", "research positions", "research staff", "R&D personnel", "research team size". Extract the NUMBER only, e.g., "8" or "11"]
        JOBS_DURING_PROJECT: [EXTRACT number of jobs/positions during the project execution. Look for "Jobs During Project:", "positions during", "staff during project", "project team size", "personnel during implementation". Extract the NUMBER only, e.g., "5" or "8"]       
        JOBS_AFTER_PROJECT: [EXTRACT number of jobs/positions after project completion. Look for "Jobs After Project:", "positions after", "permanent positions", "long-term employment", "post-project staff". Extract the NUMBER only, e.g., "12" or "15"]
        COMPANY_NAME: [Extract company name]
        MANAGER_POSITION: [Extract manager position]
        MANAGER_NAME: [Extract manager name]
        COMPLETION_DATE: [Today's date in DD.MM.YYYY format]
        MANAGER_TITLE: [Extract manager title]
        PROJECT_TYPE: [Choose: "Health technologies and biotechnologies", "New production processes, materials and technologies", "Information and communication technologies" or "NOT_FOUND"]
        PROJECT_SUBTOPIC: [Extract specific subtopic or use "NOT_FOUND"]
        RD_EXPENDITURE_2022: [Extract R&D expenditure for 2022 or use "NOT_FOUND"]
        RD_EXPENDITURE_2023: [Extract R&D expenditure for 2023 or use "NOT_FOUND"]
        TPL_JUSTIFICATION: [Extract TPL justification or use "NOT_FOUND"]
        PROJECT_IMPACT_DESCRIPTION: [Extract detailed project impact description or use "NOT_FOUND"]

        """

        try:
            print("DEBUG: Sending request to AI...")
            response = self.ai_helper.generate_response(prompt,max_tokens=32000)  # Increased token limit

            extracted_data = self.parse_extracted_data(response)
            
            print(f"FINAL RESULT: Extracted {len(extracted_data)} fields")
            return extracted_data
        except Exception as e:
            print(f"Error extracting comprehensive data: {e}")
            return self.get_empty_data_structure()
        
    def parse_extracted_data(self, response):
        """COMPLETELY FIXED PARSING METHOD"""
        extracted_data = {}
        
        # Get all valid field names
        all_fields = []
        for category, fields in self.required_fields.items():
            all_fields.extend(fields)
        
        print(f"DEBUG: Looking for {len(all_fields)} fields...")
        print(f"DEBUG: First 10 fields: {all_fields[:10]}")
        
        # Split response into lines
        lines = response.split('\n')
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or ':' not in line:
                continue
                
            # Find the first colon position
            colon_pos = line.find(':')
            if colon_pos == -1:
                continue
                
            # Extract potential field name (everything before first colon)
            potential_field = line[:colon_pos].strip()
            value_part = line[colon_pos + 1:].strip()
            
            # Check if this is actually a field we're looking for
            if potential_field in all_fields:
                # Clean the value
                if value_part.startswith('[') and value_part.endswith(']'):
                    value_part = value_part[1:-1].strip()
                
                # Remove instruction prefixes
                prefixes_to_remove = [
                    "Extract ", "Choose ", "Determine ", "Generate ",
                    "Extract and ", "Choose from ", "Determine: ",
                    "Extract the ", "Choose the ", "Select "
                ]
                
                for prefix in prefixes_to_remove:
                    if value_part.startswith(prefix):
                        value_part = value_part[len(prefix):].strip()
                        break
                
                # Clean up quotes and special characters
                value_part = value_part.strip('"\'`')
                
                # Only add if not "NOT_FOUND" and not empty
                if value_part and value_part != "NOT_FOUND" and len(value_part) > 2:
                    extracted_data[potential_field] = value_part
                    print(f"✓ FOUND {potential_field}: {value_part[:60]}...")
                else:
                    print(f"✗ EMPTY/INVALID value for {potential_field}: '{value_part}'")
            else:
                # Check if it's a field with slight variations
                for field_name in all_fields:
                    if potential_field.lower() == field_name.lower():
                        if value_part and value_part != "NOT_FOUND" and len(value_part) > 2:
                            extracted_data[field_name] = value_part
                            print(f"✓ FOUND (case variation) {field_name}: {value_part[:60]}...")
                        break
        
        print(f"DEBUG: Successfully extracted {len(extracted_data)} out of {len(all_fields)} fields")
        
        # Show what was found
        for field, value in extracted_data.items():
            print(f"EXTRACTED: {field} = {value[:50]}...")
        
        # Show critical missing fields
        critical_fields = [
            'COMPANY_NAME', 'PRODUCT_NAME', 'INNOVATIVENESS', 'RD_PRIORITY',
            'CURRENT_TPL', 'TARGET_TPL', 'LITERATURE_REVIEW', 'SUMMARY_1',
            'RD_JUSTIFICATION_1', 'MARKET_ANALYSIS', 'IPR'
        ]
        
        missing_critical = [f for f in critical_fields if f not in extracted_data]
        if missing_critical:
            print(f"WARNING: Missing critical fields: {missing_critical}")
        
        return extracted_data    
    def get_empty_data_structure(self):
        """Return empty data structure with all fields set to None"""
        empty_data = {}
        for category, fields in self.required_fields.items():
            for field in fields:
                empty_data[field] = None
        return empty_data
    
    def identify_missing_fields(self, extracted_data):
        """Identify which fields are missing and categorize them"""
        missing_fields = {}
        
        for category, fields in self.required_fields.items():
            missing_in_category = []
            for field in fields:
                if field not in extracted_data or extracted_data[field] is None:
                    missing_in_category.append(field)
            
            if missing_in_category:
                missing_fields[category] = missing_in_category
        
        return missing_fields
    
    def get_field_descriptions(self):
        """Get user-friendly descriptions for fields"""
        descriptions = {
            "COMPANY_NAME": "Company name (e.g., 'TechnoSolutions Baltic OÜ')",
            "COMPANY_CODE": "Company registration code (e.g., 'LT123456789')",
            "MANAGER_POSITION": "Manager position (e.g., 'CEO', 'CTO')",
            "MANAGER_NAME": "Manager name (e.g., 'Andrius Kazlauskas')",
            "COMPLETION_DATE": "Completion date (DD.MM.YYYY format)",
            "MAIN_ACTIVITY": "Main business activity description",
            "ACTIVITY_PERCENTAGE": "Activity percentage (e.g., '75')",
            "CESE_CLASS": "CESE classification code (e.g., '62.01')",
            "Name_of_the_legal_entity": "Legal entity name",
            "Identification_code": "Identification code",
            "Shareholding": "Shareholding percentage",
            "A_S_Ns": "Applicant's shareholders names",
            "SHARE_HS": "Shareholding percentage for each shareholder",
            "S_H": "Legal entity name in which applicant's shareholders hold shares",
            "S_I": "Identification code of that legal entity",
            "S_S": "Shareholding percentage held by shareholder in that entity",
            "MANAGER_TITLE": "Manager title",
            "SUMMARY": "200-250 word summary about the company, product, market potential, costs, and future plans",
            "PRODUCT_NAME": "Product or service name",
            "PRODUCT_DESCRIPTION": "Detailed product description",
            "JUS_PRO": "Product novelty justification",
            "NOVELTY_LEVEL": "Novelty level (company/market/global)",
            "RD_PRIORITY": "R&D priority category",
            "JUS_R_D_I": "R&D&I priority justification",
            "RESEARCH_AREA": "Research area (e.g., 'Computer Sciences')",
            "PROJECT_KEYWORDS": "Project keywords separated by commas",
            "N_As": "Asset name (equipment, software, etc.)",
            "F_Os": "Form of ownership (owned, leased, shared)",
            "S_Us": "Share/amount of asset used for R&D",
            "W_R_Ds": "R&D activities the asset will be used for",
            "PROJECT_TYPE": "Project type category",
            "PROJECT_SUBTOPIC": "Specific project subtopic",
            
            "RD_BUDGET": "R&D budget in euros (e.g., '200000')",
            "REVENUE_PROJECTION": "Revenue projection in euros",
            "REVENUE_RATIO": "Revenue to cost ratio",
            "RD_EXPENDITURE_2022": "R&D expenditure for 2022",
            "RD_EXPENDITURE_2023": "R&D expenditure for 2023",
            
            "CURRENT_TPL": "Current Technology Readiness Level",
            "TARGET_TPL": "Target Technology Readiness Level",
            "TPL_JUSTIFICATION": "TPL achievement justification",
            "PROJECT_IMPACT_TITLE": "Project impact title",
            "PROJECT_START_MONTH": "Project start month",
            "PROJECT_COMPLETION_MONTH": "Project completion month",
            "START_TPL_IMPACT": "Starting TPL for impacts",
            "END_TPL_IMPACT": "Ending TPL for impacts",
            "PROJECT_IMPACT_DESCRIPTION": "Detailed project impact description",
            
            "COMPETITOR_M": "Main competitor name",
            "COMPETITOR_MARKET_SHARE": "Competitor market share percentage",
            "TOTAL_RESEARCH_JOBS": "Total research jobs to be created",
            "JOBS_DURING_PROJECT": "Research jobs during project",
            "JOBS_AFTER_PROJECT": "Research jobs after project",
            
            # Risk Assessment fields
            "RISK_STAGE_1": "First project stage/phase",
            "RISK_DESCRIPTION_1": "First risk description",
            "CRITICAL_POINT_1": "First critical point",
            "MITIGATION_ACTION_1": "First risk mitigation action",
            "RISK_STAGE_2": "Second project stage/phase",
            "RISK_DESCRIPTION_2": "Second risk description",
            "CRITICAL_POINT_2": "Second critical point",
            "MITIGATION_ACTION_2": "Second risk mitigation action",
            "RISK_STAGE_3": "Third project stage/phase",
            "RISK_DESCRIPTION_3": "Third risk description",
            "CRITICAL_POINT_3": "Third critical point",
            "MITIGATION_ACTION_3": "Third risk mitigation action",
            "RISK_STAGE_4": "Fourth project stage/phase",
            "RISK_DESCRIPTION_4": "Fourth risk description",
            "CRITICAL_POINT_4": "Fourth critical point",
            "MITIGATION_ACTION_4": "Fourth risk mitigation action"
        }
        return descriptions
    
    def generate_smart_defaults(self, extracted_data, business_idea):
        """Generate smart defaults for missing fields based on business idea"""
        defaults = {}
        
        # Add current date
        defaults["COMPLETION_DATE"] = datetime.now().strftime("%d.%m.%Y")
        
        # Analyze business idea for smart defaults
        idea_lower = business_idea.lower()
        
        # Smart defaults based on content analysis
        if "health" in idea_lower or "medical" in idea_lower or "biotechnology" in idea_lower:
            defaults["RD_PRIORITY"] = "Health technologies"
            defaults["PROJECT_TYPE"] = "Health technologies and biotechnologies"
            defaults["RESEARCH_AREA"] = "Medical Sciences"
            defaults["EACC_CLASS"] = "72.11"
            defaults["PROJECT_KEYWORDS"] = "biotechnology, health technologies, medical devices, diagnostics"
        elif "ai" in idea_lower or "artificial intelligence" in idea_lower or "machine learning" in idea_lower:
            defaults["RD_PRIORITY"] = "Information and communication technologies"
            defaults["PROJECT_TYPE"] = "Information and communication technologies"
            defaults["PROJECT_SUBTOPIC"] = "Artificial intelligence, big and distributed data"
            defaults["RESEARCH_AREA"] = "Computer Sciences"
            defaults["EACC_CLASS"] = "62.01"
            defaults["PROJECT_KEYWORDS"] = "artificial intelligence, machine learning, data analytics, IoT"
        elif "energy" in idea_lower or "renewable" in idea_lower or "manufacturing" in idea_lower:
            defaults["RD_PRIORITY"] = "Production processes"
            defaults["PROJECT_TYPE"] = "New production processes, materials and technologies"
            defaults["PROJECT_SUBTOPIC"] = "Energy efficiency, smartness"
            defaults["RESEARCH_AREA"] = "Engineering Sciences"
            defaults["EACC_CLASS"] = "35.11"
            defaults["PROJECT_KEYWORDS"] = "renewable energy, energy efficiency, smart systems"
        else:
            # Default to ICT if no clear category
            defaults["RD_PRIORITY"] = "Information and communication technologies"
            defaults["PROJECT_TYPE"] = "Information and communication technologies"
            defaults["RESEARCH_AREA"] = "Computer Sciences"
            defaults["EACC_CLASS"] = "62.01"
            defaults["PROJECT_KEYWORDS"] = "innovation, technology, digital solutions"
        
        # Generate realistic company defaults
        company_names = [
            "Baltic Innovation Technologies UAB",
            "TechnoSolutions Baltic OÜ", 
            "Northern R&D Solutions AS",
            "Digital Innovation Hub UAB",
            "Advanced Technology Systems AS"
        ]
        
        manager_names = [
            "Dr. Vytautas Kazlauskas",
            "Dr. Andrius Petraitis",
            "Dr. Rasa Jankauskaite",
            "Dr. Mindaugas Balčiūnas",
            "Dr. Živilė Adamonienė"
        ]
        
        defaults["COMPANY_NAME"] = random.choice(company_names)
        defaults["COMPANY_CODE"] = f"LT{random.randint(300000000, 399999999)}"
        defaults["MANAGER_POSITION"] = "CEO"
        defaults["MANAGER_NAME"] = random.choice(manager_names)
        defaults["MANAGER_TITLE"] = "CEO"
        defaults["RES_MANA"] = "Leading R&D activities, technical supervision, project management"
        defaults["QUALI"] = "PhD in relevant field, 10+ years experience in R&D"
        
        # Shareholding defaults
        defaults["A_S_Ns"] = "Baltic Investment Group UAB"
        defaults["SHARE_HS"] = str(random.randint(60, 100))
        defaults["Name_of_the_legal_entity"] = "Baltic Investment Group UAB"
        defaults["Identification_code"] = f"LT{random.randint(100000000, 199999999)}"
        defaults["Shareholding"] = str(random.randint(60, 95))
        defaults["S_H"] = "European Tech Holdings AS"
        defaults["S_I"] = f"EE{random.randint(10000000, 19999999)}"
        defaults["S_S"] = str(random.randint(25, 75))
        
        # Project defaults
        defaults["N_As"] = "R&D Laboratory and Computing Infrastructure"
        defaults["F_Os"] = "Owned"
        defaults["S_Us"] = f"{random.randint(150, 300)} m²"
        defaults["W_R_Ds"] = "All R&D activities, testing, prototype development"
        
        # Financial defaults
        defaults["RD_BUDGET"] = str(random.randint(150000, 300000))
        defaults["RD_EXPENDITURE_2022"] = str(random.randint(100000, 200000))
        defaults["RD_EXPENDITURE_2023"] = str(random.randint(150000, 250000))
        defaults["REVENUE_PROJECTION"] = str(random.randint(400000, 800000))
        defaults["REVENUE_RATIO"] = str(round(random.uniform(2.0, 4.0), 1))
    
        
        # Technical defaults
        defaults["CURRENT_TPL"] = "TPL 3"
        defaults["TARGET_TPL"] = "TPL 6"
        defaults["NOVELTY_LEVEL"] = "market level"
        defaults["TOTAL_RESEARCH_JOBS"] = str(random.randint(3, 8))
        defaults["JOBS_DURING_PROJECT"] = str(random.randint(2, 5))
        defaults["JOBS_AFTER_PROJECT"] = str(random.randint(1, 3))
        
        # Project timing defaults
        defaults["PROJECT_START_MONTH"] = "1"
        defaults["PROJECT_COMPLETION_MONTH"] = "12"
        defaults["START_TPL_IMPACT"] = "TPL 3"
        defaults["END_TPL_IMPACT"] = "TPL 6"
        
        # Justification defaults
        defaults["JUS_PRO"] = "This product introduces innovative technological solutions that address current market gaps and provide significant competitive advantages"
        defaults["JUS_R_D_I"] = "The project aligns with national smart specialization priorities and addresses critical market needs through advanced R&D activities"
        defaults["TPL_JUSTIFICATION"] = "Progressive development from laboratory validation to market-ready prototype"
        defaults["PROJECT_IMPACT_TITLE"] = "Advanced Technology Solution Development"
        defaults["PROJECT_IMPACT_DESCRIPTION"] = "Development of innovative technology solution that will significantly impact the market and create new business opportunities"
        
        # Competition defaults
        defaults["COMPETITOR_1"] = "TechCorp International"
        defaults["COMPETITOR_MARKET_SHARE"] = str(random.randint(15, 35))
        
        # Activity defaults
        defaults["MAIN_ACTIVITY"] = "Research and development in technology solutions"
        defaults["ACTIVITY_PERCENTAGE"] = str(random.randint(70, 95))
        
        # Risk Assessment smart defaults
        defaults["RISK_STAGE_1"] = "Concept formulation and feasibility validation"
        defaults["RISK_DESCRIPTION_1"] = "Market acceptance uncertainty and technical feasibility risks"
        defaults["CRITICAL_POINT_1"] = "User needs validation and technical proof of concept"
        defaults["MITIGATION_ACTION_1"] = "Extensive market research and iterative prototype development"
        
        defaults["RISK_STAGE_2"] = "Layout development, testing, and optimization"
        defaults["RISK_DESCRIPTION_2"] = "Technical complexity and integration challenges"
        defaults["CRITICAL_POINT_2"] = "Algorithm optimization and system integration"
        defaults["MITIGATION_ACTION_2"] = "Agile development methodology and continuous testing"
        
        defaults["RISK_STAGE_3"] = "Prototype development and demonstration"
        defaults["RISK_DESCRIPTION_3"] = "Performance optimization and scalability issues"
        defaults["CRITICAL_POINT_3"] = "System performance under real-world conditions"
        defaults["MITIGATION_ACTION_3"] = "Comprehensive testing protocols and performance monitoring"
        
        defaults["RISK_STAGE_4"] = "Production and evaluation of pilot batch"
        defaults["RISK_DESCRIPTION_4"] = "Scale-up difficulties and quality assurance"
        defaults["CRITICAL_POINT_4"] = "Maintaining quality and performance at scale"
        defaults["MITIGATION_ACTION_4"] = "Pilot testing program and quality management systems"
        
        return defaults
    
    def auto_generate_missing_fields(self, business_idea, missing_fields):
        """Auto-generate missing fields using AI"""
        generated_data = {}
        
        # Get smart defaults as base
        smart_defaults = self.generate_smart_defaults({}, business_idea)
        
        # For each missing field, generate contextual value
        for category, fields in missing_fields.items():
            for field in fields:
                if field in smart_defaults:
                    # Use smart default as base and enhance with AI if needed
                    generated_data[field] = smart_defaults[field]
                else:
                    # Generate using AI for specific context
                    generated_value = self.ai_generate_field_value(field, business_idea)
                    generated_data[field] = generated_value
        
        return generated_data
    
    def ai_generate_field_value(self, field, business_idea):
        """Generate a specific field value using AI"""
        field_descriptions = self.get_field_descriptions()
        description = field_descriptions.get(field, field)
        
        prompt = f"""
        Based on this business idea: {business_idea}
        
        Generate a realistic value for the field: {field}
        Field description: {description}
        
        Generate only the value, no explanation. Make it realistic and appropriate for a Lithuanian R&D project.
        """
        
        try:
            response = self.ai_helper.generate_response(prompt, max_tokens=100)
            return response.strip()
        except Exception as e:
            print(f"Error generating field {field}: {e}")
            return f"Generated value for {field}"
    
    def process_business_idea(self, processed_business_idea):
        """Main processing function"""
        print(f"Processing business idea for comprehensive data extraction...")
        
        # Extract data using AI
        extracted_data = self.extract_comprehensive_data(processed_business_idea)
        
        # Identify missing fields
        missing_fields = self.identify_missing_fields(extracted_data)
        
        # Generate smart defaults
        smart_defaults = self.generate_smart_defaults(extracted_data, processed_business_idea)
        
        # Get field descriptions
        field_descriptions = self.get_field_descriptions()
        
        # Enhanced UI options
        user_options = {
            "auto_generate": "🤖 Auto-Generate All Missing Fields",
            "manual_input": "✋ Manual Input for All Fields", 
            "hybrid": "🔄 Hybrid Approach (Choose per field)"
        }
        
        return {
            "extracted_data": extracted_data,
            "missing_fields": missing_fields,
            "smart_defaults": smart_defaults,
            "field_descriptions": field_descriptions,
            "user_options": user_options,
            "auto_generation_available": True,
            "total_fields": sum(len(fields) for fields in self.required_fields.values()),
            "extracted_count": len([v for v in extracted_data.values() if v is not None]),
            "missing_count": sum(len(fields) for fields in missing_fields.values())
        }




















# from utils.ai_helper import AIHelper
# import json
# import re
# from datetime import datetime
# import random

# class ComprehensiveDataAgent:
#     def __init__(self):
#         self.ai_helper = AIHelper()
        
#         # Define all required fields with categories (UPDATED)
#         self.required_fields = {
#         "company_info": [
#             "COMPANY_NAME", "COMPANY_CODE", "MANAGER_POSITION", "MANAGER_NAME", 
#             "COMPLETION_DATE", "MAIN_ACTIVITY", "ACTIVITY_PERCENTAGE", "CESE_CLASS",
#             "N_L_E", "I_C", "Sharehol", "A_S_Ns", "SHARE_HS",
#             "S_H", "S_I", "S_S", "MANAGER_TITLE","SUMMARY_1","INNOVATIVENESS","E_S_RES","E_S_R&D",
#             "E_S_R", "A_S_RES", "A_S_R&D", "A_S_R", "A_S_P", "N_E", "N_R", "N_T", "N_W_T", "N_P_T", 
#             "LITERATURE_REVIEW","IPR", "COMMERCIALIZATION", "COLLABORATION", "LITERATURE_SOURCES",
#             # ADD MISSING FIELDS:
#             "RD_JUSTIFICATION_1", "RD_JUSTIFICATION_2", "RD_JUSTIFICATION_3", "RD_JUSTIFICATION_4", "RD_JUSTIFICATION_5",
#             "MARKET_ANALYSIS", "PRODUCT_PRICING", "PRICING_JUSTIFICATION", "RD_ACTIVITIES_PLAN"
#         ],
#         "project_details": [
#             "PRODUCT_NAME", "JUS_PRO", "NOVELTY_LEVEL", "JUS_R_D_I", "RD_PRIORITY",
#             "RESEARCH_AREA", "PROJECT_KEYWORDS","PROJECT_TYPE", "PROJECT_SUBTOPIC",
#             "N_As", "F_Os", "S_Us", "W_R_Ds","PRODUCTS_OFFERED","PER_SALES"
#         ],
#         "financial_data": [
#             "RD_BUDGET",  "REVENUE_PROJECTION", "REVENUE_RATIO",
#             "RD_EXPENDITURE_2022", "RD_EXPENDITURE_2023"
#         ],
#         "technical_info": [
#             "CURRENT_TPL", "TARGET_TPL", "TPL_JUSTIFICATION", "PROJECT_IMPACT_TITLE",
#             "PROJECT_START_MONTH", "PROJECT_COMPLETION_MONTH", "PROJECT_IMPACT_DESCRIPTION"
#         ],
#         "competition_jobs": [
#             "COMPETITOR_M", "COMPETITOR_MARKET_SHARE", "TOTAL_RESEARCH_JOBS", 
#             "JOBS_DURING_PROJECT", "JOBS_AFTER_PROJECT"
#         ],
#         "risk_assessment": [
#             "RISK_STAGE_1", "RISK_DESCRIPTION_1", "CRITICAL_POINT_1", "MITIGATION_ACTION_1",
#             "RISK_STAGE_2", "RISK_DESCRIPTION_2", "CRITICAL_POINT_2", "MITIGATION_ACTION_2",
#             "RISK_STAGE_3", "RISK_DESCRIPTION_3", "CRITICAL_POINT_3", "MITIGATION_ACTION_3",
#             "RISK_STAGE_4", "RISK_DESCRIPTION_4", "CRITICAL_POINT_4", "MITIGATION_ACTION_4"
#         ]
#     }
    
#     def extract_comprehensive_data(self, processed_business_idea):
#         prompt = f"""
#         Extract structured information from the business idea below and format responses exactly to match the document structure of the MTEP Business Plan.

#         Business Idea: {processed_business_idea}

#         CRITICAL INSTRUCTIONS:
#         - You MUST extract ALL fields listed below
#         - Use EXACTLY this format: FIELD_NAME: extracted_value
#         - If information is not available, write "NOT_FOUND"
#         - Do NOT skip any field
#         - Do NOT add explanations or additional text

#         **SPECIAL ATTENTION TO EMPLOYMENT/JOBS DATA:**
#         Look carefully for employment data which might be mentioned as:
#         - "Employment Impact"
#         - "Current Research Jobs"
#         - "Jobs During Project" 
#         - "Jobs After Project"
#         - "Total Research Jobs"
#         - Numbers followed by "jobs", "employees", "researchers", "staff"
        
#         Follow the logical sequence where Section 4.4 literature review forms the foundation for re-examining the idea according to the Frascati Manual, which then informs Section 4.3 justification of R&D activities, which subsequently guides Section 3.1 product descriptions and innovation analysis.

#         ------------------------
#         SECTION 4.4 An overview of national and international research on product development (FOUNDATION ANALYSIS - Complete this first as it forms the basis for formulating scientific problems, hypotheses and applications):
#         ------------------------
#         LITERATURE_REVIEW: [Extract and synthesize an overview of national and international research on product development up to 200 words. This analysis will be used to re-examine the idea according to the Frascati Manual and inform all subsequent sections.]

#         ------------------------
#         SECTION 4.3 Justification of the R&D activities required for product development/improvement (Based on 4.4 studies, develop the scientific problem, hypothesis, uncertainties, and systematic approach):
#         ------------------------
#         RD_JUSTIFICATION_1: [Extract justification of new or additional knowledge sought - what scientific/technological problems exist for which knowledge is not publicly available]
#         RD_JUSTIFICATION_2: [Extract original ideas and hypotheses on which the project is based - what original, non-obvious hypothesis will be tested]
#         RD_JUSTIFICATION_3: [Extract description of project uncertainties - likelihood of failing to generate sufficient knowledge, achieve planned results, or meet timeline]
#         RD_JUSTIFICATION_4: [Extract systematic nature of planned activities - how activities are coherent, logical, and comply with SMART principles]
#         RD_JUSTIFICATION_5: [Extract how results will be replicable and transferable - what documentation will enable knowledge transfer]

#         ------------------------
#         SECTION 3 PRODUCTS FOR WHICH FUNDING IS REQUESTED (Using knowledge from 4.3 about problems solved and technical solutions):
#         ------------------------
#             ------------------------
#             3.1 Description of the new or substantially improved product to be developed:
#             ------------------------
#                 ------------------------
#                 SECTION 3.1.1: Describe the product's unique features, technical solutions, and how it differs from similar products on the market. Use knowledge from 4.3 about what problems it solves and what technical solutions are needed:
#                 ------------------------
#                 INNOVATIVENESS: [Extract the innovative aspects of the product or service, how it differs from existing solutions, and its potential impact on the market. Base this on problems identified in 4.3.]

#                 ------------------------
#                 SECTION 3.1.2: The level of novelty of the product(s) created by the project (Determined by analysis from 4.4 and 3.1.1 on the Oslo Manual scale - justify that the idea is novel at the global level):
#                 ------------------------
#                 PRODUCT_NAME: [Extract product name or use "NOT_FOUND"]
#                 NOVELTY_LEVEL: [Determine: "company level", "market level", "global level" or "NOT_FOUND" - must justify global level novelty based on literature analysis]
#                 JUS_PRO: [Extract justification for product novelty using Oslo Manual criteria and literature analysis]

#                 ------------------------
#                 SECTION 3.1.3: Justify how the project supports the RDI (Smart Specialisation) Concept (Assignment to previously analysed area from 4.4, 4.3, 3.1 - use MTEPI priorities approved by Lithuanian Government Resolution No. 835 of 17 August 2022):
#                 ------------------------
#                 RD_PRIORITY: [Choose from Lithuanian priorities: "Health technologies", "Production processes", "Information and communication technologies" or "NOT_FOUND"]
#                 JUS_R_D_I: [Extract how the project matches any R&D&I priority and its theme, based on previous analysis]

#                 ------------------------
#                 SECTION 3.1.4: Research area(s) of the project (Classification from 3.1.1 analysis - choose according to Lithuanian Ministry Order No V-93 of 6 February 2019):
#                 ------------------------
#                 RESEARCH_AREA: [Extract research fields based on product classification or use "NOT_FOUND"]
                
#                 ------------------------
#                 SECTION 3.1.5: Project keywords (Derived from 3.1.1, 4.4 literature review and 4.3 R&D justification using NLP processing):
#                 ------------------------
#                 PROJECT_KEYWORDS: [Extract ALL relevant keywords from the text, especially technical terms from literature and R&D analysis, separated by commas]

#         ------------------------
#         SECTION 4.5 A plan of the R&D activities (Formulate based on 4.3 uncertainties and hypothesis testing, 4.4 literature, and 4.2 people - describe specific tasks and required hours):
#         ------------------------
#         PROJECT_IMPACT_TITLE: [Extract project impact title or use "NOT_FOUND"]
#         PROJECT_START_MONTH: [Extract project start month or use "NOT_FOUND"]
#         PROJECT_COMPLETION_MONTH: [Extract project completion month or use "NOT_FOUND"]
#         CURRENT_TPL: [Extract current Technology Readiness Level or use "NOT_FOUND"]
#         TARGET_TPL: [Extract target Technology Readiness Level or use "NOT_FOUND"]
#         RD_ACTIVITIES_PLAN: [Extract detailed R&D activities plan describing what tasks need to be performed and estimated hours required]

#         ------------------------
#         SECTION 4.2 Project implementation team (Based on 4.5 activities, determine what positions are needed, when, and how many working hours - fill iteratively with 4.5):
#         ------------------------
#             -------------------------
#             SECTION 4.2.1: Existing staff of the applicant and the partner who will be responsible for carrying out the R&D activities:
#             -------------------------
#             E_S_RES: [Extract Responsibilities based on 4.5 activities]
#             E_S_R&D: [Extract Responsibilities for R&D activities from 4.5 plan]
#             E_S_R: [Extract Minimum qualification requirements for staff]

#             -------------------------
#             SECTION 4.2.2: Additional staff of the applicant and the partner are needed to carry out the R&D activities:
#             -------------------------
#             A_S_RES: [Extract Responsibilities for new staff based on 4.5]
#             A_S_R&D: [Extract Responsibilities for R&D activities for new hires]
#             A_S_R: [Extract Minimum qualification requirements for additional staff]
#             A_S_P: [Extract Period (year and month) of planned recruitment]

#             -------------------------
#             SECTION 4.2.3: The tasks to be carried out by each R&D personnel (Take hours from 4.5 and allocate to specific personnel):
#             -------------------------
#             N_E: [Extract Name of employee Surname (if known)]
#             N_R: [Extract Responsibilities from 4.5 activities]
#             N_T: [Extract Task(s) to be carried out from 4.5 plan]
#             N_W_T: [Extract Number of working hours per task from 4.5 estimates]
#             N_P_T: [Extract Result of planned tasks from 4.5 outputs]

#         ------------------------
#         SECTION 4.6 Intellectual property issues (Evaluate after analysis of innovativeness 3.1.1 and literature 4.4):
#         ------------------------
#         IPR: [Extract Intellectual property issues for the products to be produced, including patenting details based on innovation and literature analysis]

#         ------------------------
#         SECTION 4.7 Product market development plan (Market readiness activities after R&D completion but before production start):
#         ------------------------
#         COMMERCIALIZATION: [Extract commercialization strategy focusing on testing, standardisation, production capacity design, user instructions - NOT product design or equipment acquisition]

#         ------------------------
#         SECTION 4.8 Risk assessment of the R&D project (Based on sequence of activities in 4.5 and uncertainties in 4.3):
#         ------------------------
#         RISK_STAGE_1: [Extract first risk stage/phase based on 4.5 sequence]
#         RISK_DESCRIPTION_1: [Extract first risk description based on 4.3 uncertainties]
#         CRITICAL_POINT_1: [Extract first critical point from 4.5 activities]
#         MITIGATION_ACTION_1: [Extract first mitigation action]
#         RISK_STAGE_2: [Extract second risk stage/phase based on 4.5 sequence]
#         RISK_DESCRIPTION_2: [Extract second risk description based on 4.3 uncertainties]
#         CRITICAL_POINT_2: [Extract second critical point from 4.5 activities]
#         MITIGATION_ACTION_2: [Extract second mitigation action]
#         RISK_STAGE_3: [Extract third risk stage/phase based on 4.5 sequence]
#         RISK_DESCRIPTION_3: [Extract third risk description based on 4.3 uncertainties]
#         CRITICAL_POINT_3: [Extract third critical point from 4.5 activities]
#         MITIGATION_ACTION_3: [Extract third mitigation action]
#         RISK_STAGE_4: [Extract fourth risk stage/phase based on 4.5 sequence]
#         RISK_DESCRIPTION_4: [Extract fourth risk description based on 4.3 uncertainties]
#         CRITICAL_POINT_4: [Extract fourth critical point from 4.5 activities]
#         MITIGATION_ACTION_4: [Extract fourth mitigation action]

#         ------------------------
#         SECTION 4.9 The feasibility and benefits of the partnership (Define boundaries between applicant and partner work - basis for 4.2 staff listing):
#         ------------------------
#         COLLABORATION: [Extract the feasibility and benefits of the partnership, defining what applicant vs partner will do]

#         ------------------------
#         SECTION 5 DESCRIPTION OF HOW THE PRODUCT IS PLACED ON THE MARKET (Market study needed, possibly parallel with 4.4):
#         ------------------------
#             ------------------------
#             SECTION 5.1 Market analysis (Conduct market study parallel with literature review):
#             ------------------------
#             MARKET_ANALYSIS: [Extract market demand forecast, target consumers, market characteristics including size, growth, seasonal changes, product cycles]
            
#             ------------------------
#             SECTION 5.2 Main competitors (From same sources as 5.1, plus 3.1.1 innovation analysis):
#             ------------------------
#             COMPETITOR_M: [Extract main competitor name based on market and innovation analysis]
#             COMPETITOR_MARKET_SHARE: [Extract market share percentage from market study]
            
#             ------------------------
#             SECTION 5.3 Pricing strategy (Suggest pricing based on competitor info 5.2 and product specifics 3.1.1):
#             ------------------------
#             PRODUCT_PRICING: [Extract suggested pricing strategy based on competitors and product innovation]
#             PRICING_JUSTIFICATION: [Extract pricing assumptions and main determining factors]
            
#             ------------------------
#             SECTION 5.4 Commercialisation potential (Summarise 4.5 TPL progression and evaluate activities):
#             ------------------------
#             PRODUCT_NAME: [Extract product name]
#             CURRENT_TPL: [Extract current Technology Readiness Level from 4.5]
#             TARGET_TPL: [Extract target Technology Readiness Level from 4.5]
#             TPL_JUSTIFICATION: [Extract justification based on 4.5 activities evaluation]

#         ------------------------
#         SECTION 2: DESCRIPTION OF THE LEGAL ENTITY AND ITS ACTIVITIES (Actual data for SME verification - can be filled earlier):
#         ------------------------
#             ------------------------
#             2.1 Information on shareholders: name, company code/name, number of shares held :
#             ------------------------
#                 ------------------------
#                 SECTION 2.1.1: Information on the applicant's shareholders and shareholders' shareholders (up to natural persons):
#                 ------------------------
#                 A_S_Ns: [Extract Shareholder name]
#                 COMPANY_CODE: [Extract Company code*]
#                 SHARE_HS: [Extract Shareholding, %]

#                 ------------------------
#                 SECTION 2.1.2: Information on the legal entities in which the applicant holds shares:
#                 ------------------------
#                 N_L_E: [Extract Name of the legal entity]
#                 I_C: [Extract Identification code]
#                 Sharehol: [Extract Shareholding, %]

#                 ------------------------
#                 SECTION 2.1.3: Information on the legal entities in which the applicant's shareholders hold shares:
#                 ------------------------
#                 S_H: [Extract Name of the legal entity]
#                 S_I: [Extract Identification code]
#                 S_S: [Extract Shareholding, %]

#             ------------------------
#             SECTION 2.2: The applicant must list their current business activities using ECC classification:
#             ------------------------
#             MAIN_ACTIVITY: [Extract Main business activity from ECC classification]
#             ACTIVITY_PERCENTAGE: [Extract Share of activity (%) in total company activity]
#             CESE_CLASS: [Extract Class of the CESE]
                
#             ------------------------
#             SECTION 2.3: The products offered by the applicant:
#             ------------------------
#             PRODUCTS_OFFERED: [Extract Products offered by the applicant]
#             PER_SALES: [Extract Percentage of sales]

#         ------------------------
#         SECTION 6 RESOURCES NEEDED FOR PRODUCT DEVELOPMENT/IMPROVEMENT (Describe equipment, premises, materials needs from 4.5 and available enterprise resources):
#         ------------------------
#             ------------------------
#             SECTION 6.1 A description of the main assets and resources (Most cases will be empty due to administrative burden and depreciation issues):
#             ------------------------
#             N_As: [Extract the name of the asset used in R&D activities from 4.5 needs]
#             F_Os: [Extract the form of ownership for the asset]
#             S_Us: [Extract the share or amount of the asset used for R&D]
#             W_R_Ds: [Extract which R&D activities the asset will be used for from 4.5]

#         ------------------------
#         SECTION 7 FINANCIAL PLAN (Evaluate whether revenue achievement is treated as commitment and if priority points given for higher revenue/project ratio):
#         ------------------------
#             ------------------------
#             SECTION 7.1 The ratio of enterprise's projected income (Take most optimistic option if priority points given):
#             ------------------------
#             REVENUE_PROJECTION: [Extract Planned revenue (P), EUR - use optimistic projection if priority points apply]
#             RD_BUDGET: [Extract Eligible project costs (I), EUR]
#             REVENUE_RATIO: [Extract Revenue to expenditure ratio (X)* - confirm if commitment required]

#         ------------------------
#         SECTION 1: SUMMARY (Complete last when all information has been gathered):
#         ------------------------
#         SUMMARY_1: [Extract and write a 1000 words summary about your company, your innovative product, its market potential, costs, and future plan. Complete this after all other sections are filled.]

#         -----------------------
#         SECTION 8 SOURCES OF LITERATURE (Generated automatically from 4.4 content):
#         ------------------------
#         LITERATURE_SOURCES: [Extract Literature sources - generate automatically from Section 4.4 literature review content]

#         ████████████████████████████████████████████████████████████████████████████████
#         ██  CRITICAL EMPLOYMENT/JOBS DATA EXTRACTION - PAY SPECIAL ATTENTION HERE:   ██
#         ████████████████████████████████████████████████████████████████████████████████
        
#         THESE THREE FIELDS ARE MANDATORY AND OFTEN MISSING - LOOK VERY CAREFULLY:
        
#         TOTAL_RESEARCH_JOBS: [EXTRACT the total number of research jobs/positions. Look for phrases like "Total Research Jobs:", "Current Research Jobs:", "research positions", "research staff", "R&D personnel", "research team size". Extract the NUMBER only, e.g., "8" or "11"]
        
#         JOBS_DURING_PROJECT: [EXTRACT number of jobs/positions during the project execution. Look for "Jobs During Project:", "positions during", "staff during project", "project team size", "personnel during implementation". Extract the NUMBER only, e.g., "5" or "8"]
        
#         JOBS_AFTER_PROJECT: [EXTRACT number of jobs/positions after project completion. Look for "Jobs After Project:", "positions after", "permanent positions", "long-term employment", "post-project staff". Extract the NUMBER only, e.g., "12" or "15"]

#         Now also extract these additional fields for other documents:
#         MANAGER_POSITION: [Extract manager position]
#         MANAGER_NAME: [Extract manager name]
#         COMPLETION_DATE: [Today's date in DD.MM.YYYY format]
#         MANAGER_TITLE: [Extract manager title]
#         PROJECT_TYPE: [Choose: "Health technologies and biotechnologies", "New production processes, materials and technologies", "Information and communication technologies" or "NOT_FOUND"]
#         PROJECT_SUBTOPIC: [Extract specific subtopic or use "NOT_FOUND"]
#         RD_EXPENDITURE_2022: [Extract R&D expenditure for 2022 or use "NOT_FOUND"]
#         RD_EXPENDITURE_2023: [Extract R&D expenditure for 2023 or use "NOT_FOUND"]
#         TPL_JUSTIFICATION: [Extract TPL justification or use "NOT_FOUND"]
#         PROJECT_IMPACT_DESCRIPTION: [Extract detailed project impact description or use "NOT_FOUND"]

#         """

#         try:
#             print("DEBUG: Sending request to AI...")
#             response = self.ai_helper.generate_response(prompt)
            
#             extracted_data = self.parse_extracted_data(response)
            
#             print(f"FINAL RESULT: Extracted {len(extracted_data)} fields")
#             return extracted_data
#         except Exception as e:
#             print(f"Error extracting comprehensive data: {e}")
#             return self.get_empty_data_structure()
        
#     def parse_extracted_data(self, response):
#         """IMPROVED PARSING METHOD WITH SPECIAL FOCUS ON JOBS DATA"""
#         extracted_data = {}
        
#         # Get all valid field names
#         all_fields = []
#         for category, fields in self.required_fields.items():
#             all_fields.extend(fields)
        
#         print(f"DEBUG: Looking for {len(all_fields)} fields...")
        
#         # Special handling for job fields - look for these patterns first
#         job_patterns = {
#             'TOTAL_RESEARCH_JOBS': [
#                 r'total\s+research\s+jobs[:\s]*(\d+)',
#                 r'current\s+research\s+jobs[:\s]*(\d+)',
#                 r'TOTAL_RESEARCH_JOBS[:\s]*(\d+)',
#                 r'research\s+jobs[:\s]*(\d+)',
#                 r'total.*jobs[:\s]*(\d+)'
#             ],
#             'JOBS_DURING_PROJECT': [
#                 r'jobs\s+during\s+project[:\s]*(\d+)',
#                 r'JOBS_DURING_PROJECT[:\s]*(\d+)',
#                 r'during\s+project[:\s]*(\d+)',
#                 r'project\s+team[:\s]*(\d+)'
#             ],
#             'JOBS_AFTER_PROJECT': [
#                 r'jobs\s+after\s+project[:\s]*(\d+)',
#                 r'JOBS_AFTER_PROJECT[:\s]*(\d+)',
#                 r'after\s+project[:\s]*(\d+)',
#                 r'post[_\-\s]project[:\s]*(\d+)'
#             ]
#         }
        
#         # First, try to extract job fields using regex patterns
#         response_lower = response.lower()
#         for field_name, patterns in job_patterns.items():
#             for pattern in patterns:
#                 match = re.search(pattern, response_lower, re.IGNORECASE)
#                 if match:
#                     job_count = match.group(1)
#                     extracted_data[field_name] = job_count
#                     print(f"✓ FOUND {field_name} via regex: {job_count}")
#                     break
        
#         # Split response into lines for standard parsing
#         lines = response.split('\n')
        
#         for line_num, line in enumerate(lines):
#             line = line.strip()
#             if not line or ':' not in line:
#                 continue
                
#             # Find the first colon position
#             colon_pos = line.find(':')
#             if colon_pos == -1:
#                 continue
                
#             # Extract potential field name (everything before first colon)
#             potential_field = line[:colon_pos].strip()
#             value_part = line[colon_pos + 1:].strip()
            
#             # Check if this is actually a field we're looking for
#             if potential_field in all_fields:
#                 # Clean the value
#                 if value_part.startswith('[') and value_part.endswith(']'):
#                     value_part = value_part[1:-1].strip()
                
#                 # Remove instruction prefixes
#                 prefixes_to_remove = [
#                     "Extract ", "Choose ", "Determine ", "Generate ",
#                     "Extract and ", "Choose from ", "Determine: ",
#                     "Extract the ", "Choose the ", "Select ", "EXTRACT "
#                 ]
                
#                 for prefix in prefixes_to_remove:
#                     if value_part.startswith(prefix):
#                         value_part = value_part[len(prefix):].strip()
#                         break
                
#                 # Clean up quotes and special characters
#                 value_part = value_part.strip('"\'`')
                
#                 # Special handling for job fields - extract numbers
#                 if potential_field in ['TOTAL_RESEARCH_JOBS', 'JOBS_DURING_PROJECT', 'JOBS_AFTER_PROJECT']:
#                     # Extract just the number
#                     number_match = re.search(r'(\d+)', value_part)
#                     if number_match:
#                         value_part = number_match.group(1)
#                         print(f"✓ EXTRACTED JOB NUMBER {potential_field}: {value_part}")
                
#                 # Only add if not "NOT_FOUND" and not empty
#                 if value_part and value_part != "NOT_FOUND" and len(value_part) > 0:
#                     # Don't overwrite job fields if already found via regex
#                     if potential_field not in extracted_data:
#                         extracted_data[potential_field] = value_part
#                         print(f"✓ FOUND {potential_field}: {value_part[:60]}...")
#                 else:
#                     print(f"✗ EMPTY/INVALID value for {potential_field}: '{value_part}'")
#             else:
#                 # Check if it's a field with slight variations
#                 for field_name in all_fields:
#                     if potential_field.lower() == field_name.lower():
#                         if value_part and value_part != "NOT_FOUND" and len(value_part) > 0:
#                             if field_name not in extracted_data:  # Don't overwrite
#                                 extracted_data[field_name] = value_part
#                                 print(f"✓ FOUND (case variation) {field_name}: {value_part[:60]}...")
#                         break
        
#         print(f"DEBUG: Successfully extracted {len(extracted_data)} out of {len(all_fields)} fields")
        
#         # Show what job fields were found
#         job_fields = ['TOTAL_RESEARCH_JOBS', 'JOBS_DURING_PROJECT', 'JOBS_AFTER_PROJECT']
#         for job_field in job_fields:
#             if job_field in extracted_data:
#                 print(f"✅ JOB FIELD FOUND: {job_field} = {extracted_data[job_field]}")
#             else:
#                 print(f"❌ JOB FIELD MISSING: {job_field}")
        
#         return extracted_data

#     def get_empty_data_structure(self):
#         """Return empty data structure with all fields set to None"""
#         empty_data = {}
#         for category, fields in self.required_fields.items():
#             for field in fields:
#                 empty_data[field] = None
#         return empty_data
    
#     def identify_missing_fields(self, extracted_data):
#         """Identify which fields are missing and categorize them"""
#         missing_fields = {}
        
#         for category, fields in self.required_fields.items():
#             missing_in_category = []
#             for field in fields:
#                 if field not in extracted_data or extracted_data[field] is None:
#                     missing_in_category.append(field)
            
#             if missing_in_category:
#                 missing_fields[category] = missing_in_category
        
#         return missing_fields
    
#     def get_field_descriptions(self):
#         """Get user-friendly descriptions for fields"""
#         descriptions = {
#             "COMPANY_NAME": "Company name (e.g., 'TechnoSolutions Baltic OÜ')",
#             "COMPANY_CODE": "Company registration code (e.g., 'LT123456789')",
#             "MANAGER_POSITION": "Manager position (e.g., 'CEO', 'CTO')",
#             "MANAGER_NAME": "Manager name (e.g., 'Andrius Kazlauskas')",
#             "COMPLETION_DATE": "Completion date (DD.MM.YYYY format)",
#             "MAIN_ACTIVITY": "Main business activity description",
#             "ACTIVITY_PERCENTAGE": "Activity percentage (e.g., '75')",
#             "CESE_CLASS": "CESE classification code (e.g., '62.01')",
#             "Name_of_the_legal_entity": "Legal entity name",
#             "Identification_code": "Identification code",
#             "Shareholding": "Shareholding percentage",
#             "A_S_Ns": "Applicant's shareholders names",
#             "SHARE_HS": "Shareholding percentage for each shareholder",
#             "S_H": "Legal entity name in which applicant's shareholders hold shares",
#             "S_I": "Identification code of that legal entity",
#             "S_S": "Shareholding percentage held by shareholder in that entity",
#             "MANAGER_TITLE": "Manager title",
#             "SUMMARY_1": "200-250 word summary about the company, product, market potential, costs, and future plans",
#             "PRODUCT_NAME": "Product or service name",
#             "PRODUCT_DESCRIPTION": "Detailed product description",
#             "JUS_PRO": "Product novelty justification",
#             "NOVELTY_LEVEL": "Novelty level (company/market/global)",
#             "RD_PRIORITY": "R&D priority category",
#             "JUS_R_D_I": "R&D&I priority justification",
#             "RESEARCH_AREA": "Research area (e.g., 'Computer Sciences')",
#             "PROJECT_KEYWORDS": "Project keywords separated by commas",
#             "N_As": "Asset name (equipment, software, etc.)",
#             "F_Os": "Form of ownership (owned, leased, shared)",
#             "S_Us": "Share/amount of asset used for R&D",
#             "W_R_Ds": "R&D activities the asset will be used for",
#             "PROJECT_TYPE": "Project type category",
#             "PROJECT_SUBTOPIC": "Specific project subtopic",
            
#             "RD_BUDGET": "R&D budget in euros (e.g., '200000')",
#             "REVENUE_PROJECTION": "Revenue projection in euros",
#             "REVENUE_RATIO": "Revenue to cost ratio",
#             "RD_EXPENDITURE_2022": "R&D expenditure for 2022",
#             "RD_EXPENDITURE_2023": "R&D expenditure for 2023",
            
#             "CURRENT_TPL": "Current Technology Readiness Level",
#             "TARGET_TPL": "Target Technology Readiness Level",
#             "TPL_JUSTIFICATION": "TPL achievement justification",
#             "PROJECT_IMPACT_TITLE": "Project impact title",
#             "PROJECT_START_MONTH": "Project start month",
#             "PROJECT_COMPLETION_MONTH": "Project completion month",
#             "START_TPL_IMPACT": "Starting TPL for impacts",
#             "END_TPL_IMPACT": "Ending TPL for impacts",
#             "PROJECT_IMPACT_DESCRIPTION": "Detailed project impact description",
            
#             "COMPETITOR_M": "Main competitor name",
#             "COMPETITOR_MARKET_SHARE": "Competitor market share percentage",
#             "TOTAL_RESEARCH_JOBS": "Total research jobs to be created",
#             "JOBS_DURING_PROJECT": "Research jobs during project",
#             "JOBS_AFTER_PROJECT": "Research jobs after project",
            
#             # Risk Assessment fields
#             "RISK_STAGE_1": "First project stage/phase",
#             "RISK_DESCRIPTION_1": "First risk description",
#             "CRITICAL_POINT_1": "First critical point",
#             "MITIGATION_ACTION_1": "First risk mitigation action",
#             "RISK_STAGE_2": "Second project stage/phase",
#             "RISK_DESCRIPTION_2": "Second risk description",
#             "CRITICAL_POINT_2": "Second critical point",
#             "MITIGATION_ACTION_2": "Second risk mitigation action",
#             "RISK_STAGE_3": "Third project stage/phase",
#             "RISK_DESCRIPTION_3": "Third risk description",
#             "CRITICAL_POINT_3": "Third critical point",
#             "MITIGATION_ACTION_3": "Third risk mitigation action",
#             "RISK_STAGE_4": "Fourth project stage/phase",
#             "RISK_DESCRIPTION_4": "Fourth risk description",
#             "CRITICAL_POINT_4": "Fourth critical point",
#             "MITIGATION_ACTION_4": "Fourth risk mitigation action"
#         }
#         return descriptions
    
#     def generate_smart_defaults(self, extracted_data, business_idea):
#         """Generate smart defaults for missing fields based on business idea"""
#         defaults = {}
        
#         # Add current date
#         defaults["COMPLETION_DATE"] = datetime.now().strftime("%d.%m.%Y")
        
#         # Analyze business idea for smart defaults
#         idea_lower = business_idea.lower()
        
#         # Smart defaults based on content analysis
#         if "health" in idea_lower or "medical" in idea_lower or "biotechnology" in idea_lower:
#             defaults["RD_PRIORITY"] = "Health technologies"
#             defaults["PROJECT_TYPE"] = "Health technologies and biotechnologies"
#             defaults["RESEARCH_AREA"] = "Medical Sciences"
#             defaults["CESE_CLASS"] = "72.11"
#             defaults["PROJECT_KEYWORDS"] = "biotechnology, health technologies, medical devices, diagnostics"
#         elif "ai" in idea_lower or "artificial intelligence" in idea_lower or "machine learning" in idea_lower:
#             defaults["RD_PRIORITY"] = "Information and communication technologies"
#             defaults["PROJECT_TYPE"] = "Information and communication technologies"
#             defaults["PROJECT_SUBTOPIC"] = "Artificial intelligence, big and distributed data"
#             defaults["RESEARCH_AREA"] = "Computer Sciences"
#             defaults["CESE_CLASS"] = "62.01"
#             defaults["PROJECT_KEYWORDS"] = "artificial intelligence, machine learning, data analytics, IoT"
#         elif "energy" in idea_lower or "renewable" in idea_lower or "manufacturing" in idea_lower:
#             defaults["RD_PRIORITY"] = "Production processes"
#             defaults["PROJECT_TYPE"] = "New production processes, materials and technologies"
#             defaults["PROJECT_SUBTOPIC"] = "Energy efficiency, smartness"
#             defaults["RESEARCH_AREA"] = "Engineering Sciences"
#             defaults["CESE_CLASS"] = "35.11"
#             defaults["PROJECT_KEYWORDS"] = "renewable energy, energy efficiency, smart systems"
#         else:
#             # Default to ICT if no clear category
#             defaults["RD_PRIORITY"] = "Information and communication technologies"
#             defaults["PROJECT_TYPE"] = "Information and communication technologies"
#             defaults["RESEARCH_AREA"] = "Computer Sciences"
#             defaults["CESE_CLASS"] = "62.01"
#             defaults["PROJECT_KEYWORDS"] = "innovation, technology, digital solutions"
        
#         # Generate realistic company defaults
#         company_names = [
#             "Baltic Innovation Technologies UAB",
#             "TechnoSolutions Baltic OÜ", 
#             "Northern R&D Solutions AS",
#             "Digital Innovation Hub UAB",
#             "Advanced Technology Systems AS"
#         ]
        
#         manager_names = [
#             "Dr. Vytautas Kazlauskas",
#             "Dr. Andrius Petraitis",
#             "Dr. Rasa Jankauskaite",
#             "Dr. Mindaugas Balčiūnas",
#             "Dr. Živilė Adamonienė"
#         ]
        
#         defaults["COMPANY_NAME"] = random.choice(company_names)
#         defaults["COMPANY_CODE"] = f"LT{random.randint(300000000, 399999999)}"
#         defaults["MANAGER_POSITION"] = "CEO"
#         defaults["MANAGER_NAME"] = random.choice(manager_names)
#         defaults["MANAGER_TITLE"] = "CEO"
#         defaults["E_S_RES"] = "Leading R&D activities, technical supervision, project management"
#         defaults["E_S_R"] = "PhD in relevant field, 10+ years experience in R&D"
        
#         # Shareholding defaults
#         defaults["A_S_Ns"] = "Baltic Investment Group UAB"
#         defaults["SHARE_HS"] = str(random.randint(60, 100))
#         defaults["N_L_E"] = "Baltic Investment Group UAB"
#         defaults["I_C"] = f"LT{random.randint(100000000, 199999999)}"
#         defaults["Sharehol"] = str(random.randint(60, 95))
#         defaults["S_H"] = "European Tech Holdings AS"
#         defaults["S_I"] = f"EE{random.randint(10000000, 19999999)}"
#         defaults["S_S"] = str(random.randint(25, 75))
        
#         # Project defaults
#         defaults["N_As"] = "R&D Laboratory and Computing Infrastructure"
#         defaults["F_Os"] = "Owned"
#         defaults["S_Us"] = f"{random.randint(150, 300)} m²"
#         defaults["W_R_Ds"] = "All R&D activities, testing, prototype development"
        
#         # Financial defaults
#         defaults["RD_BUDGET"] = str(random.randint(150000, 300000))
#         defaults["RD_EXPENDITURE_2022"] = str(random.randint(100000, 200000))
#         defaults["RD_EXPENDITURE_2023"] = str(random.randint(150000, 250000))
#         defaults["REVENUE_PROJECTION"] = str(random.randint(400000, 800000))
#         defaults["REVENUE_RATIO"] = str(round(random.uniform(2.0, 4.0), 1))
    
#         # Technical defaults
#         defaults["CURRENT_TPL"] = "TPL 3"
#         defaults["TARGET_TPL"] = "TPL 6"
#         defaults["NOVELTY_LEVEL"] = "market level"
#         defaults["TOTAL_RESEARCH_JOBS"] = str(random.randint(3, 8))
#         defaults["JOBS_DURING_PROJECT"] = str(random.randint(2, 5))
#         defaults["JOBS_AFTER_PROJECT"] = str(random.randint(1, 3))
        
#         # Project timing defaults
#         defaults["PROJECT_START_MONTH"] = "1"
#         defaults["PROJECT_COMPLETION_MONTH"] = "12"
        
#         # Justification defaults
#         defaults["JUS_PRO"] = "This product introduces innovative technological solutions that address current market gaps and provide significant competitive advantages"
#         defaults["JUS_R_D_I"] = "The project aligns with national smart specialization priorities and addresses critical market needs through advanced R&D activities"
#         defaults["TPL_JUSTIFICATION"] = "Progressive development from laboratory validation to market-ready prototype"
#         defaults["PROJECT_IMPACT_TITLE"] = "Advanced Technology Solution Development"
#         defaults["PROJECT_IMPACT_DESCRIPTION"] = "Development of innovative technology solution that will significantly impact the market and create new business opportunities"
        
#         # Competition defaults
#         defaults["COMPETITOR_M"] = "TechCorp International"
#         defaults["COMPETITOR_MARKET_SHARE"] = str(random.randint(15, 35))
        
#         # Activity defaults
#         defaults["MAIN_ACTIVITY"] = "Research and development in technology solutions"
#         defaults["ACTIVITY_PERCENTAGE"] = str(random.randint(70, 95))
        
#         # Risk Assessment smart defaults
#         defaults["RISK_STAGE_1"] = "Concept formulation and feasibility validation"
#         defaults["RISK_DESCRIPTION_1"] = "Market acceptance uncertainty and technical feasibility risks"
#         defaults["CRITICAL_POINT_1"] = "User needs validation and technical proof of concept"
#         defaults["MITIGATION_ACTION_1"] = "Extensive market research and iterative prototype development"
        
#         defaults["RISK_STAGE_2"] = "Layout development, testing, and optimization"
#         defaults["RISK_DESCRIPTION_2"] = "Technical complexity and integration challenges"
#         defaults["CRITICAL_POINT_2"] = "Algorithm optimization and system integration"
#         defaults["MITIGATION_ACTION_2"] = "Agile development methodology and continuous testing"
        
#         defaults["RISK_STAGE_3"] = "Prototype development and demonstration"
#         defaults["RISK_DESCRIPTION_3"] = "Performance optimization and scalability issues"
#         defaults["CRITICAL_POINT_3"] = "System performance under real-world conditions"
#         defaults["MITIGATION_ACTION_3"] = "Comprehensive testing protocols and performance monitoring"
        
#         defaults["RISK_STAGE_4"] = "Production and evaluation of pilot batch"
#         defaults["RISK_DESCRIPTION_4"] = "Scale-up difficulties and quality assurance"
#         defaults["CRITICAL_POINT_4"] = "Maintaining quality and performance at scale"
#         defaults["MITIGATION_ACTION_4"] = "Pilot testing program and quality management systems"
        
#         return defaults
    
#     def auto_generate_missing_fields(self, business_idea, missing_fields):
#         """Auto-generate missing fields using AI"""
#         generated_data = {}
        
#         # Get smart defaults as base
#         smart_defaults = self.generate_smart_defaults({}, business_idea)
        
#         # For each missing field, generate contextual value
#         for category, fields in missing_fields.items():
#             for field in fields:
#                 if field in smart_defaults:
#                     # Use smart default as base and enhance with AI if needed
#                     generated_data[field] = smart_defaults[field]
#                 else:
#                     # Generate using AI for specific context
#                     generated_value = self.ai_generate_field_value(field, business_idea)
#                     generated_data[field] = generated_value
        
#         return generated_data
    
#     def ai_generate_field_value(self, field, business_idea):
#         """Generate a specific field value using AI"""
#         field_descriptions = self.get_field_descriptions()
#         description = field_descriptions.get(field, field)
        
#         prompt = f"""
#         Based on this business idea: {business_idea}
        
#         Generate a realistic value for the field: {field}
#         Field description: {description}
        
#         Generate only the value, no explanation. Make it realistic and appropriate for a Lithuanian R&D project.
#         """
        
#         try:
#             response = self.ai_helper.generate_response(prompt, max_tokens=100)
#             return response.strip()
#         except Exception as e:
#             print(f"Error generating field {field}: {e}")
#             return f"Generated value for {field}"
    
#     def process_business_idea(self, processed_business_idea):
#         """Main processing function"""
#         print(f"Processing business idea for comprehensive data extraction...")
        
#         # Extract data using AI
#         extracted_data = self.extract_comprehensive_data(processed_business_idea)
        
#         # Identify missing fields
#         missing_fields = self.identify_missing_fields(extracted_data)
        
#         # Generate smart defaults
#         smart_defaults = self.generate_smart_defaults(extracted_data, processed_business_idea)
        
#         # Get field descriptions
#         field_descriptions = self.get_field_descriptions()
        
#         # Enhanced UI options
#         user_options = {
#             "auto_generate": "🤖 Auto-Generate All Missing Fields",
#             "manual_input": "✋ Manual Input for All Fields", 
#             "hybrid": "🔄 Hybrid Approach (Choose per field)"
#         }
        
#         return {
#             "extracted_data": extracted_data,
#             "missing_fields": missing_fields,
#             "smart_defaults": smart_defaults,
#             "field_descriptions": field_descriptions,
#             "user_options": user_options,
#             "auto_generation_available": True,
#             "total_fields": sum(len(fields) for fields in self.required_fields.values()),
#             "extracted_count": len([v for v in extracted_data.values() if v is not None]),
#             "missing_count": sum(len(fields) for fields in missing_fields.values())
#         }