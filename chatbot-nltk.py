import nltk
from nltk.chat.util import Chat, reflections
import pickle

set_pairs = [
  [
    "my name is (.*)",
    [
      "Hello %1, How are you today ?",
      
    ]
  ],
  [
    "what is your name ?",
    [
      "My name is Chatty and I'm a chatbot ?",
      
    ]
  ],
  [
    "how are you ?",
    [
      "I'm doing good\nHow about You ?",
      
    ]
  ],
  [
    "sorry (.*)",
    [
      "Its alright",
      "Its OK, never mind",
      
    ]
  ],
  [
    "i'm (.*) doing good",
    [
      "Nice to hear that",
      "Alright :)",
      
    ]
  ],
  [
    "hi|hey|hello",
    [
      "Hello",
      "Hey there",
      
    ]
  ],
  [
    "(.*) age?",
    [
      "I'm a computer program dude\nSeriously you are asking me this?",
      
    ]
  ],
  [
    "what (.*) want ?",
    [
      "Make me an offer I can't refuse",
      
    ]
  ],
  [
    "(.*) created ?",
    [
      "Nagesh created me using Python's NLTK library ",
      "top secret ;)",
      
    ]
  ],
  [
    "(.*) (location|city) ?",
    [
      'Chennai, Tamil Nadu',
      
    ]
  ],
  [
    "how is weather in (.*)?",
    [
      "Weather in %1 is awesome like always",
      "Too hot man here in %1",
      "Too cold man here in %1",
      "Never even heard about %1"
    ]
  ],
  [
    "i work in (.*)?",
    [
      "%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",
      
    ]
  ],[
    "(.*)raining in (.*)",
    [
      "No rain since last week here in %2",
      "Damn its raining too much here in %2"
    ]
  ],
  [
    "how (.*) health(.*)",
    [
      "I'm a computer program, so I'm always healthy ",
      
    ]
  ],
  [
    "(.*) (sports|game) ?",
    [
      "I'm a very big fan of Football",
      
    ]
  ],
  [
    "who (.*) sportsperson ?",
    [
      "Messy",
      "Ronaldo",
      "Roony"
    ]
  ],
  [
    "who (.*) (moviestar|actor)?",
    [
      "Brad Pitt"
    ]
  ],
  [
    "(.*) xAmplify",
    [
      "A new outbound Through Channel Marketing Automation platform that empowers you to deliver co-branded content through your channel partners"
    ]
  ],
  [
    "xAmplify (.*)",
    [
      "A new outbound Through Channel Marketing Automation platform that empowers you to deliver co-branded content through your channel partners"
    ]
  ],
  [
    "xAmplify",
    [
      "A new outbound Through Channel Marketing Automation platform that empowers you to deliver co-branded content through your channel partners"
    ]
  ],
  [
    "quit",
    [
      "BBye take care. See you soon :) ",
      "It was nice talking to you. See you soon :)"
    ]
  ],
  
]
my_reflections =  {'i am': 'you are',
     'i was': 'you were',
     'i': 'you',
     "i'm": 'you are',
     "i'd": 'you would',
     "i've": 'you have',
     "i'll": 'you will',
     'my': 'your',
     'you are': 'I am',
     'you were': 'I was',
     "you've": 'I have',
     "you'll": 'I will',
     'your': 'my',
     'yours': 'mine',
     'you': 'me',
     'me': 'you'}

chat = Chat(set_pairs, reflections)
filename_model = 'nltk.pkl'
pickle.dump(chat, open(filename_model, 'wb')) 