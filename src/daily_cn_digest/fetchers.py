from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from re import sub
from typing import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree

USER_AGENT = "daily-cn-digest/0.1 (+https://example.local)"


@dataclass(frozen=True)
class SourceItem:
    topic: str
    title: str
    url: str
    published: datetime | None
    summary: str


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _clean_html(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(unescape(sub(r"<[^>]+>", " ", text)).split())


def _child_text(node: ElementTree.Element, names: tuple[str, ...]) -> str:
    for name in names:
        child = node.find(name)
        if child is not None and child.text:
            return child.text.strip()
        child = node.find(f".//{{*}}{name}")
        if child is not None and child.text:
            return child.text.strip()
    return ""


def _entry_link(node: ElementTree.Element) -> str:
    direct = _child_text(node, ("link",))
    if direct:
        return direct
    for child in node.findall(".//{*}link"):
        href = child.attrib.get("href")
        if href:
            return href
    return ""


def fetch_feed(topic: str, feed_url: str, timeout: int) -> list[SourceItem]:
    request = Request(feed_url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        data = response.read()
    root = ElementTree.fromstring(data)
    nodes = root.findall(".//item") or root.findall(".//{*}entry")
    items: list[SourceItem] = []
    for entry in nodes[:10]:
        title = _clean_html(_child_text(entry, ("title",)))
        url = _entry_link(entry) or feed_url
        published = _parse_dt(_child_text(entry, ("published", "updated", "pubDate")))
        summary = _clean_html(_child_text(entry, ("summary", "description", "content")))
        if title and url:
            items.append(SourceItem(topic=topic, title=title, url=url, published=published, summary=summary))
    return items


def collect_sources(topics: Iterable[dict], timeout: int) -> tuple[list[SourceItem], list[str]]:
    sources: list[SourceItem] = []
    errors: list[str] = []
    seen: set[str] = set()
    for topic in topics:
        for feed_url in topic.get("feeds", []):
            try:
                for item in fetch_feed(topic["name"], feed_url, timeout):
                    if item.url not in seen:
                        sources.append(item)
                        seen.add(item.url)
            except (URLError, TimeoutError, ElementTree.ParseError, OSError) as exc:
                errors.append(f"{topic['name']} feed failed: {feed_url} ({exc})")
    return sources, errors
