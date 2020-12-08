from flask import Flask, render_template, request,session
#import keras.backend.tensorflow_backend as tb
#tb._SYMBOLIC_SCOPE.value = True
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
import psycopg2
import re
from jira.client import JIRA
from flask import current_app
from flask_mail import Mail
from flask_mail import Message
import threading
import datetime

import nltk
from nltk.chat.util import Chat, reflections
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

# from keras.models import load_model
# model = load_model('chatbot_model.h5')
import json
# import random
# intents = json.loads(open('intents.json').read())
# words = pickle.load(open('words.pkl','rb'))
# classes = pickle.load(open('classes.pkl','rb'))




app = Flask(__name__)
app.testing = False
app.secret_key = 'super secret key'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sajasmine175@gmail.com'
app.config['MAIL_PASSWORD'] = 'stratapps'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'sajasmine175@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['DEBUG'] = True
mail = Mail(app)
model_nltk = pickle.load(open("nltk.pkl", 'rb'))

# english_bot = ChatBot("Chatterbot", storage_adapter='chatterbot.storage.SQLStorageAdapter',
#                     logic_adapters=[
#                             {
#                                 'import_path': 'chatterbot.logic.BestMatch',
#                                 'default_response': 'I am sorry, but I do not understand. I am still learning.',
#                                 'maximum_similarity_threshold': 0.90
#                             }
#                         ]
#                     )
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("./greetings.yml")    

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

# def bow(sentence, words, show_details=True):
#     # tokenize the pattern
#     sentence_words = clean_up_sentence(sentence)
#     # bag of words - matrix of N words, vocabulary matrix
#     bag = [0]*len(words)
#     isFound = False
#     for s in sentence_words:
#         for i,w in enumerate(words):
#             if w == s: 
#                 # assign 1 if current word is in the vocabulary position
#                 bag[i] = 1
#                 if show_details:
#                     isFound = True
#                     print ("found in bag: %s" % w)
#     if(isFound == True):
#         return (np.array(bag))
#     else:
#         return -1000

# def predict_class(sentence, model):
#     # filter out predictions below a threshold
#     p = bow(sentence, words,show_details=True)
#     print('res', isinstance(p, np.ndarray),  p)
#     if(not isinstance(p, np.ndarray) and p == -1000):
#         return -1000
#     else:
#         res = model.predict(np.array([p]))[0]
        
#         ERROR_THRESHOLD = 0.25
#         results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
#         # sort by strength of probability
#         results.sort(key=lambda x: x[1], reverse=True)
#         return_list = []
#         for r in results:
#             return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
#         return return_list

# def getResponse(ints, intents_json):
#     if(ints == -1000):
#         tag = 'noanswer'
#         list_of_intents = intents_json['intents']
#         for i in list_of_intents:
#             if(i['tag']== tag):
#                 result = random.choice(i['responses'])
#                 break
#         return result
#     else:
#         tag = ints[0]['intent']
#         print('tag', tag)
#         list_of_intents = intents_json['intents']
#         for i in list_of_intents:
#             if(i['tag']== tag):
#                 result = random.choice(i['responses'])
#                 break
#         return result

# def chatbot_response(msg):
#     print('msg',msg)
#     ints = predict_class(msg, model)
#     res = getResponse(ints, intents)
#     return res

@app.route("/")
def home():
    session['mail_id'] = ''
    session['count'] = 0
    session['name'] = ''
    return render_template("index_new.html")



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg) 
        print ("sent")

def send_email(sub,id, to):
    app = current_app._get_current_object()
    msg = Message(subject=sub,
                  sender='sajasmine175@gmail.com', recipients=to)
    msg.html=render_template('mail_content.html', issueLink='https://xamplify.atlassian.net/browse/'+str(id))
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# @app.route("/chatterbot")
# def get_bot_response():
#     print(request)
#     userText = request.args.get('msg')
#     ts = datetime.datetime.now()
#     print(session,session['count'], re.search(regex,userText))
#     if(session['count'] == 0 and re.search(regex,userText)):
#         print("mail id is entered")
#         session['mail_id'] = userText 
#         session['count'] = 1
#         return 'Thanks, how can I help you?'
#     elif(session['count'] == 0 and re.search(regex,userText) == None):
#         return 'Please enter valid email id'

#     conn = psycopg2.connect(database="chatbotdb", user = "postgres", password = "postgres", host = 'localhost', port = "5432")
#     print("*******", english_bot.get_response(userText))
#     res = str(english_bot.get_response(userText))
#     cursor = conn.cursor()
#     s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,search_txt,persona,created_at) VALUES(%s, %s, %s, %s, %s)", (session['mail_id'], userText, userText, 'human', ts))
#     s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,resp_txt,persona,created_at) VALUES(%s, %s, %s, %s, %s) ", (session['mail_id'], res, res, 'bot',ts ))
#     print('s',s)
#     conn.commit() 
#     cursor.close()
#     conn.close()
#     return res

@app.route("/createjira")
def create_jira():
    print("############################################")
    summaryText=request.args.get('summary')
    descriptionText=request.args.get('description')
    emailidText=request.args.get('emailid')
    jira=JIRA(basic_auth=('agayatri@stratapps.com','ECCxYPP8gydsLlXR9lMKEC40'),
    options={'headers': {'content-type': 'application/json'},'server': 'https://xamplify.atlassian.net/'})
    new_issue = jira.create_issue(project={'key': 'XBI'}, summary= summaryText,   description=descriptionText, issuetype={'name': 'Bug'})
    print(new_issue)
    send_email(summaryText, new_issue, ['graghavendra@stratapps.com' ,'kjasmine@stratapps.com', emailidText])
    return str(new_issue)
    
@app.route("/chat-nltk")
def get_response():
    userText = request.args.get('msg')
    ts = datetime.datetime.now()
    print(session,session['count'], re.search(regex,userText))
    # if(session['count'] == 0 ):
    #     print("mail id is entered")
    #     session['mail_id'] = userText 
    #     session['count'] = 1
    #     return 'Hi! Before we get started I have a few questions for you. First, we’ll need your email address in case we need to follow up with you about your question [SPLIT] Please enter your email'
    # elif(session['count'] == 1 and re.search(regex,userText)):
    #     session['count'] = 2
    #     return 'Hi! My name is Jasmine, how can I help you today? [SPLIT] What is your name?'
    # elif(session['count'] == 1 and re.search(regex,userText) == None ):
    #     return 'Please enter valid email id'
    # elif(session['count'] == 2):
    #     session['count'] = 3
    #     session['name'] = userText
    #     return 'Welcome to xAmplify '+ userText+ ', how can we assist you today?'

    res= str(model_nltk.respond(userText))
    if(res == 'None'):
        return 'Please provide more info'
    else:
        conn = psycopg2.connect(database="chatbotdb", user = "postgres", password = "postgres", host = 'localhost', port = "5432")
        cursor = conn.cursor()
        s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,search_txt,persona,created_at) VALUES(%s, %s, %s, %s, %s)", (session['mail_id'], userText, userText, 'human', ts))
        s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,resp_txt,persona,created_at) VALUES(%s, %s, %s, %s, %s) ", (session['mail_id'], res, res, 'bot',ts ))
        print('s',s)
        conn.commit() 
        cursor.close()
        conn.close()
        return res

# @app.route("/chat-dl")
# def get_response_dl():
#     userText = request.args.get('msg')
#     ts = datetime.datetime.now()
#     print(session,session['count'], re.search(regex,userText))
#     if(session['count'] == 0 and re.search(regex,userText)):
#         print("mail id is entered")
#         session['mail_id'] = userText 
#         session['count'] = 1
#         return 'Thanks, how can I help you?'
#     elif(session['count'] == 0 and re.search(regex,userText) == None):
#         return 'Please enter valid email id'
#     res= str(chatbot_response(userText))
#     conn = psycopg2.connect(database="chatbotdb", user = "postgres", password = "postgres", host = 'localhost', port = "5432")
#     cursor = conn.cursor()
#     s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,search_txt,persona,created_at) VALUES(%s, %s, %s, %s, %s)", (session['mail_id'], userText, userText, 'human', ts))
#     s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,resp_txt,persona,created_at) VALUES(%s, %s, %s, %s, %s) ", (session['mail_id'], res, res, 'bot',ts ))
#     print('s',s)
#     conn.commit() 
#     cursor.close()
#     conn.close()
#     return res

# @app.route("/get-intents")
# def get_intents():
#         data_file = open('intents.json').read()
#         intents = json.loads(data_file)
#         return intents

# @app.route("/get-chats")
# def get_chats():
#         chat = Chat(set_pairs, reflections)
#         str1=json.dumps(chat)
#         str1
#         # data_file = open('intents.json').read()
#         # intents = json.loads(data_file)
#         # return intents

        
#         # filename_model = 'nltk.pkl'
#         # pickle.dump(chat, open(filename_model, 'wb'))


if __name__ == '__main__':
	app.run(debug=False,threaded=False)