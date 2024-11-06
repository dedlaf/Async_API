from flask import Flask
from flask import request
from kafka import KafkaProducer
from settings import kafka_host, sentrysdk
from schemas import KafkaData
import logging
import requests
import sentry_sdk


sentry_sdk.init(
    dsn=sentrysdk,
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)
app = Flask(__name__)


@app.route('/analytics/load-data', methods=['POST'])
def load_data():
    user_id = requests.get("http://auth:8070/auth/token/user", cookies=request.cookies).json()['id']
    data: KafkaData = KafkaData(
        value=request.json['value'],
        topic=request.json['topic'],
        user_id=user_id
    )
    producer = KafkaProducer(bootstrap_servers=[kafka_host])
    try:
        producer.send(
            topic=data.topic,
            value=data.value.encode(),
            key=str(data.user_id).encode(),
        )
        return "Successfully loaded data to Kafka"
    except Exception as e:
        logging.error(f"Failed to load data to kafka: {str(e)}")
        return "Failed to load data to Kafka"


if __name__ == '__main__':
    app.run()
