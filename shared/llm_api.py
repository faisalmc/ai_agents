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
import socket

# load API key once
openai.api_key = os.getenv("OPENAI_API_KEY", "").strip()


def call_llm(messages, model=None, temperature=0.0, max_retries=3):
    """
    Wrapper for ChatCompletion.create with exponential backoff on rate limits.
    messages: list of dict(role, content)
    model: override model name (else env-var OPENAI_MODEL)
    GPT-4o Mini vs "gpt-3.5-turbo"
    """
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    print(f"[DEBUG:call_llm] Model={model}, Temp={temperature}, Retries={max_retries}", flush=True)
    print(f"[DEBUG:call_llm] Messages count={len(messages)}", flush=True)

    for attempt in range(max_retries + 1):
        try:
            print(f"\n[DEBUG:call_llm] ---- within for loop ---- before openai.ChatCompletion.create ---\n")
            print(f"[DEBUG:call_llm] Attempt {attempt}/{max_retries} → calling OpenAI...", flush=True)
            resp = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                timeout=15  # seconds — prevents indefinite blocking
            )
            print("[DEBUG:call_llm] Received response from OpenAI.", flush=True)
            print(f"[DEBUG:call_llm] Raw type={type(resp)}", flush=True)
            print(f"[DEBUG:call_llm] Response keys={getattr(resp, 'keys', lambda: [])()}", flush=True)
            return resp.choices[0].message.content
        except RateLimitError:
            print(f"[WARN:call_llm] Rate limit. Sleeping {2**attempt}s...", flush=True)
            time.sleep(2 ** attempt)
            last_error = e
        except Exception as e:
            print(f"[ERROR:call_llm] Exception type={type(e).__name__}, msg={e}", flush=True)
            last_error = e
            continue
        except (socket.timeout, openai.error.Timeout, openai.error.APIConnectionError) as e:
            print(f"[ERROR:call_llm] Timeout/APIConnectionError: {e}", flush=True)
            continue
    raise RuntimeError(f"LLM call failed after {max_retries} attempts. Last error: {last_error}")
