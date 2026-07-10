from datetime import datetime

import speech_recognition as sr
import webbrowser
import tempfile
import pygame
import os
import time
import random 
# import wikipedia
from gtts import gTTS
# import pyttsx3
import musiclib

pygame.mixer.init()

recognizer = sr.Recognizer()
# engine = pyttsx3.init()

responses = ["Yes?","I'm listening.","How can I help?","Go ahead."]

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        path = fp.name
        tts.save(path)

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.music.unload()
    os.remove(path)
    
    # engine.say(text)
    # engine.runAndWait()
    
def processcommand(c):
    c = c.lower()
    
    if "open youtube" in c:
        speak("Opening Youtube..")
        webbrowser.open("https://www.youtube.com")
        
    elif "open google" in c:
        speak("opening google...")
        webbrowser.open("https://www.google.com")
        
    elif "play" in c:   
        song = c.replace("play", "").strip()
        speak("Playing " + song)
        if song in musiclib.music:
            webbrowser.open(musiclib.music[song])
        else:
            speak("Song not found.")   
    elif "time" in c:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    
    elif "date" in c or "today" in c:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}")
        
    elif "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
        
    elif "open whatsapp" in c:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")
        
    elif "open command prompt" in c:
        speak("Opening Command Prompt")
        os.system("start cmd")
        
    elif "search google for" in c:
        query = c.replace("search google for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        
    elif "exit" in c or "goodbye" in c or "stop" in c:
        speak("Goodbye! Have a nice day.")
        exit()
        
    # elif "who is" in c:
    #     person = c.replace("who is", "").strip()
    #     result = wikipedia.summary(person, sentences=2)
    #     speak(result)
    
    else:
        speak("Sorry, I don't know that command yet.")

if __name__ =="__main__":
    speak("Initializing Jarvis...")
    
    while True:
        
           
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(source, timeout = 5, phrase_time_limit = 5.5)
                word = recognizer.recognize_google(audio)
            
            
            if "jarvis" in word.lower():
                speak(random.choice(responses))
                
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio2 = recognizer.listen(source)
                    command = recognizer.recognize_google(audio2)
                    print(f"Your command is: {command}")
                    
                    processcommand(command)
                    
                    
        
        except sr.UnknownValueError:
            speak("Couldn't understand.")

        except sr.WaitTimeoutError:
            speak("Listening timed out.")

        except Exception as e:
            print(e)