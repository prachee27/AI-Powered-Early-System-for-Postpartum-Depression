"""Send minimal, consented critical-risk doctor alerts over SMTP."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
import logging
import os
import smtplib
import ssl

import certifi


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AlertResult:
    sent: bool
    message: str


class DoctorAlertService:
    """SMTP service configured only with environment variables, never the UI."""

    def __init__(self) -> None:
        self.host = os.getenv("SMTP_HOST", "").strip()
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME", "").strip()
        self.password = os.getenv("SMTP_PASSWORD", "")
        self.sender = os.getenv("SMTP_FROM_EMAIL", self.username).strip()

    @property
    def configured(self) -> bool:
        return bool(self.host and self.username and self.password and self.sender)

    def send_critical_alert(self, *, doctor_email: str, patient_id: str, risk_level: str) -> AlertResult:
        if not self.configured:
            return AlertResult(False, "Critical alert not sent: SMTP is not configured.")

        message = EmailMessage()
        message["Subject"] = "PPD-EWS critical screening alert — follow up required"
        message["From"] = self.sender
        message["To"] = doctor_email
        message.set_content(
            "A PPD-EWS screening assessment returned a CRITICAL risk result.\n\n"
            f"Patient reference: {patient_id}\n"
            f"Risk level: {risk_level}\n"
            f"Assessment time (UTC): {datetime.utcnow().isoformat(timespec='seconds')}Z\n\n"
            "Please follow your clinical escalation process. This is an automated screening alert, not a diagnosis.\n"
            "The journal text is intentionally not included in this email."
        )
        try:
            with smtplib.SMTP(self.host, self.port, timeout=15) as client:
                # Use certifi's current root-certificate bundle rather than relying
                # on a system Python certificate store. This is especially helpful
                # for locally-installed Python versions on macOS and Windows.
                tls_context = ssl.create_default_context(cafile=certifi.where())
                client.starttls(context=tls_context)
                client.login(self.username, self.password)
                client.send_message(message)
            return AlertResult(True, f"Critical alert sent to {doctor_email}.")
        except (OSError, smtplib.SMTPException) as exc:
            logger.exception("Could not send critical doctor alert")
            if "CERTIFICATE_VERIFY_FAILED" in str(exc):
                return AlertResult(
                    False,
                    "Critical alert could not be sent because the local trusted certificate store needs updating. "
                    "Restart the server after installing the project requirements.",
                )
            return AlertResult(False, f"Critical alert could not be sent: {exc}")
