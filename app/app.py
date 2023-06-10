from flask import Flask, request
from models.hybrid.prediction import recommendation_place

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/recommendation')
def hello_test():  # put application's code here
    args = request.args

    user_id = args.get('user_id')
    mood_input = args.get('mood')
    budget_input = args.get('budget')
    city_input = args.get('city')

    

    recommendation = recommendation_place()
    return dict({
        "success": True,
        "data": recommendation.to_dict(orient='records')
    })


if __name__ == '__main__':
    app.run()
