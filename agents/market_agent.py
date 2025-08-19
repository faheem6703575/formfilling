import requests
from utils.ai_helper import AIHelper
from config import GOOGLE_API_KEY, GOOGLE_SCHOLAR_CSE_ID, GOOGLE_PATENT_CSE_ID
import json

class EnhancedMarketAgent:
    def __init__(self):
        self.ai_helper = AIHelper()
        self.google_api_key = GOOGLE_API_KEY
        self.google_patent_cse_id = GOOGLE_PATENT_CSE_ID
        self.google_scholar_cse_id = GOOGLE_SCHOLAR_CSE_ID
    
    def extract_keywords(self, idea_text):
        """Extract keywords for patent search"""
        prompt = f"""
        Extract 5-10 key technical keywords from this business idea for patent searching:
        
        Idea: {idea_text}
        
        Return keywords that would be found in patents and technical literature.
        Focus on:
        - Technical terms
        - Product categories
        - Technology areas
        - Application domains
        
        Return as JSON array: ["keyword1", "keyword2", ...]
        """
        
        response = self.ai_helper.generate_response(prompt)
        result = self.ai_helper.extract_json_from_response(response)
        
        if result and isinstance(result, list):
            return result
        else:
            # Fallback keyword extraction
            words = idea_text.split()
            return [word for word in words if len(word) > 4][:5]
    
    def search_patents_custom_search(self, keywords, limit=20):
        """Search patents using Google Custom Search API"""
        if not self.google_api_key or self.google_api_key == "your_google_api_key_here":
            return {"error": "Google API key not configured"}
        
        # Create search query
        query = " ".join(keywords)
        
        # Google Custom Search API endpoint
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            'key': self.google_api_key,
            'cx': self.google_patent_cse_id,
            'q': f"{query} site:patents.google.com",
            'num': min(limit, 10),
            'start': 1
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "data": data.get("items", []),
                    "total": data.get("searchInformation", {}).get("totalResults", 0)
                }
            else:
                return {"error": f"API Error: {response.status_code}"}
        
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def search_literature_google_scholar(self, keywords, limit=20):
        """Search literature using Google Custom Search on Scholar"""
        if not self.google_api_key or self.google_api_key == "your_google_api_key_here":
            return {"error": "Google API key not configured"}
        
        # Create search query
        query = " ".join(keywords)
        
        # Google Custom Search API endpoint
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            'key': self.google_api_key,
            'cx': self.google_scholar_cse_id,
            'q': f"{query} site:scholar.google.com",
            'num': min(limit, 10),
            'start': 1
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "data": data.get("items", []),
                    "total": data.get("searchInformation", {}).get("totalResults", 0)
                }
            else:
                return {"error": f"API Error: {response.status_code}"}
        
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def analyze_market_saturation(self, idea_text, patent_results, literature_results):
        """Analyze market saturation based on search results"""
        patent_count = len(patent_results.get('data', []))
        literature_count = len(literature_results.get('data', []))
        
        # Get sample results for analysis
        sample_patents = patent_results.get('data', [])[:5]
        sample_literature = literature_results.get('data', [])[:5]
        
        prompt = f"""
        Analyze market saturation for this business idea:
        
        Original idea: {idea_text}
        
        Search results:
        - Patents found: {patent_count}
        - Literature papers found: {literature_count}
        
        Sample patents: {json.dumps(sample_patents, indent=2)}
        Sample literature: {json.dumps(sample_literature, indent=2)}
        
        Determine:
        1. Market saturation level (Low/Medium/High)
        2. Key competitors or similar solutions
        3. Differentiation opportunities
        4. Market gaps identified
        
        Return as JSON:
        {{
            "saturation_level": "Medium",
            "competitors": ["Company A", "Company B"],
            "differentiation_opportunities": ["Opportunity 1", "Opportunity 2"],
            "market_gaps": ["Gap 1", "Gap 2"],
            "recommendation": "Proceed with differentiation strategy"
        }}
        """
        
        response = self.ai_helper.generate_response(prompt)
        result = self.ai_helper.extract_json_from_response(response)
        
        if result:
            return result
        else:
            return {
                "saturation_level": "Unknown",
                "competitors": [],
                "differentiation_opportunities": [],
                "market_gaps": [],
                "recommendation": "Unable to analyze market"
            }
    
    def generate_differentiation_strategies(self, idea_text, market_analysis):
        """Generate differentiation strategies based on market analysis"""
        prompt = f"""
        Generate 3-5 differentiation strategies for this business idea based on market analysis:
        
        Original idea: {idea_text}
        Market analysis: {json.dumps(market_analysis, indent=2)}
        
        For each strategy, provide:
        1. Strategy name
        2. Key differentiators
        3. Implementation approach
        4. Pros and cons
        5. Impact on original idea
        6. Market positioning
        
        Return as JSON array:
        [
            {{
                "name": "Strategy Name",
                "key_differentiators": "What makes this approach unique",
                "implementation_approach": "How to implement this strategy",
                "pros": "Benefits of this approach",
                "cons": "Potential drawbacks",
                "impact_on_original_idea": "How this changes the original concept",
                "market_positioning": "Market position this creates"
            }}
        ]
        """
        
        response = self.ai_helper.generate_response(prompt)
        result = self.ai_helper.extract_json_from_response(response)
        
        if result and isinstance(result, list):
            return result
        else:
            return []
    
    def regenerate_idea_with_strategy(self, original_idea, selected_strategy):
        """Regenerate idea based on selected differentiation strategy"""
        
        regeneration_prompt = f"""
        You are an expert business strategist and R&D consultant. Regenerate the business idea by incorporating the selected differentiation strategy while maintaining TRL 4 compliance and R&D focus.

        Original Business Idea:
        {original_idea}

        Selected Differentiation Strategy:
        - Name: {selected_strategy.get('name', 'N/A')}
        - Key Differentiators: {selected_strategy.get('key_differentiators', 'N/A')}
        - Implementation: {selected_strategy.get('implementation_approach', 'N/A')}
        - Market Impact: {selected_strategy.get('impact_on_original_idea', 'N/A')}

        REQUIREMENTS for the enhanced idea:
        1. MAINTAIN TRL 4 LEVEL: Must include laboratory validation, component integration, and proof-of-concept
        2. INTEGRATE DIFFERENTIATION: Seamlessly incorporate the selected strategy's key differentiators
        3. PRESERVE R&D FOCUS: Keep scientific and technological development activities
        4. ADD UNIQUE VALUE: Clearly articulate what makes this solution unique in the market
        5. ENSURE MARKET FIT: Address identified market gaps and competitive advantages

        MANDATORY ELEMENTS to include:
        - Laboratory validation requirements for the differentiated approach
        - Technical integration challenges and solutions
        - Proof-of-concept demonstrations that showcase differentiation
        - Research activities needed to implement the strategy
        - Development milestones that prove competitive advantage

        Generate an enhanced business idea that naturally incorporates the differentiation strategy while maintaining all R&D and TRL 4 requirements. The result should read as a mature, market-aware technology development project.
        """
        
        enhanced_idea = self.ai_helper.generate_response(regeneration_prompt)
        return enhanced_idea
    
    def process_idea(self, business_idea):
        """Process business idea with enhanced strategy selection"""
        try:
            # Extract keywords for search
            keywords = self.extract_keywords(business_idea)
            
            # Perform patent and literature searches
            patent_results = self.search_patents_custom_search(keywords)
            literature_results = self.search_literature_google_scholar(keywords)
            
            # Analyze market saturation
            market_analysis = self.analyze_market_saturation(
                business_idea, patent_results, literature_results
            )
            
            # Generate differentiation strategies
            differentiation_strategies = self.generate_differentiation_strategies(
                business_idea, market_analysis
            )
            
            # Check if strategy selection is needed
            requires_selection = (
                market_analysis.get("saturation_level") in ["Medium", "High"] or
                len(differentiation_strategies) > 1
            )
            
            return {
                "keywords": keywords,
                "patent_results": patent_results,
                "literature_results": literature_results,
                "market_analysis": market_analysis,
                "differentiation_strategies": differentiation_strategies,
                "requires_user_selection": requires_selection,
                "success": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "requires_user_selection": False
            }