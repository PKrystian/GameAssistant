import sys
import json
import threading
import tkinter as tk
import pyttsx3 as tts
import speech_recognition as sr

class Response:
    def __init__(self, input_text, output_text):
        self.input_text = input_text
        self.output_text = output_text

class GameAssistant:
    def __init__(self):
        self.assistant_name = 'alpha'
        self.assistant_command = f'hey {self.assistant_name}'
        self.assistant_stop = 'stop'
        self.input_output = 'text.json'

        self.recognizer = sr.Recognizer()
        self.voice = tts.init()
        self.voice.setProperty('rate', 100)

        self.root = tk.Tk()
        self.root.title('Game Assistant V3')
        self.root.geometry('900x600')
        self.label = tk.Label(text=f'Listening ({self.assistant_command} to start)')
        self.label.pack()

        threading.Thread(target=self.game_assistant_init).start()

        self.root.mainloop()

    def load_responses(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return [Response(item['input'], item['output']) for item in data['text']]

    def find_response(self, text, responses):
        for response in responses:
            if response.input_text in text:
                return response.output_text
        return None

    def handle_response(self, text, responses):
        if text is not None:
            try:
                voice = self.find_response(text, responses)
                if voice:
                    self.voice.say(voice)
                    self.voice.runAndWait()
                else:
                    self.voice.say("I'm sorry, I don't understand")
                    self.voice.runAndWait()
            except Exception as e:
                self.voice.say(f"An error occurred: {e}")
                self.voice.runAndWait()

    def game_assistant_init(self):
        while True:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.recognizer.listen(source)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    self.label.config(text=text)  # Uncomment for testing

                    if self.assistant_command in text:
                        self.label.config(text='Waiting for command')
                        audio = self.recognizer.listen(source)

                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()

                        if text == self.assistant_stop:
                            self.voice.say('Goodbye!')
                            self.voice.runAndWait()
                            self.voice.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            try:
                                responses = self.load_responses(self.input_output)
                                self.handle_response(text, responses)
                            except FileNotFoundError:
                                self.voice.say(f"Couldn't find {self.input_output} file")
                                self.voice.runAndWait()
                            except Exception as e:
                                self.voice.say(f"An error occurred: {e}")
                                self.voice.runAndWait()
                            self.label.config(text='Listening')
            except sr.UnknownValueError:
                self.label.config(text="Sorry, I didn't catch that. Could you please repeat?")
            except sr.RequestError as e:
                self.label.config(text=f"Sorry, there was an issue with the speech recognition service: {e}")
            except Exception as e:
                self.label.config(text=f"An error occurred: {e}")
                continue

if __name__ == "__main__":
    GameAssistant()
