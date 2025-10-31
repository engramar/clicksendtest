# ClickSend Notification Tester

A simple FastAPI application to test email and SMS notifications via ClickSend API.

## Features

- **Email Notification Tester**: Send test emails via ClickSend API
- **SMS Notification Tester**: Send test SMS messages via ClickSend API
- **Modern UI**: Clean, mobile-first design with Vibecamp branding
- **Real-time Feedback**: Immediate success/error notifications

## Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
Create a `.env` file in the root directory with your ClickSend credentials:
```
CLICKSEND_API_KEY=your_api_key_here
CLICKSEND_API_USERNAME=your_username_here
CLICKSEND_EMAIL=your_email@example.com
CLICKSEND_PHONE=+1234567890
CLICKSEND_API_URL=https://rest.clicksend.com/v3
CLICKSEND_EMAIL_ADDRESS_ID=optional_email_address_id
```

3. **Run the Application**
```bash
uvicorn main:app --reload
```

4. **Access the Application**
Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

### Send Email
1. Fill in the recipient email address
2. Enter email subject
3. Enter email body/message
4. Click "Send Email"

### Send SMS
1. Fill in the recipient phone number
   - Must be in E.164 format: `+[country code][number]`
2. Enter SMS message (max 160 characters)
3. Click "Send SMS"

## API Endpoints

### POST `/api/email/send`
Send an email notification.

**Request Body:**
```json
{
  "to": "recipient@example.com",
  "subject": "Test Subject",
  "body": "Test message body"
}
```

### POST `/api/sms/send`
Send an SMS notification.

**Request Body:**
```json
{
  "to": "+1234567890",
  "message": "Test SMS message"
}
```

## Project Structure

```
clicksendtest/
├── app/
│   ├── controllers/      # Business logic (ClickSend API calls)
│   ├── models/            # Pydantic models
│   ├── routes/            # API and web routes
│   └── templates/         # Jinja2 HTML templates
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (not in git)
```

## Notes

- Make sure your ClickSend account has sufficient credits
- The sender email must be verified in your ClickSend account
- Phone numbers must be in international E.164 format (e.g., `+1234567890`)
- SMS messages are limited to 160 characters

