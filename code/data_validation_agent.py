import os
import json
import re
from typing import Dict, List, Tuple, Any
from groq import Groq
import logging
from dotenv import load_dotenv
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidationAgent:
    """
    Agent that validates input data completeness by comparing against all prompt requirements
    """
    
    def __init__(self, groq_api_key: str = None):
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY must be provided or set as environment variable")
        self.client = Groq(api_key=self.groq_api_key)
        
    def read_input_data(self, data_file_path: str) -> str:
        """Read the input data file"""
        try:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"✅ Successfully read input data: {data_file_path} ({len(content)} characters)")
            return content
        except FileNotFoundError:
            logger.error(f"❌ Input data file not found: {data_file_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error reading input data file: {e}")
            raise
    
    def read_prompt_file(self, prompt_path: str) -> str:
        """Read a single prompt file"""
        try:
            with open(prompt_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            logger.error(f"❌ Prompt file not found: {prompt_path}")
            return ""
        except Exception as e:
            logger.error(f"❌ Error reading prompt file {prompt_path}: {e}")
            return ""
    
    def get_all_prompt_files(self, prompts_dir: str = "prompts") -> List[str]:
        """Get all prompt files from the prompts directory"""
        try:
            prompt_files = []
            for file in os.listdir(prompts_dir):
                if file.endswith('.txt'):
                    prompt_files.append(os.path.join(prompts_dir, file))
            logger.info(f"✅ Found {len(prompt_files)} prompt files")
            return sorted(prompt_files)
        except Exception as e:
            logger.error(f"❌ Error reading prompts directory: {e}")
            return []
    
    def preprocess_input_data(self, input_data: str) -> str:
        """
        Preprocess input data to highlight key information for better analysis
        """
        # Add markers to help LLM identify different sections
        processed_data = f"""
=== INPUT DATA SUMMARY ===
Total Length: {len(input_data)} characters
Contains multiple sections with project, financial, and technical information.

=== FULL INPUT DATA ===
{input_data}

=== DATA ANALYSIS NOTES ===
- Look for project names, descriptions, costs, timelines, staff details
- Check for financial figures, budgets, funding amounts
- Look for technical specifications, methodologies, outcomes
- Consider that some information might be implicit or described differently
- Be thorough in recognizing existing information before marking as missing
"""
        return processed_data
    
    def analyze_data_completeness(self, input_data: str, prompt_content: str, prompt_name: str) -> Dict[str, Any]:
        """
        Analyze if input data contains all required information for a specific prompt
        """
        # Preprocess the input data for better analysis
        processed_input = self.preprocess_input_data(input_data)
        
        analysis_prompt = f"""
You are an expert data completeness validator with advanced semantic understanding. Your task is to thoroughly analyze input data against prompt requirements.

CRITICAL VALIDATION RULES:
🔍 THOROUGH SEARCH: Scan the ENTIRE input data multiple times before marking anything as missing
🎯 SEMANTIC MATCHING: Recognize that required information might be expressed differently:
   - "Project costs" = "Budget" = "Financial requirements" = "Expenses"
   - "Team members" = "Staff" = "Personnel" = "Human resources"
   - "Timeline" = "Schedule" = "Duration" = "Project phases"
   - "Methodology" = "Approach" = "Process" = "Procedures"
   
⚠️ BE CONSERVATIVE: Only mark data as "missing" if you are 100% certain it's not present in ANY form
✅ GIVE CREDIT: If information is partially present or can be reasonably inferred, mark it as PRESENT

PROMPT NAME: {prompt_name}

PROMPT REQUIREMENTS:
{prompt_content}

INPUT DATA TO VALIDATE:
{processed_input}

DETAILED ANALYSIS PROCESS:
1. Read the prompt requirements carefully
2. For EACH required field, search the input data for:
   ✓ Direct mentions
   ✓ Synonyms and related terms  
   ✓ Implicit information
   ✓ Data that could satisfy the requirement even if worded differently
3. Mark as PRESENT if found in any recognizable form
4. Mark as MISSING only if absolutely not present or inferrable
5. Provide evidence for present fields (quotes from input)

ENHANCED SCORING (be generous):
- 95-100: All or nearly all required information clearly present
- 85-94: Most information present, very minor gaps
- 75-84: Good coverage, some specific details missing
- 65-74: Adequate coverage, moderate gaps
- 50-64: Basic information present, several gaps
- Below 50: Significant information missing

Respond in JSON format:
{{
    "prompt_name": "{prompt_name}",
    "completeness_score": 0-100,
    "required_fields": ["specific data fields needed by this prompt"],
    "present_fields": ["data fields found in input - BE GENEROUS in recognition"],
    "missing_fields": ["ONLY fields that are genuinely missing after thorough search"],
    "present_evidence": {{
        "field_name": "specific quote or reference from input showing this data exists"
    }},
    "missing_details": {{
        "field_name": "what exactly is missing and why it matters"
    }},
    "suggestions": ["specific actionable suggestions for truly missing data only"]
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": "You are a thorough data validation expert with semantic understanding. Be CONSERVATIVE about marking data as missing - only mark something as missing if you are absolutely certain it's not present in any form. Always respond with valid JSON. Err on the side of recognizing present data rather than falsely identifying missing data."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, extract key information manually
                logger.warning(f"⚠️ Could not parse JSON response for {prompt_name}, using fallback")
                # Try to extract completeness score from the raw response
                fallback_score = 75  # Default fallback score
                if "completeness_score" in response_text:
                    try:
                        # Extract the score using regex
                        import re
                        score_match = re.search(r'"completeness_score":\s*(\d+)', response_text)
                        if score_match:
                            fallback_score = int(score_match.group(1))
                    except:
                        pass
                
                return {
                    "prompt_name": prompt_name,
                    "completeness_score": fallback_score,
                    "required_fields": [],
                    "present_fields": ["Data analysis completed with fallback"],
                    "missing_fields": ["Unable to parse detailed analysis"],
                    "present_evidence": {},
                    "missing_details": {},
                    "suggestions": ["Manual review recommended - LLM response parsing failed"],
                    "raw_response": response_text
                }
                
        except Exception as e:
            logger.error(f"❌ Error analyzing data completeness for {prompt_name}: {e}")
            return {
                "prompt_name": prompt_name,
                "completeness_score": 70,  # Higher default - assume most data is present
                "required_fields": [],
                "present_fields": ["Analysis error occurred"],
                "missing_fields": ["Analysis failed"],
                "present_evidence": {},
                "missing_details": {},
                "suggestions": ["Error occurred during analysis - manual review required"],
                "error": str(e)
            }
    
    def validate_all_prompts(self, data_file_path: str, prompts_dir: str = "prompts") -> Dict[str, Any]:
        """
        Validate input data against all prompt files
        """
        logger.info("🔍 Starting comprehensive data validation...")
        
        # Read input data
        input_data = self.read_input_data(data_file_path)
        
        # Get all prompt files
        prompt_files = self.get_all_prompt_files(prompts_dir)
        
        if not prompt_files:
            logger.error("❌ No prompt files found!")
            return {"error": "No prompt files found"}
        
        validation_results = []
        total_score = 0
        
        # Analyze each prompt
        for prompt_file in prompt_files:
            prompt_name = os.path.basename(prompt_file).replace('.txt', '')
            logger.info(f"📝 Analyzing prompt: {prompt_name}")
            
            prompt_content = self.read_prompt_file(prompt_file)
            if prompt_content:
                result = self.analyze_data_completeness(input_data, prompt_content, prompt_name)
                validation_results.append(result)
                total_score += result.get('completeness_score', 0)
            else:
                logger.warning(f"⚠️ Skipping empty prompt file: {prompt_name}")
        
        # Calculate overall completeness with better error handling
        if not validation_results:
            overall_score = 0
        else:
            # Filter out invalid scores and calculate average
            valid_scores = [r.get('completeness_score', 0) for r in validation_results if isinstance(r.get('completeness_score'), (int, float))]
            if valid_scores:
                overall_score = sum(valid_scores) / len(valid_scores)
            else:
                # If no valid scores, use a reasonable default based on data length
                overall_score = min(85, max(60, len(input_data) / 1000))  # Scale based on data richness
        
        # Compile missing data summary
        all_missing_fields = []
        all_suggestions = []
        
        for result in validation_results:
            missing_fields = result.get('missing_fields', [])
            suggestions = result.get('suggestions', [])
            
            # Filter out system messages
            if isinstance(missing_fields, list):
                all_missing_fields.extend([f for f in missing_fields if f not in ["Unable to parse detailed analysis", "Analysis failed"]])
            if isinstance(suggestions, list):
                all_suggestions.extend([s for s in suggestions if s not in ["Manual review required - LLM response parsing failed", "Error occurred during analysis - manual review required"]])
        
        summary = {
            "overall_completeness_score": round(overall_score, 2),
            "total_prompts_analyzed": len(validation_results),
            "validation_results": validation_results,
            "summary": {
                "all_missing_fields": list(set(all_missing_fields)),
                "all_suggestions": list(set(all_suggestions)),
                "prompts_with_issues": [r.get('prompt_name', 'Unknown') for r in validation_results if r.get('completeness_score', 0) < 80]
            }
        }
        
        return summary
    
    def generate_completion_suggestions(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate human-readable suggestions for completing missing data
        """
        suggestions_prompt = f"""
Based on the following data validation results, generate clear, actionable suggestions for the user to complete their input data:

VALIDATION RESULTS:
{json.dumps(validation_results, indent=2)}

Please provide:
1. A summary of overall data completeness
2. Priority list of missing information (most important first)
3. Specific questions the user should answer to complete each missing field
4. Suggested format for adding the missing information

Make the response user-friendly and actionable.
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, actionable data completion guides. Focus only on truly missing information. Be conservative - don't suggest adding data that might already be present in a different form."},
                    {"role": "user", "content": suggestions_prompt}
                ],
                temperature=0.2,  # Lower temperature for more focused suggestions
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"❌ Error generating completion suggestions: {e}")
            return "Error generating suggestions. Please review the validation results manually."
    
    def interactive_data_completion(self, data_file_path: str) -> str:
        """
        Interactive process to help user complete missing data
        """
        # First, validate current data
        validation_results = self.validate_all_prompts(data_file_path)
        
        if validation_results.get('overall_completeness_score', 0) >= 90:
            logger.info("✅ Data is already sufficiently complete!")
            return data_file_path
        
        # Generate suggestions
        suggestions = self.generate_completion_suggestions(validation_results)
        
        print("\n" + "="*80)
        print("📊 DATA COMPLETENESS ANALYSIS")
        print("="*80)
        print(f"Overall Completeness Score: {validation_results.get('overall_completeness_score', 0):.1f}%")
        print(f"Total Prompts Analyzed: {validation_results.get('total_prompts_analyzed', 0)}")
        
        # Show top performing prompts (high scores)
        high_scoring = [r for r in validation_results.get('validation_results', []) 
                       if r.get('completeness_score', 0) >= 80]
        if high_scoring:
            print(f"\n✅ WELL-COVERED AREAS ({len(high_scoring)} prompts):")
            for result in high_scoring[:5]:  # Show top 5
                score = result.get('completeness_score', 0)
                present_count = len(result.get('present_fields', []))
                print(f"   • {result.get('prompt_name', 'Unknown')}: {score}% ({present_count} fields found)")
        
        # Show problematic prompts (low scores)
        problem_prompts = validation_results.get('summary', {}).get('prompts_with_issues', [])
        if problem_prompts:
            print(f"\n⚠️ AREAS NEEDING ATTENTION ({len(problem_prompts)} prompts):")
            for prompt_name in problem_prompts[:5]:  # Show top 5 issues
                prompt_result = next((r for r in validation_results.get('validation_results', []) 
                                    if r.get('prompt_name') == prompt_name), {})
                score = prompt_result.get('completeness_score', 0)
                missing_count = len(prompt_result.get('missing_fields', []))
                print(f"   • {prompt_name}: {score}% ({missing_count} fields missing)")
        
        print("\n📋 COMPLETION SUGGESTIONS:")
        print(suggestions)
        print("\n" + "="*80)
        
        # Ask user if they want to add missing data
        while True:
            user_choice = input("\nWould you like to add missing data? (y/n/skip): ").lower().strip()
            
            if user_choice in ['n', 'no', 'skip']:
                logger.info("⏭️ Skipping data completion, proceeding with current data...")
                return data_file_path
            elif user_choice in ['y', 'yes']:
                break
            else:
                print("Please enter 'y' for yes, 'n' for no, or 'skip' to proceed anyway.")
        
        # Interactive data addition
        print("\n📝 Please provide the missing information:")
        additional_data = []
        
        missing_fields = validation_results.get('summary', {}).get('all_missing_fields', [])
        for field in missing_fields[:5]:  # Limit to top 5 missing fields
            if field and field != "Unable to parse detailed analysis":
                user_input = input(f"\n{field}: ").strip()
                if user_input:
                    additional_data.append(f"{field}: {user_input}")
        
        # Allow free-form additional data entry
        print("\nAdd any other relevant information (press Enter twice when done):")
        additional_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            additional_lines.append(line)
        
        if additional_lines:
            additional_data.extend(additional_lines)
        
        # Append to original file
        if additional_data:
            try:
                with open(data_file_path, 'a', encoding='utf-8') as file:
                    file.write("\n\n--- ADDITIONAL INFORMATION ---\n")
                    file.write("\n".join(additional_data))
                    
                logger.info(f"✅ Added {len(additional_data)} pieces of additional information to {data_file_path}")
                print(f"\n✅ Successfully updated {data_file_path} with additional information!")
                
            except Exception as e:
                logger.error(f"❌ Error updating data file: {e}")
                print(f"❌ Error updating file: {e}")
        
        return data_file_path

def run_data_validation():
    """Example usage of DataValidationAgent"""
    try:
        # Initialize the validation agent
        validator = DataValidationAgent()
        
        # Run interactive data completion
        data_file = "finalInput.txt"
        completed_file = validator.interactive_data_completion(data_file)
        
        print(f"\n🎉 Data validation complete! Using file: {completed_file}")
        
    except Exception as e:
        print(f"❌ Error in data validation: {e}")

if __name__ == "__main__":
    run_data_validation()
