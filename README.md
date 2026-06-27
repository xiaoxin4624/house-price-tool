# 每日中文主题摘要

这是一个 Python 3.11+ 最小可运行项目，用于每天抓取公开来源并生成中文主题摘要。项目会保留所有来源链接；如果某个主题没有抓到可靠来源，会明确输出“未找到可靠来源”。

## 项目结构

```text
.
├── .env.example                  # 环境变量模板，复制为 .env 后填写密钥和邮箱配置
├── README.md                     # 使用说明
├── requirements.txt              # Python 依赖
└── src/
    └── daily_cn_digest/
        ├── __init__.py
        ├── __main__.py           # 支持 python -m daily_cn_digest
        ├── config.py             # 读取 .env 配置
        ├── emailer.py            # SMTP 邮件发送
        ├── fetchers.py           # RSS/公开链接抓取
        ├── main.py               # 程序入口
        ├── render.py             # 中文摘要渲染
        └── topics.py             # 主题、关键词和来源配置
```

## 覆盖主题

- 中国30年国债期货、TL2609或30年国债期货连续合约
- 资金面、央行公开市场操作、PBOC信号
- 超长期特别国债发行
- CPI/PPI、社融、债券供需
- 科创50ETF期权和A股波动（如无重大变化可简写）
- OpenAI / ChatGPT / Codex 产品更新
- 山西/太原高考志愿或招生政策（如无时效变化可省略）

## 快速开始

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
PYTHONPATH=src python -m daily_cn_digest
```

运行后会在 `output/` 目录生成类似 `digest-YYYY-MM-DD.md` 的 Markdown 文件。

## 邮件发送

在 `.env` 中填写 SMTP 配置：

```dotenv
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_user
SMTP_PASSWORD=your_password
SMTP_USE_TLS=true
EMAIL_FROM=sender@example.com
EMAIL_TO=receiver1@example.com,receiver2@example.com
EMAIL_SUBJECT_PREFIX=每日中文主题摘要
```

如果 SMTP 主机或收件人为空，程序会跳过邮件发送，但仍会生成摘要文件。

## 可靠性规则

- 只基于抓取到的公开来源标题、摘要和链接生成内容。
- 抓取失败或无可靠来源时，输出“未找到可靠来源”。
- 不编造数据、不补写未确认的价格、规模、日期或政策细节。
