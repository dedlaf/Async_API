from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


@app.route('/load-data', methods=['POST'])
def load_data():
    print(request.data)
    print(request.json)
    print(request)
    return request.data


if __name__ == '__main__':
    app.run()
