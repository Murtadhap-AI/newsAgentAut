# agent/delivery_agent.py

import os
from datetime import datetime
from dotenv import load_dotenv
from tools.telegram_sender import send_telegram_message

load_dotenv()


def format_header(articles: list) -> str:
    count = len(articles)
    week_number = datetime.now().isocalendar()[1]
    
    return (
        f"🗞️ <b>ملخص أخبار AI</b>\n"
        f"📅 الأسبوع {week_number}\n"
        f"────────────────\n"
        f"📬 <b>{count}</b> أخبار بانتظارك\n"
        f"سيتم إرسالها الآن واحدة تلو الأخرى 👇"
    )


def format_single_article(index: int, article: dict) -> str:
    title   = article.get("title", "بدون عنوان")
    summary = article.get("summary", "بدون ملخص")
    insight = article.get("personal_insight", "")
    url     = article.get("url", "")

    lines = []
    lines.append(f"{index}️⃣ <b>{title}</b>")
    lines.append(f"────────────────")
    lines.append(f"📝 {summary}")

    if insight:
        lines.append(f"")
        lines.append(f"🎯 <b>أهميته ليك:</b>")
        lines.append(f"{insight}")

    if url:
        lines.append(f'🔗 <a href="{url}">اقرأ المزيد</a>')

    return "\n".join(lines)

def delivery_agent(state: dict) -> dict:
    articles = state.get("summarized_articles", [])
    
    if not articles:
        print("⚠️ لا توجد مقالات للإرسال")
        return {**state, "delivery_status": "no_articles"}
    
    # أرسل الـ header أولاً
    header = format_header(articles)
    send_telegram_message(header)
    
    # أرسل كل خبر لحاله
    failed = 0
    for i, article in enumerate(articles, start=1):
        message = format_single_article(i, article)
        success = send_telegram_message(message)
        if not success:
            failed += 1
        print(f"📨 إرسال خبر {i}/{len(articles)}...")
    
    # قرر الحالة النهائية
    if failed == 0:
        print(f"✅ تم إرسال كل الأخبار ({len(articles)}) بنجاح")
        return {**state, "delivery_status": "sent"}
    elif failed < len(articles):
        print(f"⚠️ أُرسل معظمها، فشل {failed} منها")
        return {**state, "delivery_status": "partial"}
    else:
        print("❌ فشل إرسال كل الأخبار")
        return {**state, "delivery_status": "failed"}

