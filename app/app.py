from flask import Flask
from models.knowledge_constraint.prediction import knowledge_main as knowledge_constraint

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/recommendation')
def hello_test():  # put application's code here
    test = knowledge_constraint()
    print(test)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
