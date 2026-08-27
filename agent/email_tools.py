from email.mime.text import MIMEText
import base64

from .gmail_auth import get_gmail_service


def prepare_email(to: str, subject: str, body: str) -> dict:
    """Prepare an email for user approval before sending."""
    return {
        "success": True,
        "status": "awaiting_approval",
        "email": {
            "to": to,
            "subject": subject,
            "body": body,
        },
        "message": "Email prepared. Explicit user approval is required before sending.",
    }


def approve_email(
    to: str,
    subject: str,
    body: str,
    approval: str = "",
) -> dict:
    """Send an email through Gmail only after explicit user approval."""

    if approval.strip().lower() not in {"yes", "approved", "send"}:
        return {
            "success": False,
            "status": "rejected",
            "error": "Email cannot be sent without explicit user approval.",
        }

    try:
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        service = get_gmail_service()

        sent_message = (
            service.users()
            .messages()
            .send(
                userId="me",
                body={"raw": encoded_message},
            )
            .execute()
        )

        return {
            "success": True,
            "status": "sent",
            "email": {
                "to": to,
                "subject": subject,
                "body": body,
            },
            "message_id": sent_message.get("id"),
            "message": "Email sent successfully through Gmail.",
        }

    except Exception as e:
        return {
            "success": False,
            "status": "failed",
            "error": str(e),
        }