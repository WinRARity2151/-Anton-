import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import speech_recognition
import difflib
from threading import *
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
DIALOGFLOW_PROJECT_ID = 'small-talk-elwr'
DIALOGFLOW_LANGUAGE_CODE = 'ru'
SESSION_ID = 'Proba'

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def rec_com(text):
    for i in text.split():
        dif=difflib.SequenceMatcher(a='блокнот', b=i.lower())
        if dif.ratio()>0.60:
            os.system('start notepad')
            return 'Запускаю...'
        dif=difflib.SequenceMatcher(a='время', b=i.lower())
        if dif.ratio()>0.60:
            now = datetime.datetime.now()
            return now.strftime("%H:%M")


def record_and_recognize_audio(*args: tuple):
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    with microphone:
        recognized_data = ""

        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Прослушиваем вас...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Проблема с микрофоном")
            return

        try:
            print("Распознаем")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print("Проблема с интернетом")

        return recognized_data

def Answer(dia_text):
    answ=''
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=dia_text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        answ =response.query_result.fulfillment_text
    except InvalidArgument:
        answ=''
    if answ=='':
        answ = 'Извини, я тебя недопонял'
    return answ


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def threading():
    t1=Thread(target=work)
    t1.start()
  
def work():
    while True:
        voice_input = record_and_recognize_audio()
        print(voice_input)
        try:
            for i in voice_input.split():
                dif=difflib.SequenceMatcher(a='антон', b=i.lower())
                if dif.ratio()>0.60:
                    voice_input=voice_input.replace(i,'')
                    entry_1.config(state='normal')
                    entry_1.insert(0.0, '===========================================================')

                    if rec_com(voice_input):
                        entry_1.insert(0.0,'Антон: '+rec_com(voice_input) +'\n')
                    else:
                        entry_1.insert(0.0,'Антон: '+Answer(voice_input) +'\n')
            
                    entry_1.insert(0.0,'Вы: '+voice_input[1:].capitalize () +'\n')
                    entry_1.config(state='disabled')
        except:
            continue
    
def extract_data():
    entry_1.config(state='normal')
    entry_1.insert(0.0, '===========================================================')

    if rec_com(entry_2.get()):
        entry_1.insert(0.0,'Антон: '+'Запускаю...' +'\n')
    else:
        entry_1.insert(0.0,'Антон: '+Answer(entry_2.get()) +'\n')
        
    entry_1.insert(0.0, 'Вы: '+entry_2.get()+'\n') 
    entry_1.config(state='disabled')
    entry_2.delete(0,'end')


window = Tk()
window.geometry("496x205")
window.configure(bg = "#FFFFFF")
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 205,
    width = 496,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    496.0,
    205.0,
    fill="#2B2323",
    outline="")
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    223.0,
    173.99999999999997,
    image=image_image_1
)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    248.0,
    76.99999999999997,
    image=entry_image_1
)
entry_2 = Entry(
    bd=0,
    bg="#ECEAEA",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=42.0,
    y=158.99999999999997,
    width=378.0,
    height=22.0
)
entry_1 = Text(
    bd=0,
    bg="#ECEAEA",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=10.0,
    y=9.999999999999972,
    width=476.0,
    height=132.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=extract_data,
    relief="flat"
)
button_1.place(
    x=420.0,
    y=151,
    width=48.0,
    height=40.0
)
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    231.0,
    170.99999999999997,
    image=entry_image_2
)
window.title("Антон")
window.resizable(False, False)
threading()
window.mainloop()
