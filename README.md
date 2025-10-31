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
The `.env` file is already configured with your ClickSend credentials:
- API Key: `BA405B6A-4D4C-DF61-BE11-FF310F62C258`
- Email: `engramar@code.sydney`
- Phone: `+61430410829`

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
1. Fill in the recipient email (default: `engramar@code.sydney`)
2. Enter email subject
3. Enter email body/message
4. Click "Send Email"

### Send SMS
1. Fill in the recipient phone number (default: `+61430410829`)
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
  "to": "+61430410829",
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
- The sender email (`engramar@code.sydney`) must be verified in your ClickSend account
- Phone numbers must be in international E.164 format (e.g., `+61430410829`)
- SMS messages are limited to 160 characters

