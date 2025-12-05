import uuid

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from .user import User


def get_expiration_datetime():
    return timezone.now() + timezone.timedelta(days=settings.USER_INVITE_EXPIRATION_DAYS)


class UserInvitation(models.Model):
    # Must be a UUID for security reasons. UUID can not be guessed.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(max_length=255, unique=True)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_datetime)

    def send_invitation_email(self):
        message = f"""
{'=' * 70}
                    INVITATION EMAIL SENT
{'=' * 70}

To: {self.email}
From: {self.invited_by.full_name} ({self.invited_by.email})
Invitation ID: {self.id}
Expires At: {self.expires_at.strftime('%Y-%m-%d %H:%M:%S UTC')}

Subject: You have been invited to join our platform

Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hello,

You have been invited to join our platform by {self.invited_by.full_name}.

To accept this invitation, please click on the link below:
{settings.SENDING_DOMAIN}/invite/{self.id}

This invitation will expire on {self.expires_at.strftime('%B %d, %Y at %I:%M %p UTC')}.

Kind regards,
The Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{'=' * 70}
"""
        send_mail(
            subject="You have been invited to join our platform",
            message=message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings, or 'webmaster@localhost' by default
            recipient_list=[self.email],
        )