import speech_recognition as sr

def listen_for_commands():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("listening")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, phrase_time_limit=2)

        try:
            recognized_text = recognizer.recognize_google(audio)
            if recognized_text:
                print("you said:", recognized_text)

                if "say hello" in recognized_text.lower():
                    print("hello!")

        except sr.UnknownValueError:
            print("could not understand audio.")
        except sr.RequestError as e:
            print(f"error occurred during recognition: {e}")

if __name__ == "__main__":
    listen_for_commands()
