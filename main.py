# main.py
import time
import logging
import sys

from agent.scheduler_agent import create_scheduler, run_news_pipeline


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M"
    )

    logging.info("🤖 NewsAgent يبدأ...")

    # تشغيل أولي فوري
    logging.info("📰 تشغيل أولي فوري...")
    run_news_pipeline()

    # ابدأ الـ scheduler
    scheduler = create_scheduler()
    scheduler.start()
    logging.info("⏰ الـ scheduler شغّال — يتحقق كل يوم الساعة 9")

    # خلّي البرنامج حي
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("🛑 إيقاف NewsAgent...")
        scheduler.shutdown()
        logging.info("✅ أوقف بنظافة")
        sys.exit(0)


if __name__ == "__main__":
    main()