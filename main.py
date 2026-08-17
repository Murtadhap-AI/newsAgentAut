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
    run_news_pipeline()  # يشتغل مرة وحدة ويقفل
    logging.info("✅ انتهى")


if __name__ == "__main__":
    main()

