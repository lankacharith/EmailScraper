from urllib.parse import urlparse
import os
import requests

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def validate_email(email, base_url):
    """Ensure emails are relevant to the domain."""
    domain = urlparse(base_url).netloc
    return domain in email or email.endswith(('.com', '.org', '.net'))

def validate_email_with_hunter(email):
    """Validate email using Hunter.io API."""
    if not HUNTER_API_KEY:
        print("Hunter API key is missing.")
        return False

    try:
        response = requests.get(
            "https://api.hunter.io/v2/email-verifier",
            params={"email": email, "api_key": HUNTER_API_KEY},
        )
        data = response.json()
        return data.get("data", {}).get("result") == "deliverable"
    except Exception as e:
        print(f"Error validating email {email}: {e}")
        return False