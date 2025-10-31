"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

load_dotenv()

CLICKSEND_API_KEY = os.getenv("CLICKSEND_API_KEY", "")
CLICKSEND_API_USERNAME = os.getenv("CLICKSEND_API_USERNAME", "")  # Username from ClickSend dashboard
CLICKSEND_EMAIL = os.getenv("CLICKSEND_EMAIL", "")
CLICKSEND_EMAIL_ADDRESS_ID = os.getenv("CLICKSEND_EMAIL_ADDRESS_ID", "")  # Optional: email_address_id if known
CLICKSEND_PHONE = os.getenv("CLICKSEND_PHONE", "")
CLICKSEND_API_URL = os.getenv("CLICKSEND_API_URL", "https://rest.clicksend.com/v3")

