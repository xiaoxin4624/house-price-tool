from __future__ import annotations

from datetime import datetime, timezone

from .config import load_config
from .emailer import send_email
from .fetchers import collect_sources
from .render import render_digest
from .topics import TOPICS


def main() -> None:
    config = load_config()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    items, errors = collect_sources(TOPICS, config.request_timeout_seconds)
    digest = render_digest(TOPICS, items, errors, config.lookback_hours)

    date_slug = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_file = config.output_dir / f"digest-{date_slug}.md"
    output_file.write_text(digest, encoding="utf-8")
    print(f"Wrote {output_file}")

    subject = f"{config.email.subject_prefix} {date_slug}"
    if send_email(config.email, subject, digest):
        print("Email sent")
    else:
        print("Email skipped: SMTP settings are incomplete")


if __name__ == "__main__":
    main()
