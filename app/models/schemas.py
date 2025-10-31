"""Pydantic models for validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class EmailRequest(BaseModel):
    """Request model for sending email."""
    to: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject", min_length=1)
    body: str = Field(..., description="Email body content", min_length=1)


class SMSRequest(BaseModel):
    """Request model for sending SMS."""
    to: str = Field(..., description="Recipient phone number (E.164 format)", pattern=r"^\+\d{10,15}$")
    message: str = Field(..., description="SMS message content", min_length=1, max_length=160)


class NotificationResponse(BaseModel):
    """Response model for notification sending."""
    success: bool
    message: str
    data: Optional[dict] = None

