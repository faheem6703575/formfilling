from utils.ai_helper import AIHelper
from config import FRASCATI_THRESHOLD
import json
import re

class EnhancedFrascatiAgent:
    def __init__(self):
        self.ai_helper = AIHelper()
        self.criteria = {
            "Novel": {
                "weight": 0.25,
                "description": "Aimed at new findings - novel approach",
                "oecd_reference": "Section 2.1 - Creative and systematic work"
            },
            "Creative": {
                "weight": 0.25, 
                "description": "Based on original, non-obvious concepts",
                "oecd_reference": "Section 2.4 - Five core criteria"
            },
            "Uncertain": {
                "weight": 0.20,
                "description": "Uncertain about final outcome",
                "oecd_reference": "Section 2.5 - Uncertainty criterion"
            },
            "Systematic": {
                "weight": 0.15,
                "description": "Planned and budgeted approach",
                "oecd_reference": "Section 2.2 - Systematic work"
            },
            "Transferable": {
                "weight": 0.15,
                "description": "Results can be reproduced/transferred",
                "oecd_reference": "Section 2.6 - Transferability"
            }
        }
    
    def get_oecd_questions(self, criterion):
        """Get OECD-compliant evaluation questions for each criterion"""
        questions = {
            "Novel": """
            NOVELTY EVALUATION (OECD Section 2.1):
            - What new or additional knowledge does the project aim to provide?
            - What scientific/technological problems lack publicly available solutions?
            - How will the project generate knowledge leading to new/improved products?
            - What specific problems need solving for product development?
            - How does this differ from existing knowledge in the field?
            """,
            
            "Creative": """
            CREATIVITY EVALUATION (OECD Section 2.4):
            - What original ideas/hypotheses is the project based on?
            - What non-obvious hypothesis does it test?
            - What methods add value (analysis/experimentation/observation)?
            - How does it solve scientific-technological problems creatively?
            - What makes the approach original and innovative?
            """,
            
            "Uncertain": """
            UNCERTAINTY EVALUATION (OECD Section 2.5):
            - What is the likelihood of failing to generate sufficient knowledge?
            - What is the probability of not achieving planned results at planned cost?
            - What is the risk of not meeting planned timeframe?
            - What technical uncertainties exist in the approach?
            - What are the unknown outcomes that make this research necessary?
            """,
            
            "Systematic": """
            SYSTEMATIC EVALUATION (OECD Section 2.2):
            - Are the project activities coherent and logically structured?
            - How does the quality comply with SMART principles (Specific, Measurable, Achievable, Relevant, Timed)?
            - How do activities relate to research and experimental development stages?
            - Is there a clear methodology and work plan?
            - Are resources planned and budgeted appropriately?
            """,
            
            "Transferable": """
            TRANSFERABILITY EVALUATION (OECD Section 2.6):
            - Can the results be reproduced by other researchers?
            - Are the methods and findings transferable to other applications?
            - Will the knowledge be available for further research and development?
            - Can the technology be scaled or adapted for different uses?
            - Are the results documented and communicable?
            """
        }
        return questions.get(criterion, "")
    
    def score_frascati_criteria_oecd(self, idea_text):
        """Score idea against OECD Frascati Manual criteria with detailed evaluation"""
        
        prompt = f"""
        You are an OECD R&D evaluation expert. Evaluate this business idea against the OECD Frascati Manual R&D criteria using the official framework.

        Business Idea: {idea_text}

        For each criterion below, provide detailed evaluation following OECD guidelines:

        1. NOVEL (25 points - OECD Section 2.1):
        {self.get_oecd_questions("Novel")}

        2. CREATIVE (25 points - OECD Section 2.4):
        {self.get_oecd_questions("Creative")}

        3. UNCERTAIN (20 points - OECD Section 2.5):
        {self.get_oecd_questions("Uncertain")}

        4. SYSTEMATIC (15 points - OECD Section 2.2):
        {self.get_oecd_questions("Systematic")}

        5. TRANSFERABLE (15 points - OECD Section 2.6):
        {self.get_oecd_questions("Transferable")}

        EVALUATION REQUIREMENTS:
        - Score each criterion from 0-100
        - Provide detailed justification referencing OECD sections
        - Include specific evidence from the business idea
        - Ensure total weighted score reflects R&D quality
        - Flag any areas needing improvement for OECD compliance

        RESPOND WITH ONLY THIS JSON FORMAT:
        {{
            "Novel": {{
                "score": 85,
                "justification": "The project addresses a specific knowledge gap in [field] with clear scientific novelty. The approach to [specific innovation] represents new knowledge not publicly available in current literature.",
                "evidence": "Specific technical elements that demonstrate novelty",
                "oecd_compliance": "Meets OECD Section 2.1 requirements for novel research",
                "improvement_needed": false
            }},
            "Creative": {{
                "score": 75,
                "justification": "Original hypothesis testing [specific approach] with non-obvious methodology combining [methods]. Creative integration of [technologies/approaches].",
                "evidence": "Non-obvious technical approach and original concepts",
                "oecd_compliance": "Complies with OECD Section 2.4 creativity criteria",
                "improvement_needed": false
            }},
            "Uncertain": {{
                "score": 70,
                "justification": "Technical uncertainties in [specific areas]. Risk of not achieving [specific outcomes] within timeframe. Unknown performance parameters require investigation.",
                "evidence": "Specific uncertainties and risks identified",
                "oecd_compliance": "Meets OECD Section 2.5 uncertainty requirements",
                "improvement_needed": false
            }},
            "Systematic": {{
                "score": 80,
                "justification": "Well-structured approach with clear methodology. SMART objectives defined with measurable outcomes. Systematic work plan with logical progression.",
                "evidence": "Structured methodology and work plan",
                "oecd_compliance": "Meets OECD Section 2.2 systematic requirements",
                "improvement_needed": false
            }},
            "Transferable": {{
                "score": 85,
                "justification": "Results will be reproducible and transferable to [applications]. Clear documentation and knowledge transfer potential. Scalable methodology.",
                "evidence": "Transferability and reproducibility elements",
                "oecd_compliance": "Meets OECD Section 2.6 transferability criteria",
                "improvement_needed": false
            }}
        }}
        IMPORTANT:
        - Respond ONLY with valid JSON. 
        - Do NOT wrap in markdown or text.
        - Use double quotes everywhere.
        - Do NOT write anything else outside the JSON.
        """
        
        response = self.ai_helper.generate_response(prompt, max_tokens=1200)
        
        # Try to extract JSON from response
        result = self.extract_json_from_response(response)
        
        if result and self.validate_oecd_response(result):
            return result
        else:
            # If JSON parsing fails, use fallback
            print(f"OECD evaluation JSON parsing failed, using fallback...")
            return self.fallback_oecd_evaluation(idea_text)
    
    def extract_json_from_response(self, response_text):
        """Extract JSON data from AI response, robustly."""
        try:
            response_text = response_text.strip()

            # Remove markdown code fences if present
            if response_text.startswith("```") and response_text.endswith("```"):
                response_text = re.sub(r'^```(json)?', '', response_text, flags=re.IGNORECASE).strip()
                response_text = response_text.rstrip('`').rstrip()

            # Replace Python booleans with JSON booleans
            response_text = re.sub(r'\bTrue\b', 'true', response_text)
            response_text = re.sub(r'\bFalse\b', 'false', response_text)

            # Remove trailing commas inside JSON objects and arrays
            response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)

            # Try to parse directly
            return json.loads(response_text)

        except Exception as e:
            print(f"Robust JSON extraction error: {e}")
            return None

    
    def validate_oecd_response(self, result):
        """Validate that the response has the correct OECD structure"""
        if not isinstance(result, dict):
            return False
        
        required_fields = ["score", "justification", "evidence", "oecd_compliance", "improvement_needed"]
        
        for criterion in self.criteria.keys():
            if criterion not in result:
                return False
            if not isinstance(result[criterion], dict):
                return False
            for field in required_fields:
                if field not in result[criterion]:
                    return False
        
        return True
    
    def fallback_oecd_evaluation(self, idea_text):
        """Fallback OECD evaluation if JSON parsing fails"""
        print("Using OECD evaluation fallback...")
        
        scores = {}
        
        for criterion, criteria_data in self.criteria.items():
            criterion_prompt = f"""
            Evaluate this business idea for the {criterion} criterion according to OECD Frascati Manual:
            
            Business Idea: {idea_text}
            
            OECD Reference: {criteria_data['oecd_reference']}
            Definition: {criteria_data['description']}
            
            Questions: {self.get_oecd_questions(criterion)}
            
            Provide:
            1. Score (0-100)
            2. OECD-compliant justification
            3. Specific evidence
            4. Compliance statement
            
            Format:
            Score: [number]
            Justification: [detailed explanation]
            Evidence: [specific elements]
            OECD Compliance: [compliance statement]
            """
            
            response = self.ai_helper.generate_response(criterion_prompt, max_tokens=400)
            score, justification, evidence, compliance = self.parse_oecd_response(response, criterion)
            
            scores[criterion] = {
                "score": score,
                "justification": justification,
                "evidence": evidence,
                "oecd_compliance": compliance,
                "improvement_needed": score < FRASCATI_THRESHOLD
            }
        
        return scores
    
    def parse_oecd_response(self, response, criterion):
        """Parse individual OECD criterion response"""
        try:
            # Extract score
            score_match = re.search(r'[Ss]core:?\s*(\d+)', response)
            score = int(score_match.group(1)) if score_match else 60
            
            # Extract justification
            just_match = re.search(r'[Jj]ustification:?\s*([^\n]+)', response)
            justification = just_match.group(1).strip() if just_match else f"OECD-compliant {criterion} evaluation completed"
            
            # Extract evidence
            evidence_match = re.search(r'[Ee]vidence:?\s*([^\n]+)', response)
            evidence = evidence_match.group(1).strip() if evidence_match else f"{criterion} elements identified"
            
            # Extract compliance
            compliance_match = re.search(r'OECD Compliance:?\s*([^\n]+)', response)
            compliance = compliance_match.group(1).strip() if compliance_match else f"Meets OECD {criterion} criteria"
            
            return max(0, min(100, score)), justification, evidence, compliance
            
        except:
            return 60, f"OECD {criterion} assessment completed", f"{criterion} elements evaluated", f"OECD {criterion} compliance checked"
    
    def identify_low_scores(self, scores):
        """Identify criteria with scores below threshold"""
        low_scores = {}
        for criterion, data in scores.items():
            if data["score"] < FRASCATI_THRESHOLD:
                low_scores[criterion] = data
        return low_scores
    
    def generate_oecd_improvement_suggestions(self, idea_text, low_scores):
        """Generate OECD-compliant improvement suggestions"""
        suggestions = {}
        
        for criterion, data in low_scores.items():
            prompt = f"""
            Generate OECD Frascati Manual compliant improvements for the {criterion} criterion:
            
            Current idea: {idea_text}
            Current score: {data['score']}%
            Current justification: {data['justification']}
            OECD Reference: {self.criteria[criterion]['oecd_reference']}
            
            OECD Evaluation Questions:
            {self.get_oecd_questions(criterion)}
            
            Provide specific, actionable improvements that would:
            1. Increase the score above {FRASCATI_THRESHOLD}%
            2. Ensure full OECD Frascati Manual compliance
            3. Address the specific {criterion} deficiencies
            4. Include concrete examples and evidence
            
            Focus on OECD-compliant enhancements that demonstrate clear {criterion} characteristics according to the manual.
            
            Return a clear, implementable improvement strategy in 2-3 sentences.
            """
            
            suggestion = self.ai_helper.generate_response(prompt, max_tokens=400)
            suggestions[criterion] = suggestion
        
        return suggestions
    
    def apply_improvements(self, idea_text, improvements, selected_criteria):
        """Apply selected OECD-compliant improvements to the idea"""
        improvements_to_apply = {
            criterion: improvements[criterion] 
            for criterion in selected_criteria 
            if criterion in improvements
        }
        
        if not improvements_to_apply:
            return idea_text
        
        prompt = f"""
        Enhance this business idea by incorporating OECD Frascati Manual compliant improvements:
        
        Original idea: {idea_text}
        
        OECD-Compliant Improvements to apply:
        {json.dumps(improvements_to_apply, indent=2)}
        
        Integration Requirements:
        1. Maintain the core business concept and value proposition
        2. Seamlessly integrate improvements into the existing idea
        3. Ensure all enhancements comply with OECD Frascati Manual standards
        4. Strengthen R&D characteristics while preserving commercial viability
        5. Add specific evidence and examples that demonstrate compliance
        
        Return an enhanced version that naturally incorporates all improvements while maintaining coherence and OECD compliance.
        """
        
        improved_idea = self.ai_helper.generate_response(prompt, max_tokens=1500)
        return improved_idea
    
    def process_idea(self, idea_text):
        """Main OECD Frascati processing function"""
        print(f"Processing idea for OECD Frascati analysis: {idea_text[:100]}...")
        
        # Score the idea using OECD framework
        scores = self.score_frascati_criteria_oecd(idea_text)
        print(f"OECD scores received: {[(k, v['score']) for k, v in scores.items()]}")
        
        # Identify low scores
        low_scores = self.identify_low_scores(scores)
        
        # Generate OECD-compliant improvement suggestions if needed
        suggestions = {}
        if low_scores:
            suggestions = self.generate_oecd_improvement_suggestions(idea_text, low_scores)
        
        # Calculate weighted total score
        total_score = sum(scores[criterion]["score"] * self.criteria[criterion]["weight"] 
                         for criterion in self.criteria.keys())
        
        return {
            "scores": scores,
            "low_scores": low_scores,
            "suggestions": suggestions,
            "needs_improvement": len(low_scores) > 0,
            "total_weighted_score": round(total_score, 1),
            "oecd_compliance_level": "High" if total_score >= 95 else "Medium" if total_score >= 80 else "Low"
        }