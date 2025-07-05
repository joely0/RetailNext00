"""
config.py
Contains basic OpenAI configs
"""

import os

GPT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_COST_PER_1K_TOKENS = 0.00013

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ Warning: OPENAI_API_KEY environment variable not set")
    print("Please set your OpenAI API key as an environment variable")
    print("You can set it in Streamlit Cloud deployment settings")