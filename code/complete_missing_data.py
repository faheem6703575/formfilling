import os
import json
import sys
from typing import Dict, List, Any, Optional
from groq import Groq
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCompletionAgent:
    """
    Agent that completes missing data using three approaches:
    1. AI-powered completion
    2. Manual user input
    3. Hybrid approach (AI suggestions with user approval)
    """
    
    def __init__(self, groq_api_key: str = None):
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY must be provided or set as environment variable")
        self.client = Groq(api_key=self.groq_api_key)
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
        # Required fields for validation (based on comprehensive_data_agent.py)
        self.required_fields = {
            "company_info": [
                "COMPANY_NAME", "COMPANY_CODE", "MANAGER_POSITION", "MANAGER_NAME", 
                "COMPLETION_DATE", "MAIN_ACTIVITY", "ACTIVITY_PERCENTAGE", "CESE_CLASS",
                "N_L_E", "I_C", "Sharehol", "A_S_Ns", "SHARE_HS",
                "S_H", "S_I", "S_S", "MANAGER_TITLE", "SUMMARY_1", "INNOVATIVENESS",
                "E_S_RES", "E_S_R&D", "E_S_R", "A_S_RES", "A_S_R&D", "A_S_R", 
                "A_S_P", "N_E", "N_R", "N_T", "N_W_T", "N_P_T", 
                "LITERATURE_REVIEW", "IPR", "COMMERCIALIZATION", "COLLABORATION", 
                "LITERATURE_SOURCES", "RD_JUSTIFICATION_1", "RD_JUSTIFICATION_2", 
                "RD_JUSTIFICATION_3", "RD_JUSTIFICATION_4", "RD_JUSTIFICATION_5",
                "MARKET_ANALYSIS", "PRODUCT_PRICING", "PRICING_JUSTIFICATION", 
                "RD_ACTIVITIES_PLAN"
            ],
            "project_details": [
                "PRODUCT_NAME", "JUS_PRO", "NOVELTY_LEVEL", "JUS_R_D_I", "RD_PRIORITY",
                "RESEARCH_AREA", "PROJECT_KEYWORDS", "PROJECT_TYPE", "PROJECT_SUBTOPIC",
                "N_As", "F_Os", "S_Us", "W_R_Ds", "PRODUCTS_OFFERED", "PER_SALES"
            ],
            "financial_data": [
                "RD_BUDGET", "REVENUE_PROJECTION", "REVENUE_RATIO",
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
                "RISK_FACTORS", "MITIGATION_STRATEGIES", "SUCCESS_PROBABILITY"
            ]
        }

    def run_data_validation(self, data_file_path: str = "code/finalInput.txt") -> Dict[str, Any]:
        """
        Run data validation and return completeness results
        """
        try:
            # Import validation agent
            from data_validation_agent import DataValidationAgent
            
            validator = DataValidationAgent()
            validation_results = validator.validate_all_prompts(data_file_path)
            
            completeness_score = validation_results.get("overall_completeness_score", 0)
            missing_fields = validation_results.get("summary", {}).get("all_missing_fields", [])
            
            print(f"✅ Data Completeness: {completeness_score:.2f}%")
            if missing_fields:
                print(f"⚠️ {len(missing_fields)} fields may need attention")
            
            return {
                "completeness_score": completeness_score,
                "missing_fields": missing_fields,
                "validation_results": validation_results,
                "needs_completion": completeness_score < 99
            }
            
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            return {
                "completeness_score": 0,
                "missing_fields": ["Validation failed"],
                "error": str(e),
                "needs_completion": True
            }

    def complete_missing_data(self, data_file_path: str = "code/finalInput.txt") -> str:
        """
        Main function to complete missing data with user choice of approach
        """
        print("🔍 Running Data Validation...")
        validation_results = self.run_data_validation(data_file_path)
        
        missing_fields = validation_results.get("missing_fields", [])
        meaningful_missing_fields = [f for f in missing_fields if f and f not in ["None", "Unable to parse detailed analysis"]]
        
        if not meaningful_missing_fields:
            print("✅ No meaningful missing fields found")
            return data_file_path
        
        print(f"📊 Found {len(meaningful_missing_fields)} fields that can be completed")
        
        print("\n" + "="*80)
        print("📋 MISSING DATA COMPLETION OPTIONS")
        print("="*80)
        print("Choose how you would like to fill the missing information:")
        print("\n1. 🤖 AI-Powered Completion")
        print("   - AI will analyze your data and intelligently fill missing fields")
        print("   - Fast and automated based on existing context")
        print("   - Uses advanced language models for realistic data generation")
        
        print("\n2. ✍️ Manual User Input")
        print("   - You will be prompted to manually enter each missing field")
        print("   - Full control over every piece of information")
        print("   - Ensures 100% accuracy according to your specifications")
        
        print("\n3. 🔄 Hybrid Approach")
        print("   - AI generates suggestions for each missing field")
        print("   - You review and approve/modify each suggestion")
        print("   - Best of both worlds: speed + accuracy")
        
        print("\n" + "="*80)
        
        # Get user choice
        while True:
            choice = input("\nPlease choose an option (1, 2, or 3): ").strip()
            
            if choice == "1":
                return self._ai_completion(data_file_path, validation_results)
            elif choice == "2":
                return self._manual_completion(data_file_path, validation_results)
            elif choice == "3":
                return self._hybrid_completion(data_file_path, validation_results)
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

    def _ai_completion(self, data_file_path: str, validation_results: Dict[str, Any]) -> str:
        """
        AI-powered completion of missing fields
        """
        print("\n🤖 Starting AI-Powered Data Completion...")
        
        # Read current data
        with open(data_file_path, 'r', encoding='utf-8') as file:
            current_data = file.read()
        
        missing_fields = validation_results.get("missing_fields", [])
        meaningful_missing_fields = [f for f in missing_fields if f and f not in ["None", "Unable to parse detailed analysis"]]
        
        print(f"🔍 Analyzing {len(meaningful_missing_fields)} missing fields...")
        
        # Generate AI completions for missing fields
        completed_data = {}
        
        for field in meaningful_missing_fields[:20]:  # Limit to prevent too many API calls
            if field:
                print(f"🤖 Generating completion for: {field}")
                
                try:
                    ai_value = self._generate_ai_field_value(field, current_data)
                    completed_data[field] = ai_value
                    print(f"   ✅ Generated: {ai_value[:100]}...")
                    
                except Exception as e:
                    logger.error(f"Error generating AI value for {field}: {e}")
                    completed_data[field] = f"[AI_GENERATED_PLACEHOLDER_{field}]"
        
        # Append to file
        return self._append_completed_data(data_file_path, completed_data, "AI-GENERATED")

    def _manual_completion(self, data_file_path: str, validation_results: Dict[str, Any]) -> str:
        """
        Manual user input completion of missing fields
        """
        print("\n✍️ Starting Manual Data Completion...")
        
        missing_fields = validation_results.get("missing_fields", [])
        meaningful_missing_fields = [f for f in missing_fields if f and f not in ["None", "Unable to parse detailed analysis"]]
        completed_data = {}
        
        print(f"📝 Please provide information for {len(meaningful_missing_fields)} missing fields:")
        print("(Press Enter to skip a field, type 'quit' to stop)\n")
        
        for i, field in enumerate(meaningful_missing_fields[:20], 1):
            if field:
                print(f"[{i}/{min(len(missing_fields), 20)}] {field}:")
                
                # Provide context/description for the field
                field_description = self._get_field_description(field)
                if field_description:
                    print(f"   💡 {field_description}")
                
                user_input = input("   Enter value: ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input:
                    completed_data[field] = user_input
                    print(f"   ✅ Saved: {user_input[:100]}...")
                else:
                    print("   ⏭️ Skipped")
        
        return self._append_completed_data(data_file_path, completed_data, "USER-PROVIDED")

    def _hybrid_completion(self, data_file_path: str, validation_results: Dict[str, Any]) -> str:
        """
        Hybrid completion: AI suggestions with user approval
        """
        print("\n🔄 Starting Hybrid Data Completion...")
        
        # Read current data
        with open(data_file_path, 'r', encoding='utf-8') as file:
            current_data = file.read()
        
        missing_fields = validation_results.get("missing_fields", [])
        meaningful_missing_fields = [f for f in missing_fields if f and f not in ["None", "Unable to parse detailed analysis"]]
        completed_data = {}
        
        print(f"🤖 AI will suggest values for {len(meaningful_missing_fields)} missing fields.")
        print("You can approve, modify, or skip each suggestion.\n")
        
        for i, field in enumerate(meaningful_missing_fields[:20], 1):
            if field:
                print(f"\n[{i}/{min(len(missing_fields), 20)}] {field}:")
                
                # Generate AI suggestion
                try:
                    ai_suggestion = self._generate_ai_field_value(field, current_data)
                    print(f"🤖 AI Suggestion: {ai_suggestion}")
                    
                    while True:
                        choice = input("   [A]ccept / [M]odify / [S]kip / [Q]uit: ").lower().strip()
                        
                        if choice in ['a', 'accept']:
                            completed_data[field] = ai_suggestion
                            print(f"   ✅ Accepted AI suggestion")
                            break
                        elif choice in ['m', 'modify']:
                            user_input = input("   Enter your value: ").strip()
                            if user_input:
                                completed_data[field] = user_input
                                print(f"   ✅ Saved modified value")
                            break
                        elif choice in ['s', 'skip']:
                            print("   ⏭️ Skipped")
                            break
                        elif choice in ['q', 'quit']:
                            print("   🛑 Stopping completion process")
                            return self._append_completed_data(data_file_path, completed_data, "HYBRID")
                        else:
                            print("   ❌ Invalid choice. Please enter A, M, S, or Q.")
                
                except Exception as e:
                    logger.error(f"Error generating AI suggestion for {field}: {e}")
                    print(f"   ❌ Could not generate AI suggestion. Please enter manually:")
                    user_input = input("   Enter value: ").strip()
                    if user_input:
                        completed_data[field] = user_input
        
        return self._append_completed_data(data_file_path, completed_data, "HYBRID")

    def _generate_ai_field_value(self, field_name: str, current_data: str) -> str:
        """
        Generate AI value for a specific field based on current data context
        """
        prompt = f"""
Based on the following project data, generate a realistic and appropriate value for the field "{field_name}".

CONTEXT DATA:
{current_data[:3000]}...

FIELD TO COMPLETE: {field_name}

INSTRUCTIONS:
1. Analyze the existing data to understand the project context
2. Generate a realistic value that fits the project type and domain
3. Ensure the value is specific, detailed, and professional
4. For numerical fields, provide realistic numbers based on project scale
5. For text fields, provide meaningful descriptions (2-3 sentences minimum)
6. Maintain consistency with the existing project information

FIELD DESCRIPTION: {self._get_field_description(field_name)}

Generate ONLY the value for this field, without explanations or formatting:
"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional project data analyst. Generate realistic, detailed, and contextually appropriate field values based on project data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI value: {e}")
            return f"[Generated value for {field_name}]"

    def _get_field_description(self, field_name: str) -> str:
        """
        Get description/context for a field to help user understand what to enter
        """
        field_descriptions = {
            "COMPANY_NAME": "Full legal name of your company/organization",
            "COMPANY_CODE": "Official company registration code or ID number",
            "MANAGER_NAME": "Full name of the project manager",
            "MANAGER_POSITION": "Job title/position of the project manager",
            "COMPLETION_DATE": "Expected project completion date (YYYY-MM-DD)",
            "MAIN_ACTIVITY": "Primary business activity or research focus",
            "PRODUCT_NAME": "Name of the main product or service being developed",
            "RD_BUDGET": "Research & Development budget amount in EUR",
            "RESEARCH_AREA": "Scientific or technical research domain",
            "PROJECT_KEYWORDS": "Key terms that describe your project (comma-separated)",
            "MARKET_ANALYSIS": "Analysis of target market and opportunities",
            "COMPETITOR_M": "Information about main competitors",
            "RISK_FACTORS": "Potential risks and challenges for the project",
            "CURRENT_TPL": "Current Technology Readiness Level (1-9)",
            "TARGET_TPL": "Target Technology Readiness Level (1-9)",
            "REVENUE_PROJECTION": "Expected revenue from project in EUR",
            "JOBS_DURING_PROJECT": "Number of jobs created during project execution",
            "JOBS_AFTER_PROJECT": "Number of jobs to be maintained after project completion"
        }
        
        return field_descriptions.get(field_name, f"Information related to {field_name}")

    def _append_completed_data(self, data_file_path: str, completed_data: Dict[str, str], completion_type: str) -> str:
        """
        Append completed data to the original file
        """
        if not completed_data:
            print("❌ No data was completed.")
            return data_file_path
        
        try:
            with open(data_file_path, 'a', encoding='utf-8') as file:
                file.write(f"\n\n--- {completion_type} DATA COMPLETION ---\n")
                file.write(f"Completion Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Fields Completed: {len(completed_data)}\n\n")
                
                for field, value in completed_data.items():
                    file.write(f"{field}: {value}\n")
                    
            print(f"\n✅ Successfully added {len(completed_data)} completed fields to {data_file_path}")
            print(f"📄 File updated with {completion_type} completion")
            
            # Run validation again to show improvement
            print("\n🔍 Re-running validation to check improvement...")
            new_validation = self.run_data_validation(data_file_path)
            
            print(f"📈 Data Completeness improved to: {new_validation.get('completeness_score', 0):.2f}%")
            
            return data_file_path
            
        except Exception as e:
            logger.error(f"Error appending completed data: {e}")
            print(f"❌ Error updating file: {e}")
            return data_file_path


def run_complete_missing_data():
    """
    Main function to run the complete missing data process
    """
    try:
        print("🚀 Starting Data Completion Process...")
        print("="*80)
        
        completion_agent = DataCompletionAgent()
        
        # Use the finalInput.txt file path
        data_file_path = r"C:\Users\USER\Documents\final\code\finalInput.txt"
        
        # Run the completion process
        updated_file = completion_agent.complete_missing_data(data_file_path)
        
        print(f"\n🎉 Data completion process finished!")
        print(f"📄 Updated file: {updated_file}")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error in data completion process: {e}")
        logger.error(f"Error in data completion: {e}")


if __name__ == "__main__":

    run_complete_missing_data()
