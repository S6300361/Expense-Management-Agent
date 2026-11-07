import json
from datetime import date

from google import genai

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from agent.validator import Expense, validate_expense


SYSTEM_PROMPT = """
You extract expense records from user text.

Return one JSON object matching this schema:
amount (number), currency (3-letter code), category (string),
payment_method (string), description (string), date (YYYY-MM-DD),
vendor (string or null), notes (string or null).

Rules:
1. Never invent an expense amount or currency.
2. Use today's date only when the user clearly says today.
3. If a date is relative, resolve it using the supplied current date.
4. If amount or currency is missing, do not invent it.
5. Use null for optional vendor and notes when not provided.
6. Return valid JSON only.
"""


def parse_expense(user_text: str) -> Expense:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
{SYSTEM_PROMPT}

Current date: {date.today().isoformat()}

User input:
{user_text}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json"
        }
    )

    content = response.text

    if not content:
        raise ValueError("Gemini returned an empty response.")

    try:
        extracted_data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini did not return valid JSON: {content}"
        ) from exc

    if not extracted_data.get("amount") or not extracted_data.get("currency"):
        raise ValueError(
            "The expense amount or currency is missing. "
            "Please provide both before saving."
        )

    return validate_expense(extracted_data)