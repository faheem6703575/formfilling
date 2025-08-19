from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

class AIHelper:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate_response(self, prompt, max_tokens=32000):
        """Generate AI response using Groq"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def extract_json_from_response(self, response_text):
        """Extract JSON data from AI response"""
        try:
            import json
            # Find JSON content between ```json and ```
            start = response_text.find('```json')
            if start != -1:
                start += 7
                end = response_text.find('```', start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            
            # Try to parse entire response as JSON
            return json.loads(response_text)
        except:
            return None