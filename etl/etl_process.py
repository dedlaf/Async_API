import argparse
import logging
import time

from etl_process_handler import ETLProcessHandler
from settings import FILE_PATH
from state import JsonFileStorage, State

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--date")
args = parser.parse_args()


if __name__ == "__main__":
    file_storage = JsonFileStorage(FILE_PATH)
    state = State(file_storage)

    if args.date:
        state.set_last_modified(args.date)

    etl_process_handler = ETLProcessHandler(state)

    while True:
        try:
            etl_process_handler.handle_process()
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            etl_process_handler = ETLProcessHandler(state)
        finally:
            time.sleep(30)
