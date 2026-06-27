from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        env_file = Path(".env")
        if not env_file.exists():
            return
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class EmailConfig:
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_use_tls: bool
    email_from: str
    email_to: list[str]
    subject_prefix: str

    @property
    def enabled(self) -> bool:
        return bool(self.smtp_host and self.email_from and self.email_to)


@dataclass(frozen=True)
class AppConfig:
    output_dir: Path
    lookback_hours: int
    request_timeout_seconds: int
    email: EmailConfig


def _bool(value: str, default: bool = True) -> bool:
    if value == "":
        return default
    return value.lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> AppConfig:
    load_dotenv()
    recipients = [item.strip() for item in os.getenv("EMAIL_TO", "").split(",") if item.strip()]
    return AppConfig(
        output_dir=Path(os.getenv("DIGEST_OUTPUT_DIR", "output")),
        lookback_hours=int(os.getenv("DIGEST_LOOKBACK_HOURS", "48")),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "15")),
        email=EmailConfig(
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            smtp_use_tls=_bool(os.getenv("SMTP_USE_TLS", "true")),
            email_from=os.getenv("EMAIL_FROM", ""),
            email_to=recipients,
            subject_prefix=os.getenv("EMAIL_SUBJECT_PREFIX", "每日中文主题摘要"),
        ),
    )
