import json
import speech_recognition as sr
import pyttsx3
import random
from fuzzywuzzy import fuzz

with open('/Users/abhinavtadiparthi/Desktop/PYTHON AI ML/Wakeword2/responses.json', 'r') as file:
    intents = json.load(file)


engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


recognizer = sr.Recognizer()


def wait_for_wake_word():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  
        print("Waiting for the wake word 'Lucifer'...")
        while True:  
            try:
                audio = recognizer.listen(source, timeout=5)  
                wake_word_command = recognizer.recognize_google(audio).lower()  
                print(f"Recognized wake word attempt: {wake_word_command}")
                return wake_word_command
            except sr.UnknownValueError:
                print("Did not recognize the wake word. Listening again...")
                continue  
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue 
            except sr.WaitTimeoutError:
                print("Listening timed out. Continuing to listen...")
                continue  


def recognize_command():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5)  
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except sr.WaitTimeoutError:
            print("Command listening timed out.")
            return None


def get_response(command):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if fuzz.ratio(pattern.lower(), command.lower()) > 80:  
                return random.choice(intent['responses'])
    return "Sorry, I don't have an answer for that."


def is_wake_word_detected(phrase):
    return fuzz.ratio(phrase.lower(), "lucifer") > 80


def main():
    while True:
        
        wake_word_command = wait_for_wake_word()

        
        if wake_word_command and is_wake_word_detected(wake_word_command):
            print("Wake word 'Lucifer' detected.")
            speak("Hi, I'm listening...") 

            
            while True:  
                command = recognize_command()

                if command:
                    
                    response_command = command.replace("lucifer", "").strip()

                    
                    response = get_response(response_command)
                    print(f"Response: {response}")
                    speak(response)

                else:
                    print("Returning to wake word listening mode...")
                    break  

if __name__ == "__main__":
    main()


