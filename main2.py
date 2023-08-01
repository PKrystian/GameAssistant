import tkinter as tk
import threading
import speech_recognition as sr

def listen_for_commands():
    def start_listening():
        recognizer = sr.Recognizer()
        recognized_text = ''
        while True:
            with sr.Microphone() as source:
                output_text.set(recognized_text)
                recognizer.adjust_for_ambient_noise(source, duration = 0.5)
                audio = recognizer.listen(source, phrase_time_limit = 2)

            try:
                recognized_text = recognizer.recognize_google(audio)
                if recognized_text:
                    if 'say hello' in recognized_text.lower():
                        output_text.set('hello!')
                    if 'set day' in recognized_text.lower():
                        output_text.set('time set to day')

            except sr.UnknownValueError:
                output_text.set('could not understand audio.')
            except sr.RequestError as e:
                output_text.set(f'error occurred during recognition: {e}')

    threading.Thread(target=start_listening).start()

root = tk.Tk()
root.title('Game Assistant V2')
root.geometry('900x600')

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text)
output_label.pack(pady = 10)

record_button = tk.Button(root, text='Start Listening', command=listen_for_commands)
record_button.pack(pady = 20)

root.mainloop()
