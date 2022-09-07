from flask import Flask
from flask import request
from flask import Response
import requests

TOKEN = "5725012312:AAGnpucEHiCUvf1byIqAKuxG4plv5cgnOIU"
 
app = Flask(__name__)
 
def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)

        g_chat_id = message['message']['chat']['id']
        g_file_id = message['message']['photo'][0]['file_id']
        print("g_chat_id-->", g_chat_id)
        print("g_image_id-->", g_file_id)
 
        return chat_id,txt,g_file_id
    except:
        print("NO text found-->>")

def tel_parse_get_message(message):
    print("message-->",message)
  
    try:
        g_chat_id = message['message']['chat']['id']
        g_file_id = message['message']['photo'][0]['file_id']
        print("g_chat_id-->", g_chat_id)
        print("g_image_id-->", g_file_id)
 
        return g_file_id
    except:
        print("NO file found found-->>")
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
 
    return r
 
def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
        'caption': "This is a sample image"
    }
 
    r = requests.post(url, json=payload)
    return r

def tel_send_audio(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAudio'  
    payload = {
        'chat_id': chat_id,
        "audio": "http://www.largesound.com/ashborytour/sound/brobob.mp3",
    }
 
    r = requests.post(url, json=payload)
    return r

def tel_send_video(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
 
    payload = {
        'chat_id': chat_id,
        "video": "https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4",
 
    }
 
    r = requests.post(url, json=payload)
 
    return r

def tel_send_document(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
 
    payload = {
        'chat_id': chat_id,
        "document": "http://www.africau.edu/images/default/sample.pdf",
 
    }
 
    r = requests.post(url, json=payload)
 
    return r

def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    payload = {
        'chat_id': chat_id,
        "question": "In which direction does the sun rise?",
        "options": (["North", "South", "East", "West"]),
        "is_anonymous": False,
        "type": "quiz",
        "correct_option_id": 2
    }
 
    r = requests.post(url, json=payload)
 
    return r

def tel_send_button(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
        'text': "What is this?",
                'reply_markup': {'keyboard': [[{'text': 'supa'}, {'text': 'mario'}]]}
    }
 
    r = requests.post(url, json=payload)
 
    return r

def tel_send_inlinebutton(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
        'text': "What is this?",
        'reply_markup': {
            "inline_keyboard": [[
                {
                    "text": "A",
                    "callback_data": "ic_A"
                },
                {
                    "text": "B",
                    "callback_data": "ic_B"
                }]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r

def tel_send_inlineurl(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
        'text': "Which link would you like to visit?",
        'reply_markup': {
            "inline_keyboard": [
                [
                    {"text": "google", "url": "http://www.google.com/"},
                    {"text": "youtube", "url": "http://www.youtube.com/"}
                ]
            ]
        }
    }
 
    r = requests.post(url, json=payload)
    return r

def tel_upload_file(file_id):
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    a = requests.post(url)
    json_resp = (a.content)
    print("a-->",a)
    print("json_resp-->",json_resp)
    file_pathh = json_resp['result']['file_path']
    print("file_path-->", file_pathh)
   
    url_1 = f'https://api.telegram.org/file/bot{TOKEN}/{file_pathh}'
    b = requests.get(url_1)
    file_content = b.content
    with open(file_pathh, "wb") as f:
        f.write(file_content)
 
@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt, file_id = tel_parse_message(msg)
            # file_id = tel_parse_get_message(msg)
            print("🚀 ~ file: server.py ~ line 184 ~ file_id", file_id)
            if txt == "hi":
                tel_send_message(chat_id,"Hello, world!")
            elif txt == "image":
                tel_send_image(chat_id)
            elif txt == "audio":
                tel_send_audio(chat_id)
            elif txt == "video":
                tel_send_video(chat_id)
            elif txt == "file":
                tel_send_document(chat_id)
            elif txt == "poll":
                tel_send_poll(chat_id)
            elif txt == "button":
              tel_send_button(chat_id)
            elif txt == "inline":
                tel_send_inlinebutton(chat_id)
            elif txt == "inlineurl":
                tel_send_inlineurl(chat_id)

            if file_id:
                tel_upload_file(file_id)

            else:
                tel_send_message(file_id, chat_id, 'from webhook') 

        except:
            print("from index-->")
 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
    app.run(host="localhost", port=3009, threaded=True)