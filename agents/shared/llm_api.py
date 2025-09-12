"""
Author: Faisal Chaudhry

LLM API Wrapper:
- Provides a interface to OpenAI ChatCompletion
- Includes retry logic with exponential backoff for rate limits
- Accepts messages and optional model/temperature arguments
- Returns structured content from first choice
"""

import os
import time
import openai
from openai.error import RateLimitError

# load API key once
openai.api_key = os.getenv("OPENAI_API_KEY", "").strip()


def call_llm(messages, model=None, temperature=0.0, max_retries=3):
    """
    Wrapper for ChatCompletion.create with exponential backoff on rate limits.
    messages: list of dict(role, content)
    model: override model name (else env-var OPENAI_MODEL)
    """
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo").strip()
    for attempt in range(max_retries):
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return resp.choices[0].message.content
        except RateLimitError:
            time.sleep(2 ** attempt)
    raise RuntimeError("LLM rate-limit or network failures after retries")
