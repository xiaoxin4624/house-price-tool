from __future__ import annotations

TOPICS = [
    {
        "name": "中国30年国债期货 / TL2609 / 连续合约",
        "queries": ["中国30年国债期货 TL2609", "30年国债期货 连续合约", "TL2609 国债期货"],
        "feeds": [
            "https://newssearch.eastmoney.com/rss/search.aspx?keyword=30%E5%B9%B4%E5%9B%BD%E5%80%BA%E6%9C%9F%E8%B4%A7",
        ],
    },
    {
        "name": "资金面 / 央行公开市场操作 / PBOC信号",
        "queries": ["央行 公开市场操作 资金面", "PBOC open market operations liquidity"],
        "feeds": ["http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html"],
    },
    {
        "name": "超长期特别国债发行",
        "queries": ["超长期特别国债 发行", "财政部 超长期特别国债"],
        "feeds": [],
    },
    {
        "name": "CPI/PPI / 社融 / 债券供需",
        "queries": ["中国 CPI PPI 社融 债券 供需", "社融 CPI PPI 债券供需"],
        "feeds": [],
    },
    {
        "name": "科创50ETF期权和A股波动",
        "queries": ["科创50ETF期权 A股 波动", "科创50ETF期权 波动率"],
        "feeds": [],
        "optional": True,
    },
    {
        "name": "OpenAI / ChatGPT / Codex 产品更新",
        "queries": ["OpenAI ChatGPT Codex product updates", "OpenAI Codex ChatGPT updates"],
        "feeds": ["https://openai.com/news/rss.xml"],
    },
    {
        "name": "山西/太原高考志愿或招生政策",
        "queries": ["山西 太原 高考志愿 招生政策", "山西招生考试网 高考志愿"],
        "feeds": [],
        "optional": True,
    },
]
