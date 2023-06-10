from flask import Flask
from models.hybrid.prediction import recommendation_place

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/recommendation')
def hello_test():  # put application's code here
    recommendation = recommendation_place()
    return dict({
        "success": True,
        "data": recommendation.to_dict(orient='records')
    })


if __name__ == '__main__':
    app.run()
