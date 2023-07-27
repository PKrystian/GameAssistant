import tkinter as tk
import speech_recognition as sr

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        output_text.set("Recorded: " + text)
        print("Recorded: ", text)
    except sr.UnknownValueError:
        output_text.set("Could not understand audio")
        print("Could not understand audio")
    except sr.RequestError as e:
        output_text.set("Error during transcription: {0}".format(e))
        print("Error during transcription: {0}".format(e))

root = tk.Tk()
root.title("Game Assistant v1")
root.geometry("600x400")

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text)
output_label.pack(pady=10)

record_button = tk.Button(root, text="Record Audio", command=record_audio)
record_button.pack(pady=20)

root.mainloop()
