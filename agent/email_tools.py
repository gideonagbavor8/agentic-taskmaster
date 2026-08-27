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


def approve_email(to: str, subject: str, body: str, approval: str = "") -> dict:
    """Send an approved email. Sending is simulated until an email provider is connected."""
    if approval.strip().lower() not in {"yes", "approved", "send"}:
        return {
            "success": False,
            "status": "rejected",
            "error": "Email cannot be sent without explicit user approval.",
        }

    return {
        "success": True,
        "status": "sent",
        "email": {
            "to": to,
            "subject": subject,
            "body": body,
        },
        "message": "Email sent successfully.",
    }