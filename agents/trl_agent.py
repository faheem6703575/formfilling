from utils.ai_helper import AIHelper
from config import TRL_DEFINITIONS
import json

class EnhancedTRLAgent:
    def __init__(self):
        self.ai_helper = AIHelper()
    
    def assess_trl_level(self, idea_text):
        """Assess current TRL level of the idea"""
        prompt = f"""
        You are an expert technology assessor specializing in Technology Readiness Level (TRL) evaluations. Your task is to conduct a thorough and precise assessment of the following business idea.

        TRL REFERENCE FRAMEWORK:
        {json.dumps(TRL_DEFINITIONS, indent=2)}

        BUSINESS IDEA TO ASSESS:
        {idea_text}
       
        
        MOST IMPORTATNT NOTE:
        IMPORTANT NOTE -> IF the input is greater then 10 characters then dont check its TRL level its should remains the same okay.

        ASSESSMENT INSTRUCTIONS:
        Conduct a comprehensive analysis following these steps:

        1. TECHNOLOGY IDENTIFICATION:
        - Identify the core technology components within this idea
        - Distinguish between existing technologies and novel innovations
        - Assess the technological complexity and interdependencies

        2. EVIDENCE EVALUATION:
        - Look for indicators of research, development, or validation activities
        - Assess the depth of technical understanding demonstrated
        - Evaluate any mentions of testing, prototyping, or implementation

        3. TRL DETERMINATION:
        - Compare the idea's current state against each TRL level criteria
        - Identify the highest TRL level that is fully supported by evidence
        - Be conservative in your assessment - require clear evidence for each level

        4. GAP ANALYSIS:
        - Identify specific activities that have been completed
        - Determine critical missing elements for the next TRL level
        - Prioritize the most important remaining activities

        IMPORTANT CRITERIA:
        - TRL 1: Basic scientific principles must be documented and observed
        - TRL 2: Practical applications must be clearly formulated with theoretical foundation
        - TRL 3: Requires experimental proof of concept or analytical studies
        - TRL 4: Needs laboratory validation of component/subsystem performance
        - TRL 5+: Requires testing in realistic environments

        OUTPUT FORMAT (strict JSON):
        {{
            "current_trl": [1-9],
            "confidence_level": "[high/medium/low]",
            "evidence": "Detailed explanation of why this TRL level is appropriate, citing specific elements from the idea",
            "technology_components": ["List of key technological elements identified"],
            "completed_activities": ["Specific activities that provide evidence of current TRL level"],
            "remaining_activities": ["Prioritized list of activities needed to advance to next TRL level"],
            "risk_factors": ["Potential technical or implementation risks identified"],
            "assessment_notes": "Additional insights or considerations for this evaluation"
        }}

        Be thorough, objective, and provide clear reasoning for your assessment.

        MOST IMPORTATNT NOTE:
        IMPORTANT NOTE -> IF the input is greater then 10 characters then dont check its TRL level its should remains the same okay.
        """
        
        response = self.ai_helper.generate_response(prompt)
        result = self.ai_helper.extract_json_from_response(response)
        
        if result:
            return result
        else:
            # Fallback if JSON parsing fails
            return {
                "current_trl": 2,
                "confidence_level": "low",
                "evidence": "Unable to parse assessment - requires manual review",
                "technology_components": [],
                "completed_activities": [],
                "remaining_activities": ["Complete comprehensive TRL assessment"],
                "risk_factors": ["Assessment parsing failure"],
                "assessment_notes": "JSON parsing failed - manual assessment required"
            }
    
    def upgrade_to_trl4(self, idea_text, current_assessment):
        """Upgrade idea to TRL 4 level"""
        current_trl = current_assessment.get("current_trl", 2)
        
        if current_trl >= 4:
            return {
                "upgraded_idea": idea_text,
                "changes_made": "No changes needed - already at TRL 4+",
                "trl_level": current_trl,
                "validation_activities": "Current TRL level meets or exceeds TRL 4 requirements"
            }
        
        prompt = f"""
        You are a technology development strategist tasked with advancing a business idea to TRL 4 "Technology validated in laboratory environment."

        ORIGINAL BUSINESS IDEA:
        {idea_text}

        CURRENT TRL ASSESSMENT:
        - Current TRL Level: {current_trl}
        - Evidence: {current_assessment.get('evidence', '')}
        - Technology Components: {current_assessment.get('technology_components', [])}
        - Completed Activities: {current_assessment.get('completed_activities', [])}
        - Risk Factors: {current_assessment.get('risk_factors', [])}

        TRL 4 REQUIREMENTS:
        To achieve TRL 4, the technology must demonstrate:
        1. Laboratory validation of individual components or subsystems
        2. Proof-of-concept demonstrations in controlled environments
        3. Technical feasibility confirmation through testing
        4. Initial prototype development and validation
        5. Performance metrics and benchmarking data
        6. Risk assessment with mitigation strategies
        7. Technical specifications and design documentation

        UPGRADE STRATEGY:
        Transform the original idea by incorporating these specific elements:

        1. LABORATORY VALIDATION FRAMEWORK:
        - Design controlled testing environments
        - Establish measurable performance criteria
        - Create validation protocols and procedures
        - Define success metrics and acceptance criteria

        2. PROOF-OF-CONCEPT DEVELOPMENT:
        - Develop functional prototypes or demonstrations
        - Create testable components that validate core concepts
        - Design experiments that prove technical feasibility
        - Document experimental procedures and results

        3. TECHNICAL MATURITY INDICATORS:
        - Add specific technical specifications
        - Include performance benchmarks and targets
        - Incorporate design constraints and requirements
        - Reference relevant technical standards or methodologies

        4. RISK MANAGEMENT:
        - Identify technical risks and mitigation strategies
        - Address scalability and implementation challenges
        - Consider integration requirements and dependencies
        - Plan for performance optimization and refinement

        5. DOCUMENTATION AND EVIDENCE:
        - Include references to testing procedures
        - Mention prototype development activities
        - Describe validation methodologies
        - Reference technical documentation and specifications

        IMPORTANT GUIDELINES:
        - Maintain the core business value proposition
        - Ensure all additions are technically credible and realistic
        - Focus on laboratory-scale validation rather than full deployment
        - Emphasize component-level rather than system-level maturity
        - Keep the language professional and technically accurate

        OUTPUT REQUIREMENTS:
        Provide a comprehensive, enhanced version of the original idea that clearly demonstrates TRL 4 readiness. The upgraded idea should read as a mature technology development project with clear evidence of laboratory validation activities.

        Include specific details about:
        - Testing environments and methodologies
        - Prototype development and validation results
        - Technical specifications and performance metrics
        - Risk assessment and mitigation strategies
        - Next-phase development planning
        """
        
        upgraded_idea = self.ai_helper.generate_response(prompt)
        
        return {
            "upgraded_idea": upgraded_idea,
            "changes_made": f"Enhanced from TRL {current_trl} to TRL 4 through laboratory validation framework",
            "trl_level": 4,
            "validation_activities": "Added laboratory testing, proof-of-concept development, technical specifications, and risk management components"
        }
    
    def process_idea(self, idea_text):
        """Main TRL processing function"""
        # Step 1: Assess current TRL
        assessment = self.assess_trl_level(idea_text)
        
        # Step 2: Upgrade to TRL 4 if needed
        upgrade_result = self.upgrade_to_trl4(idea_text, assessment)
        
        return {
            "original_idea": idea_text,
            "trl_assessment": assessment,
            "upgrade_result": upgrade_result
        }
