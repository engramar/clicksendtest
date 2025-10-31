"""API routes for ClickSend testing."""
from fastapi import APIRouter, HTTPException
from app.models.schemas import EmailRequest, SMSRequest, NotificationResponse
from app.controllers.clicksend_controller import ClickSendController
from app.config import CLICKSEND_EMAIL
import httpx

router = APIRouter()


@router.post("/email/send", response_model=NotificationResponse, tags=["email"])
async def send_email(request: EmailRequest) -> NotificationResponse:
    """
    Send an email notification via ClickSend.
    
    Args:
        request: Email request with to, subject, and body
        
    Returns:
        NotificationResponse with success status and message
    """
    try:
        result = await ClickSendController.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body
        )
        
        if result["success"]:
            return NotificationResponse(
                success=True,
                message="Email sent successfully!",
                data=result.get("data")
            )
        else:
            error_msg = result.get("error", "Unknown error")
            if result.get("data"):
                error_msg = str(result.get("data"))
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=error_msg
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@router.post("/sms/send", response_model=NotificationResponse, tags=["sms"])
async def send_sms(request: SMSRequest) -> NotificationResponse:
    """
    Send an SMS notification via ClickSend.
    
    Args:
        request: SMS request with to and message
        
    Returns:
        NotificationResponse with success status and message
    """
    try:
        result = await ClickSendController.send_sms(
            to=request.to,
            message=request.message
        )
        
        if result["success"]:
            return NotificationResponse(
                success=True,
                message="SMS sent successfully!",
                data=result.get("data")
            )
        else:
            error_msg = result.get("error", "Unknown error")
            if result.get("data"):
                error_msg = str(result.get("data"))
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=error_msg
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")


@router.post("/email/addresses", tags=["email", "verify"])
async def add_email_address(email: str = None):
    """
    Add an email address to ClickSend for verification.
    If email is not provided as query param, uses CLICKSEND_EMAIL from config.
    
    Example: POST /api/email/addresses?email=your@email.com
    Or: POST /api/email/addresses (uses CLICKSEND_EMAIL from .env)
    """
    from app.config import CLICKSEND_API_USERNAME, CLICKSEND_API_KEY, CLICKSEND_API_URL, CLICKSEND_EMAIL
    
    # Allow email as query param or use from config
    if not email:
        email = CLICKSEND_EMAIL
    
    if not email:
        raise HTTPException(status_code=400, detail="Email address is required. Provide ?email=your@email.com or set CLICKSEND_EMAIL in .env")
    
    url = f"{CLICKSEND_API_URL}/email/addresses"
    username = CLICKSEND_API_USERNAME or CLICKSEND_EMAIL or CLICKSEND_API_KEY
    password = CLICKSEND_API_KEY
    
    payload = {
        "email_address": email
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                json=payload,
                auth=(username, password),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_data = None
            try:
                error_data = e.response.json()
            except:
                error_data = {"message": e.response.text}
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_data
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to add email address: {str(e)}")


@router.put("/email/address-verify/{email_address_id}/send", tags=["email", "verify"])
async def send_verification_token(email_address_id: int):
    """
    Send a verification token to the email address.
    Check your email inbox for the verification token.
    """
    from app.config import CLICKSEND_API_USERNAME, CLICKSEND_API_KEY, CLICKSEND_API_URL, CLICKSEND_EMAIL
    
    url = f"{CLICKSEND_API_URL}/email/address-verify/{email_address_id}/send"
    username = CLICKSEND_API_USERNAME or CLICKSEND_EMAIL or CLICKSEND_API_KEY
    password = CLICKSEND_API_KEY
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                url,
                auth=(username, password),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_data = None
            try:
                error_data = e.response.json()
            except:
                error_data = {"message": e.response.text}
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_data
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send verification token: {str(e)}")


@router.put("/email/address-verify/{email_address_id}/verify/{activation_token}", tags=["email", "verify"])
async def verify_email_address(email_address_id: int, activation_token: str):
    """
    Verify the email address using the activation token received via email.
    """
    from app.config import CLICKSEND_API_USERNAME, CLICKSEND_API_KEY, CLICKSEND_API_URL, CLICKSEND_EMAIL
    
    url = f"{CLICKSEND_API_URL}/email/address-verify/{email_address_id}/verify/{activation_token}"
    username = CLICKSEND_API_USERNAME or CLICKSEND_EMAIL or CLICKSEND_API_KEY
    password = CLICKSEND_API_KEY
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                url,
                auth=(username, password),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_data = None
            try:
                error_data = e.response.json()
            except:
                error_data = {"message": e.response.text}
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_data
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to verify email address: {str(e)}")


@router.get("/email/addresses", tags=["email", "debug"])
async def get_email_addresses():
    """
    Debug endpoint to list all verified email addresses and their IDs.
    Useful for finding the email_address_id to add to .env file.
    """
    from app.config import CLICKSEND_API_USERNAME, CLICKSEND_API_KEY, CLICKSEND_API_URL
    
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
            return response.json()
        except httpx.HTTPStatusError as e:
            error_data = None
            try:
                error_data = e.response.json()
            except:
                error_data = {"message": e.response.text}
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_data
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch email addresses: {str(e)}")

