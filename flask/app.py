from flask import Flask
from flask import request
from kafka import KafkaProducer

app = Flask(__name__)


@app.route('/load-data', methods=['POST'])
def load_data():
    data: dict = request.json
    producer = KafkaProducer(bootstrap_servers=['55a785524c3e:9092'])
    try:
        producer.send(
            topic=data.get('topic'),
            value=data.get('value').encode(),
            key=data.get('user_id').encode(),
        )
        return "Successfully loaded data to kafka"
    except Exception as e:
        return f"Failed to load data to kafka: {str(e)}"


if __name__ == '__main__':
    app.run()
