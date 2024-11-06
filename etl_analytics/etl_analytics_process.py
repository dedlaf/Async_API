import argparse
import logging
import time
from settings import sentrysdk
import sentry_sdk

from etl_analytics_process_handler import ETLAnalyticsProcessHandler

sentry_sdk.init(
    dsn=sentrysdk,
    traces_sample_rate=1.0,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()


if __name__ == "__main__":
    sentry_sdk.profiler.start_profiler()

    etl_process_handler = ETLAnalyticsProcessHandler()

    while True:
        try:
            etl_process_handler.handle_process()
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            etl_process_handler = ETLAnalyticsProcessHandler()
        finally:
            time.sleep(30)
