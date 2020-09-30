import nltk
from nltk.chat.util import Chat, reflections
import pickle

set_pairs = [
    [
        'my name is (.*)',
        ['Hello %1, How are you doing today ?', ]
    ],
    [
        'hi|hey|hello',
        ['Hello', 'Hey there', ]
    ],
    [
        'what is your name?',
        ['You can call me a chatbot ?', ]
    ],
    [
        'how are you ?',
        ['I am fine, thank you! How can i help you?', ]
    ],
    [
        'I am fine, thank you',
        ['great to hear that, how can i help you?', ]
    ],
    [
        'how can i help you? ',
        ['i am looking for online guides and courses to learn data science, can you suggest?',
         'i am looking for data science training platforms', ]
    ],
    [
        'im (.*) doing good',
        ['Thats great to hear', 'How can i help you?:)', ]
    ],
    [
        'i am looking for online guides and courses to learn data science, can you suggest?',
        ['Pluralsight is a great option to learn data science. You can check their website', ]
    ],
    [
        'thanks for the suggestion. do they have great authors and instructors?',
        ['Yes, they have the world class best authors, that is their strength;)', ]
    ],
    [
        '(.*) thank you so much, that was helpful',
        ['Iam happy to help', 'No problem, you are welcome', ]
    ],
    [
        'quit',
        ['Bye, take care. See you soon :) ',
            'It was nice talking to you. See you soon :)']
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