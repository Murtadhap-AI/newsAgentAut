from dotenv import load_dotenv
import os

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

# Email
EMAIL_ADDRESS  = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_MODEL = "Qwen3:8b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
# مصادر الأخبار ()
# config/settings.py

RSS_SOURCES = [
    "https://feeds.feedburner.com/oreilly/radar",
    "https://towardsdatascience.com/feed",
]

TOPICS_OF_INTEREST = [
    "artificial intelligence", "machine learning", "LLM",
    "langchain", "langgraph", "ollama", "multi-agent",
    "deep learning", "neural network", "GPT", "Claude"
]


# ── الجديد ──────────────────────────────────────
USER_PROFILE = {
    "name": "مرتضى",
    "background": " مبتدء يحاول يطور من نفسة حتى يكون محترف ومضبط  AI Engineer",
    "skills": [
        "Python", "LangGraph", "Ollama",
        "multi-agent systems", "RAG"
    ],
    "current_project": "نظام multi-agent يجمع أخبار AI أسبوعياً باستخدام LangGraph و qwen3:8b",
    "goal": "أبني portfolio قوي وأحصل على وظيفة AI Engineer",
    "learning_path": "LangGraph → RAG → deployment → job applications"
}
SCHEDULE_INTERVAL_DAYS = 1  