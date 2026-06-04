"""Configuration for Straight Dope."""

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# All roles use the same model — Claude Sonnet 4.5 via OpenRouter
ADVISOR_MODEL = "anthropic/claude-sonnet-4-5"
CHAIRMAN_MODEL = "anthropic/claude-sonnet-4-5"

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

DATA_DIR = "data/conversations"
