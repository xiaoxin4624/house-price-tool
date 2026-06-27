from __future__ import annotations

import smtplib
from email.message import EmailMessage

from .config import EmailConfig


def send_email(config: EmailConfig, subject: str, body: str) -> bool:
    if not config.enabled:
        return False
    message = EmailMessage()
    message["From"] = config.email_from
    message["To"] = ", ".join(config.email_to)
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as smtp:
        if config.smtp_use_tls:
            smtp.starttls()
        if config.smtp_username:
            smtp.login(config.smtp_username, config.smtp_password)
        smtp.send_message(message)
    return True
