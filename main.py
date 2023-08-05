import sys
import threading
import tkinter as tk
import pyttsx3 as tts
import speech_recognition as sr

ASSISTANT_NAME = 'circle'
ASSISTANT_COMMAND = f'hey {ASSISTANT_NAME}'
ASSISTANT_STOP = 'stop'

class GameAssistant:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.voice = tts.init()
        self.voice.setProperty('rate', 200)

        self.root = tk.Tk()
        self.root.title('Game Assistant V3')
        self.root.geometry('900x600')
        self.label = tk.Label(text = f'Listening ({ASSISTANT_COMMAND} to start)')
        self.label.pack()

        threading.Thread(target = self.game_assistant_init).start()

        self.root.mainloop()

    def game_assistant_init(self) -> None:
        while True:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration = 0.2)
                    audio = self.recognizer.listen(source)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

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
                                self.voice.say('TODO: text.json here')
                                self.voice.runAndWait()
                            self.label.config(text = 'Listening')
            except:
                self.label.config(text = f'Listening ({ASSISTANT_COMMAND} to start)')
                continue

GameAssistant()