"""Email ticket buyers their confirmation."""
import resend
from django.conf import settings
from django.utils.dateformat import format as date_format
from django.utils.timezone import localtime


def send_ticket_email(ticket):
    """Email one buyer confirming their tickets."""
    resend.api_key = settings.RESEND_API_KEY
    event = ticket.event
    when = f" on {date_format(localtime(event.start_time), 'j F Y, g:i A')}" if event.start_time else ""
    return resend.Emails.send({
        "from": "noreply@srdg.co.nz",
        "to": ticket.email,
        "subject": f"Your tickets for {event.title}",
        "html": f"""
            <h2>Thank you for purchasing {"tickets" if ticket.quantity > 1 else "a ticket"}.</h2>
            <p><strong>{ticket.quantity} × {event.title}</strong>{when}{f" at {event.location}" if event.location else ""}.</p>
            <p>Show this email at the door, under the name <strong>{ticket.name}</strong>.</p>
            <p>Enjoy the event!</p>
        """,
    })
