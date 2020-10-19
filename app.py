from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
import psycopg2
import re


app = Flask(__name__)

model = pickle.load(open("nltk.pkl", 'rb'))

english_bot = ChatBot("Chatterbot", storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=[
                            'chatterbot.logic.MathematicalEvaluation',
                            'chatterbot.logic.TimeLogicAdapter',
                            'chatterbot.logic.BestMatch',
                            {
                                'import_path': 'chatterbot.logic.BestMatch',
                                'default_response': 'I am sorry, but I do not understand. I am still learning.',
                                'maximum_similarity_threshold': 0.90
                            }
                        ]
                    )
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("./greetings.yml")    

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
mail_id = None  
count = 0 

@app.route("/")
def home():
    global count
    count = 0
    return render_template("index_new.html")

def increment(num):
    global count
    count = num + 1 


@app.route("/chatterbot")
def get_bot_response():
    print(request)
    userText = request.args.get('msg')

    global count
    global mail_id
    print(count, re.search(regex,userText))
    if(count == 0 and re.search(regex,userText)):
        print("mail id")
        mail_id = userText 
        increment(count)
        return 'Thanks, how can I help you?'
    elif(count == 0 and re.search(regex,userText) == None):
        return 'Please enter valid email id'

    conn = psycopg2.connect(database="chatbotdb", user = "postgres", password = "postgres", host = 'localhost', port = "5432")
    res = str(english_bot.get_response(userText))
    cursor = conn.cursor()
    s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,search_txt,persona,created_at) VALUES(%s, %s, %s, %s, now())", (mail_id, userText, userText, 'human', ))
    s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,resp_txt,persona,created_at) VALUES(%s, %s, %s, %s, now()) ", (mail_id, res, res, 'bot', ))
    print('s',s)
    conn.commit() 
    cursor.close()
    conn.close()
    return res

@app.route("/chat-nltk")
def get_response():
    userText = request.args.get('msg')
    return str(model.respond(userText))

if __name__ == '__main__':
	app.run(debug=True)
