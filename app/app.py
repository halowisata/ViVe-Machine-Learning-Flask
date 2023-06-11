from flask import Flask, request
from models.hybrid.prediction import recommendation_place
from utils.create_user_handler import create_user_main
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

    recommendation = recommendation_place(
        user_id, mood_input, budget_input, city_input)
    return dict({
        "success": True,
        "data": recommendation.to_dict(orient='records')
    })


@app.route('/users', methods=['POST'])
def create_user():
    # TODO: fix this if user is already existing
    user_data = request.json
    address = user_data.get('address')
    age = user_data.get('age')

    user = create_user_main(address, age)

    if user is not None:
        return dict({
            "success": True,
            "message": f"User with ID {user['User_Id']} created successfully."
        })
    else:
        return dict({
            "success": False,
            "message": "failed to create user"
        })


if __name__ == '__main__':
    app.run()
