# agent/collector_agent.py

from tools.rss_reader import fetch_articles
from agent.filter_agent import filter_agent
from agent.summarizer_agent import summarizer_agent


def collector_agent(state: dict) -> dict:
    # الخطوة 1: جيب المقالات
    articles = fetch_articles()
    
    # الخطوة 2: حدّث الـ state
    state = {**state, "raw_articles": articles}
    
    # الخطوة 3: صفّي
    state = filter_agent(state)
    
    # الخطوة 4: لخّص
    state = summarizer_agent(state)
    
    return state


if __name__ == "__main__":
    result = collector_agent({})
    
    articles = result.get("summarized_articles", [])
    print(f"✅ جُمع {len(result.get('raw_articles', []))} مقالة")
    print(f"✅ صُفّي {len(result.get('filtered_articles', []))} مقالة")
    print(f"✅ لُخّص {len(articles)} مقالة\n")
    
    for article in articles:
        print(f"📰 {article['title']}")
        print(f"{article.get('ai_summary', 'لا يوجد ملخص')}")
        print("-" * 50)