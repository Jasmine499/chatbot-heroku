from flask import Flask, render_template, request
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle

app = Flask(__name__)

model = pickle.load(open("nltk.pkl", 'rb'))

# english_bot = ChatBot("Chatterbot", storage_adapter='chatterbot.storage.SQLStorageAdapter',database_uri='sqlite:///db.sqlite3')
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("./greetings.yml")

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/chatterbot")
# def get_bot_response():
#     print(request)
#     userText = request.args.get('msg')
#     return str(english_bot.get_response(userText))

@app.route("/chat-nltk")
def get_response():
    userText = request.args.get('msg')
    return str(model.respond(userText))

if __name__ == '__main__':
	app.run(debug=True)
