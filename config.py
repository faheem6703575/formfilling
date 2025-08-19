import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SCHOLAR_CSE_ID = os.getenv("GOOGLE_SCHOLAR_CSE_ID")
GOOGLE_PATENT_CSE_ID = os.getenv("GOOGLE_PATENT_CSE_ID")

# SME Criteria
SME_CRITERIA = {
    "max_employees": 250,
    "max_turnover": 50_000_000,  # EUR
    "max_balance_sheet": 43_000_000  # EUR
}

# Frascati Scoring Threshold
FRASCATI_THRESHOLD = 40  # Minimum score required

# TRL Definitions
TRL_DEFINITIONS = {
    1: "Basic principles observed",
    2: "Technology concept formulated", 
    3: "Experimental proof of concept",
    4: "Technology validated in lab",
    5: "Technology validated in relevant environment",
    6: "Technology demonstrated in relevant environment",
    7: "System prototype demonstration",
    8: "System complete and qualified",
    9: "System proven in operational environment"
}