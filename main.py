import sys
import json
import threading
import tkinter as tk
import pyttsx3 as tts
import speech_recognition as sr

ASSISTANT_NAME = 'alpha'
ASSISTANT_COMMAND = f'hey {ASSISTANT_NAME}'
ASSISTANT_STOP = 'stop'
INPUT_OUTPUT = 'text.json'

class GameAssistant:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.voice = tts.init()
        self.voice.setProperty('rate', 100)

        self.root = tk.Tk()
        self.root.title('Game Assistant V3')
        self.root.geometry('900x600')
        self.label = tk.Label(text = f'Listening ({ASSISTANT_COMMAND} to start)')
        self.label.pack()

        threading.Thread(target = self.game_assistant_init).start()

        self.root.mainloop()

    def load_responses(filename) -> str:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def find_response(text, data) -> str:
        for item in data['text']:
            if text in item['input']:
                return item['output']
        return None

    def game_assistant_init(self) -> None:
        while True:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration = 0.2)
                    audio = self.recognizer.listen(source)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    self.label.config(text = text) # Uncomment for testing

                    if ASSISTANT_COMMAND in text:
                        self.label.config(text = 'Waiting for command')
                        audio = self.recognizer.listen(source)

                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()

                        if text == ASSISTANT_STOP:
                            self.voice.say('Goodbye!')
                            self.voice.runAndWait()
                            self.voice.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                try:
                                    data = self.load_responses(INPUT_OUTPUT)
                                    voice = self.find_response(text, data)
                                    if voice:
                                        self.voice.say(voice)
                                        self.voice.runAndWait()
                                    else:
                                        self.voice.say('I\'m sorry, I don\'t understand')
                                        self.voice.runAndWait()
                                except FileNotFoundError:
                                    self.voice.say(f'Couldn\'t find {INPUT_OUTPUT} file')
                                    self.voice.runAndWait()
                            self.label.config(text = 'Listening')
            except:
                self.label.config(text = f'Listening, ({ASSISTANT_COMMAND} to start)')
                continue

GameAssistant()