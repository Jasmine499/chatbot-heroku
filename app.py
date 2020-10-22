from flask import Flask, render_template, request,session
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
import psycopg2
import re
from jira.client import JIRA
from flask import current_app
from flask_mail import Mail
from flask_mail import Message
import threading

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
model = pickle.load(open("nltk.pkl", 'rb'))

english_bot = ChatBot("Chatterbot",
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


@app.route("/")
def home():
    session['mail_id'] = ''
    session['count'] = 0
    return render_template("index_new.html")



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg) 
        print ("sent")

def send_email(id, to):
    app = current_app._get_current_object()
    msg = Message(subject='hello',
                  sender='sajasmine175@gmail.com', recipients=to)
    msg.body = "Issue has been created and jira id is "+str(id)
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

@app.route("/chatterbot")
def get_bot_response():
    print(request)
    userText = request.args.get('msg')

    
    print(session,session['count'], re.search(regex,userText))
    if(session['count'] == 0 and re.search(regex,userText)):
        print("mail id is entered")
        session['mail_id'] = userText 
        session['count'] = 1
        return 'Thanks, how can I help you?'
    elif(session['count'] == 0 and re.search(regex,userText) == None):
        return 'Please enter valid email id'

    conn = psycopg2.connect(database="chatbotdb", user = "postgres", password = "postgres", host = 'localhost', port = "5432")
    res = str(english_bot.get_response(userText))
    cursor = conn.cursor()
    s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,search_txt,persona,created_at) VALUES(%s, %s, %s, %s, now())", (session['mail_id'], userText, userText, 'human', ))
    s= cursor.execute("INSERT INTO chathistry (user_mail_id,text,resp_txt,persona,created_at) VALUES(%s, %s, %s, %s, now()) ", (session['mail_id'], res, res, 'bot', ))
    print('s',s)
    conn.commit() 
    cursor.close()
    conn.close()
    return res

@app.route("/createjira")
def create_jira():
    print("############################################")
    summaryText=request.args.get('summary')
    descriptionText=request.args.get('description')
    jira=JIRA(basic_auth=('dtejashwini@stratapps.com','0DoVu9iM9acCZ795ngv20AEC'),
    options={'headers': {'content-type': 'application/json'},'server': 'https://xamplify.atlassian.net/'})
    new_issue = jira.create_issue(project={'key': 'XBI'}, summary= summaryText,   description=descriptionText, issuetype={'name': 'Bug'})
    print(new_issue)
    send_email(new_issue, ['graghavendra@stratapps.com','kjasmine@stratapps.com'])
    return str(new_issue)
    
@app.route("/chat-nltk")
def get_response():
    userText = request.args.get('msg')
    return str(model.respond(userText))

if __name__ == '__main__':
	app.run(debug=True)
