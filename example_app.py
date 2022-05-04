import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/home_page', methods=["GET"])
def home_page():
    return "Hello, Welcome to my Homepage!"


@app.route("/display_message", methods=["POST"])
def display_message():
    requested_message = json.loads(request.data)
    return f"Hello, the message to display is: {requested_message['message']}"
    # return requested_message


@app.route("/display_message_text", methods=["POST"])
def display_message_text():
    requested_message = request.data.decode()
    return f"Hello, the text message is: {requested_message}"



@app.route("/get_user/<user>", methods=["GET"])
def get_user(user):
    return f"Hello, the user is: {user}"


@app.route("/delete_user/<user>", methods=["DELETE"])
def delete_user(user):
    return f"User {user} has been deleted"

if __name__ == '__main__':
    app.run()