"""
LLM Verifier: Sends code slices to Google Gemini Pro for semantic race verification.
Uses the google-genai SDK (v1+) with the Client-based API.
"""
import json
import time
from typing import Optional
from models import RaceVerificationRequest, RaceVerificationResponse, Verdict
import config


def create_client():
    """Create and configure the Gemini client (google-genai v1+ SDK)."""
    from google import genai

    if not config.GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Get your key from https://aistudio.google.com/apikey"
        )

    client = genai.Client(api_key=config.GOOGLE_API_KEY)
    return client


def verify_race(client, request: RaceVerificationRequest,
                generation_config: dict = None) -> Optional[RaceVerificationResponse]:
    """
    Send a single race candidate to Gemini for verification.
    Returns a structured RaceVerificationResponse or None on failure.
    Uses google-genai v1+ Client API.
    """
    from google.genai import types

    if generation_config is None:
        generation_config = config.GENERATION_CONFIG

    prompt = config.VERIFICATION_PROMPT_TEMPLATE.format(
        race_type=request.race_type,
        entity_name=request.entity,
        endpoint1_name=request.endpoint1_name,
        endpoint1_http=request.endpoint1_http,
        endpoint1_code=request.endpoint1_code,
        endpoint2_name=request.endpoint2_name,
        endpoint2_http=request.endpoint2_http,
        endpoint2_code=request.endpoint2_code,
        protection_status=request.protection_status
    )

    generate_config = types.GenerateContentConfig(
        system_instruction=config.SYSTEM_PROMPT,
        temperature=generation_config.get("temperature", 0.3),
        top_p=generation_config.get("top_p", 0.95),
        max_output_tokens=generation_config.get("max_output_tokens", 2048),
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config=generate_config,
            )

            # Parse the response text as JSON
            response_text = response.text.strip()
            
            # Clean up markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                # Remove first and last lines (```json and ```)
                lines = [l for l in lines if not l.strip().startswith("```")]
                response_text = '\n'.join(lines)

            parsed = json.loads(response_text)

            return RaceVerificationResponse(
                verdict=Verdict(parsed.get("verdict", "TRUE_POSITIVE")),
                confidence=float(parsed.get("confidence", 0.5)),
                reasoning=parsed.get("reasoning", ""),
                race_pattern=parsed.get("race_pattern"),
                mitigation_suggestion=parsed.get("mitigation_suggestion")
            )

        except json.JSONDecodeError:
            # Try to extract JSON from the response
            response_text = response.text if hasattr(response, 'text') else ""
            json_match = _extract_json(response_text)
            if json_match:
                try:
                    parsed = json.loads(json_match)
                    return RaceVerificationResponse(
                        verdict=Verdict(parsed.get("verdict", "TRUE_POSITIVE")),
                        confidence=float(parsed.get("confidence", 0.5)),
                        reasoning=parsed.get("reasoning", ""),
                        race_pattern=parsed.get("race_pattern"),
                        mitigation_suggestion=parsed.get("mitigation_suggestion")
                    )
                except (json.JSONDecodeError, ValueError):
                    pass

        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                # Rate limited — exponential backoff
                wait_time = (2 ** attempt) * 2
                print(f"  Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            elif attempt < max_retries - 1:
                time.sleep(1)
            else:
                print(f"  ⚠ LLM verification failed after {max_retries} attempts: {e}")
                return None

    return None


def _extract_json(text: str) -> Optional[str]:
    """Try to extract a JSON object from mixed text."""
    # Find the first { and last }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return None
