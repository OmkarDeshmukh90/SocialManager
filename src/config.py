import os
from dotenv import load_dotenv

load_dotenv()

MASTODON_CLIENT_ID = os.getenv("MASTODON_CLIENT_ID")
MASTODON_CLIENT_SECRET = os.getenv("MASTODON_CLIENT_SECRET")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
MASTODON_API_BASE_URL = os.getenv("MASTODON_API_BASE_URL")

# Optional: add a quick check
if not all([MASTODON_CLIENT_ID, MASTODON_CLIENT_SECRET, MASTODON_ACCESS_TOKEN, MASTODON_API_BASE_URL]):
    raise ValueError("One or more Mastodon credentials are missing. Check your .env file.")
