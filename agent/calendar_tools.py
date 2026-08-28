from datetime import datetime, timedelta

from googleapiclient.discovery import build

from .gmail_auth import get_gmail_service


def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
) -> dict:
    """Create a Google Calendar event."""

    try:
        gmail_service = get_gmail_service()

        credentials = gmail_service._http.credentials

        calendar_service = build(
            "calendar",
            "v3",
            credentials=credentials,
        )

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "Africa/Accra",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Africa/Accra",
            },
        }

        created_event = (
            calendar_service.events()
            .insert(
                calendarId="primary",
                body=event,
            )
            .execute()
        )

        return {
            "success": True,
            "status": "created",
            "event": {
                "id": created_event.get("id"),
                "summary": created_event.get("summary"),
                "start": created_event.get("start"),
                "end": created_event.get("end"),
                "link": created_event.get("htmlLink"),
            },
            "message": "Calendar event created successfully.",
        }

    except Exception as e:
        return {
            "success": False,
            "status": "failed",
            "error": str(e),
        }