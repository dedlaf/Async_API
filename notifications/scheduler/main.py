import logging
import time

import schedule
from connections import get_db_connection, get_rabbitmq_connection
from fetcher import Fetcher
from rb_producer import Producer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def fetch_and_parse_events():
    logging.info("Fetching events")
    try:
        fetcher = Fetcher(get_db_connection())
        events = fetcher.get_all()
        logging.info(events)
        if events:
            producer = Producer(get_rabbitmq_connection())
            for event in events:
                producer.publish(message=event, queue_name="delayed_notify")

    except Exception as e:
        logging.info(f"Error fetching events: {e}")


schedule.every(3).seconds.do(fetch_and_parse_events)

logging.info("Starting scheduler...")
while True:
    schedule.run_pending()
    time.sleep(1)
