"""ClickSend service controller for sending emails and SMS."""
import httpx
import base64
from typing import Dict, Any, Optional
from app.config import (
    CLICKSEND_API_KEY, CLICKSEND_API_USERNAME, CLICKSEND_EMAIL, 
    CLICKSEND_EMAIL_ADDRESS_ID, CLICKSEND_API_URL
)


class ClickSendController:
    """Controller for ClickSend API operations."""

    @staticmethod
    async def get_verified_email_id(email: str) -> Optional[int]:
        """
        Get the email_address_id for a verified email address.
        
        Args:
            email: Email address to look up
            
        Returns:
            Email address ID if found, None otherwise
        """
        url = f"{CLICKSEND_API_URL}/email/addresses"
        username = CLICKSEND_API_USERNAME or CLICKSEND_EMAIL or CLICKSEND_API_KEY
        password = CLICKSEND_API_KEY
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    auth=(username, password),
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # ClickSend API structure might vary - try different paths
                email_list = []
                if "data" in data:
                    # Check if data is a dict with nested data array
                    if isinstance(data["data"], dict) and "data" in data["data"]:
                        email_list = data["data"]["data"]
                    # Check if data is directly an array
                    elif isinstance(data["data"], list):
                        email_list = data["data"]
                
                # Find the email address ID matching our email
                for email_addr in email_list:
                    email_value = email_addr.get("email") or email_addr.get("email_address")
                    if email_value and email_value.lower() == email.lower():
                        email_id = email_addr.get("email_address_id") or email_addr.get("id")
                        # Return the ID even if verified status is 0 (might still work)
                        if email_id:
                            return email_id
                
                return None
            except Exception as e:
                # Return None on error - will be handled by caller
                return None

    @staticmethod
    async def send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Send an email via ClickSend API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            
        Returns:
            Dictionary with response data
        """
        url = f"{CLICKSEND_API_URL}/email/send"
        
        # Get the email_address_id - first try from config, then from API
        email_address_id = None
        if CLICKSEND_EMAIL_ADDRESS_ID:
            try:
                email_address_id = int(CLICKSEND_EMAIL_ADDRESS_ID)
            except:
                pass
        
        # If not in config, fetch from API
        if not email_address_id:
            email_address_id = await ClickSendController.get_verified_email_id(CLICKSEND_EMAIL)
        
        # ClickSend email API expects a flat structure with email_address_id for verified emails
        if not email_address_id:
            return {
                "success": False,
                "status_code": 400,
                "data": {
                    "message": f"Email {CLICKSEND_EMAIL} not found. Please verify it in ClickSend dashboard first."
                },
                "error": "Email address ID not found"
            }
        
        payload = {
            "from": {
                "email_address_id": email_address_id,
                "name": "ClickSend Tester"
            },
            "to": [{"email": to}],
            "subject": subject,
            "body": body
        }
        
        # ClickSend uses Basic Auth: username:api_key
        # Common patterns:
        # 1. API username from dashboard:api_key
        # 2. email:api_key (if no username provided)
        # 3. api_key:api_key (fallback)
        username = CLICKSEND_API_USERNAME or CLICKSEND_EMAIL or CLICKSEND_API_KEY
        password = CLICKSEND_API_KEY
        
        headers = {
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, 
                    json=payload, 
                    headers=headers, 
                    auth=(username, password),
                    timeout=30.0
                )
                response.raise_for_status()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json()
                }
            except httpx.HTTPStatusError as e:
                error_data = None
                try:
                    error_data = e.response.json()
                except:
                    error_data = {"message": e.response.text}
                
                # Log authentication details for debugging (without exposing sensitive data)
                if e.response.status_code == 401:
                    error_data["debug"] = "Authentication failed. Check if CLICKSEND_API_USERNAME is set correctly."
                    error_data["auth_used"] = f"Username: {username[:3]}... (length: {len(username)})"
                    
                return {
                    "success": False,
                    "status_code": e.response.status_code,
                    "data": error_data,
                    "error": str(e)
                }
            except Exception as e:
                return {
                    "success": False,
                    "status_code": None,
                    "data": None,
                    "error": str(e)
                }

    @staticmethod
    async def send_sms(to: str, message: str) -> Dict[str, Any]:
        """
        Send an SMS via ClickSend API.
        
        Args:
            to: Recipient phone number (E.164 format)
            message: SMS message content
            
        Returns:
            Dictionary with response data
        """
        url = f"{CLICKSEND_API_URL}/sms/send"
        
        payload = {
            "messages": [
                {
                    "source": "php",
                    "body": message,
                    "to": to
                }
            ]
        }
        
        # ClickSend uses Basic Auth: username:api_key
        # Common patterns:
        # 1. API username from dashboard:api_key
        # 2. email:api_key (if no username provided)
        # 3. api_key:api_key (fallback)
        username = CLICKSEND_API_USERNAME or CLICKSEND_EMAIL or CLICKSEND_API_KEY
        password = CLICKSEND_API_KEY
        
        headers = {
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, 
                    json=payload, 
                    headers=headers, 
                    auth=(username, password),
                    timeout=30.0
                )
                response.raise_for_status()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json()
                }
            except httpx.HTTPStatusError as e:
                error_data = None
                try:
                    error_data = e.response.json()
                except:
                    error_data = {"message": e.response.text}
                
                # Log authentication details for debugging (without exposing sensitive data)
                if e.response.status_code == 401:
                    error_data["debug"] = "Authentication failed. Check if CLICKSEND_API_USERNAME is set correctly."
                    error_data["auth_used"] = f"Username: {username[:3]}... (length: {len(username)})"
                    
                return {
                    "success": False,
                    "status_code": e.response.status_code,
                    "data": error_data,
                    "error": str(e)
                }
            except Exception as e:
                return {
                    "success": False,
                    "status_code": None,
                    "data": None,
                    "error": str(e)
                }

