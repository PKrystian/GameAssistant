import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import subprocess

def listen_for_commands():
    def start_listening():
        recognizer = sr.Recognizer()
        recognized_text = ''
        last_command = ''
        while True:
            output_text.set(recognized_text)
            if recognized_text != None:
                last_command = recognized_text
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration = 0.5)
                audio = recognizer.listen(source, phrase_time_limit = 2)
            try:
                recognized_text = recognizer.recognize_google(audio)
                if recognized_text:
                    if 'say hello' in recognized_text.lower():
                        text_to_voice('hello!')
                    if 'set day' in recognized_text.lower():
                        text_to_voice('time set to day')
                    if 'open code' in recognized_text.lower():
                        text_to_voice('opening vscode, enjoy coding')
                        try:
                            subprocess.run(['code'])
                        except FileNotFoundError:
                            text_to_voice('Program VScode wasn\'t found')
            except sr.UnknownValueError:
                output_text.set('could not understand audio.')
            except sr.RequestError as e:
                output_text.set(f'error occurred during recognition: {e}')

    threading.Thread(target=start_listening).start()

def text_to_voice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

root = tk.Tk()
root.title('Game Assistant V2')
root.geometry('900x600')

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text)
output_label.pack(pady = 10)

record_button = tk.Button(root, text='Start Listening', command=listen_for_commands)
record_button.pack(pady = 20)

root.mainloop()
