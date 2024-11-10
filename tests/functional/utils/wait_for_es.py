import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


def get_es_ready():
    print("Starting elasticsearch test ping")
    es_client = Elasticsearch(hosts=os.getenv("ES_HOST"))
    while True:
        if es_client.ping():
            break
        time.sleep(1)
