#Flask REST-API chatbot

# Install flask for running the server:
# pip install flask
from flask import Flask,request



PATH_MODEL = ""

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, I am a Chatbot which offer help for culinary recipes"


# Process the message of the user send to the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    pass


def load_model():
    pass



app.run()