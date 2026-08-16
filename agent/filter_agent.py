from langchain_core.messages import HumanMessage, AIMessage
from config.settings import TOPICS_OF_INTEREST


def filter_agent(state: dict) -> dict:
    articles = state.get("raw_articles", [])
    filtered = []

    for article in articles:
        if is_relevant(article):
            filtered.append(article)

    print(f"[Filter Agent] من {len(articles)} مقالة → بقي {len(filtered)}")
    return {**state, "articles": filtered}


def is_relevant(article: dict) -> bool:
    text = f"{article['title']} {article['summary']}".lower()

    for topic in TOPICS_OF_INTEREST:
        if topic.lower() in text:
            return True

    return False


