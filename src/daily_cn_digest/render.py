from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from .fetchers import SourceItem


def _fmt_dt(value: datetime | None) -> str:
    if value is None:
        return "发布时间未知"
    return value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _recent_items(items: list[SourceItem], lookback_hours: int) -> list[SourceItem]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    recent = [item for item in items if item.published is None or item.published >= cutoff]
    return sorted(recent, key=lambda item: item.published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)


def render_digest(topics: list[dict], items: list[SourceItem], errors: list[str], lookback_hours: int) -> str:
    grouped: dict[str, list[SourceItem]] = defaultdict(list)
    for item in _recent_items(items, lookback_hours):
        grouped[item.topic].append(item)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"# 每日中文主题摘要（{today} UTC）", "", "## 已确认事实"]
    for topic in topics:
        topic_items = grouped.get(topic["name"], [])[:5]
        lines.append(f"### {topic['name']}")
        if not topic_items:
            lines.append("- 未找到可靠来源。")
            continue
        for item in topic_items:
            summary = f"；{item.summary[:160]}" if item.summary else ""
            lines.append(f"- {_fmt_dt(item.published)}：{item.title}{summary}（来源：{item.url}）")

    lines.extend(["", "## 判断分析"])
    for topic in topics:
        count = len(grouped.get(topic["name"], []))
        if count:
            lines.append(f"- {topic['name']}：已检索到 {count} 条候选来源；本工具仅基于来源标题、摘要和链接做保守归纳，不编造缺失数据。")
        elif topic.get("optional"):
            lines.append(f"- {topic['name']}：未找到可靠来源，按需求可省略或简写。")
        else:
            lines.append(f"- {topic['name']}：未找到可靠来源，暂不作方向性判断。")

    lines.extend(["", "## 今日观察项"])
    for topic in topics:
        lines.append(f"- 继续跟踪：{topic['name']}。关键词：{'、'.join(topic.get('queries', []))}")

    lines.extend(["", "## 风险提示"])
    lines.extend([
        "- 本摘要由公开来源自动抓取生成，可能存在来源延迟、链接失效、转载重复或发布时间缺失。",
        "- 未抓到可靠来源时会明确标注，不应据此推断事件不存在。",
        "- 涉及市场与政策内容仅供信息整理，不构成投资建议。",
    ])
    if errors:
        lines.append("- 抓取异常：" + "；".join(errors[:5]))

    lines.extend(["", "## 数据来源链接"])
    if items:
        for item in items:
            lines.append(f"- [{item.title}]({item.url})")
    else:
        lines.append("- 未找到可靠来源。")
    lines.append("")
    return "\n".join(lines)
