# agent/scheduler_agent.py
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from graph import news_graph

logging.basicConfig(level=logging.INFO)


def run_news_pipeline():
    logging.info("🔍 NewsAgent: أتحقق من الأخبار اليوم...")
    try:
        result = news_graph.invoke({})
        
        articles = result.get("summarized_articles", [])
        
        if not articles:
            logging.info("📭 ما في أخبار جديدة اليوم — ما راح أرسل")
            return
            
        status = result.get("delivery_status", "unknown")
        logging.info(f"✅ أرسلت {len(articles)} خبر — الحالة: {status}")
        
    except Exception as e:
        logging.error(f"❌ فشل — {e}")

def create_scheduler():
    """يُنشئ ويُعيد scheduler جاهز للتشغيل"""
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        func=run_news_pipeline,
        trigger=CronTrigger( hour=9, minute=0),
        id="weekly_news",
        name="Weekly AI News Digest",
        replace_existing=True
    )
    
    return scheduler