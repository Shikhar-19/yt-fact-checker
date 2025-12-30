import subprocess
import json
import re


# -------------------------------
# Calls Ollama model
# -------------------------------
def ask_ollama(prompt: str, model: str = "llama3.1:8b"):
    """
    Calls the Ollama model and returns the raw response text.
    Fully compatible with Windows terminal.
    """

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore"   # Fix Windows cp1252 UnicodeDecode errors
        )

        return result.stdout.strip()

    except Exception as e:
        return f"Error contacting Ollama: {e}"


# -------------------------------
# Extract JSON safely
# -------------------------------
def extract_json(text: str):
    """
    Finds the FIRST valid JSON object in the model response.
    Works even if the model adds text before or after JSON.
    """

    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except:
        return None


# -------------------------------
# Fact-check a claim
# -------------------------------
def verify_claim(claim: str):
    """
    Uses Llama 3.1 8B (via Ollama) to fact-check a claim.
    Always returns a dict with:
      - verdict
      - explanation
      - evidence
    """

    prompt = f"""
You are a factual verification assistant.
Your job is to analyze the claim below and classify it as EXACTLY one of:

- TRUE
- FALSE
- PARTIALLY TRUE
- UNVERIFIABLE

Also provide short reasoning and include at least one real evidence source.

Claim: "{claim}"

Respond ONLY in valid JSON with this format:

{{
  "verdict": "",
  "explanation": "",
  "evidence": [
    {{
      "source": "",
      "description": ""
    }}
  ]
}}
"""

    raw = ask_ollama(prompt)

    # Try to extract clean JSON
    data = extract_json(raw)

    if data:
        return data

    # Fallback if model did not return valid JSON
    return {
        "verdict": "UNVERIFIABLE",
        "explanation": raw,
        "evidence": []
    }


# Quick test
if __name__ == "__main__":
    claim = "The moon landing was faked."
    print("Checking:", claim)
    print(json.dumps(verify_claim(claim), indent=4))
