import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import cv2
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")    
    else:
        speak("Good Evening!")
    speak("Ready To Comply. What can I do for you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

def writeInNotepad(content):
    pyautogui.typewrite(content)

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "channel analytics" in query:
            webbrowser.open("https://studio.youtube.com/channel/UCxeYbp9rU_HuIwVcuHvK0pw/analytics/tab-overview/period-default")

        elif 'search on youtube' in query:
            speak("What should I search on YouTube?")
            search_query = takeCommand().lower()
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif 'open youtube' in query:
            speak("What you will like to watch?")
            qrry = takeCommand().lower()
            kit.playonyt(f"{qrry}")
            

        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")

        elif 'close youtube' in query:
            os.system("taskkill /f /im msedge.exe")

        elif 'open google' in query:
            speak("What should I search?")
            search_query = takeCommand().lower()
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open_new_tab(f"https://www.google.com/search?q={search_query}")

        elif 'close google' in query:
            os.system("taskkill /f /im msedge.exe")

        elif 'play music' in query:
            music_dir = 'E:\\Musics'
            songs = os.listdir(music_dir)    
            os.startfile(os.path.join(music_dir, random.choice(songs)))

        elif 'play iron man movie' in query:
            npath = "E:\\ironman.mkv"    
            os.startfile(npath)

        elif 'close movie' in query:
            os.system("taskkill /f /im vlc.exe")

        elif 'close music' in query:
            os.system("taskkill /f /im vlc.exe")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        elif "restart the system" in query:
            os.system("shutdown /r /t 5")

        elif "lock the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "open notepad" in query:
            os.startfile("notepad.exe")
            time.sleep(2)
            speak("Are you going to write or dictate?")
            action = takeCommand().lower()
            if 'yourself' in action:
                speak("What should I write?")
                note = takeCommand().lower()
                writeInNotepad(note)
            elif 'write' in action:
                speak("You can start writing now.")

        elif "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")

        elif "open camera" in query:
            camera_on = True
            cap = cv2.VideoCapture(0)
            speak("Camera is now on.")
            while camera_on:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):  
                    break
                query = takeCommand().lower()  
                if "close camera" in query:
                    camera_on = False
                    speak("Closing the camera.")
            cap.release()
            cv2.destroyAllWindows()


        elif "go to sleep" in query:
            speak('Alright then, I am switching off')
            sys.exit()

        elif "take screenshot" in query:
            speak('Tell me a name for the file')
            name = takeCommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()  
            img.save(f"{name}.png")  
            speak("Screenshot saved")

        elif "calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Ready")
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                    '+' : operator.add,
                    '-' : operator.sub,
                    'x' : operator.mul,
                    'divided' : operator.__truediv__,
                }[op]
            def eval_bianary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak("Your result is")
            speak(eval_bianary_expr(*(my_string.split())))

        elif "what is my ip address" in query:
            speak("Checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak("Your IP address is")
                speak(ipAdd)
            except Exception as e:
                speak("Network is weak, please try again some time later")

        elif "volume up" in query:
            for _ in range(15):
                pyautogui.press("volumeup")

        elif "volume down" in query:
            for _ in range(15):
                pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif "refresh" in query:
            pyautogui.moveTo(1620, 667)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'r')

        elif "right click" in query:
            pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='right')

        elif "left click" in query:
            pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')

        elif "open teams" in query:
            npath = "C:\\Users\\Nitish Singla\\AppData\\Local\\Microsoft\\Teams\\Update.exe"    
            os.startfile(npath)

        elif "close teams" in query:
            os.system("taskkill /f /im Teams.exe")

        elif "open excel" in query:
            npath = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(npath)

        elif "close excel" in query:
            os.system("taskkill /f /im excel.exe")

        elif "open word" in query:
            npath = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(npath)

        elif "close word" in query:
            os.system("taskkill /f /im WINWORD.EXE")

        elif "open edge" in query:
            npath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"    
            os.startfile(npath)

        elif "close edge" in query:
            os.system("taskkill /f /im msedge.exe")

        elif "close all windows" in query:
            pyautogui.hotkey('alt', 'f4')

        elif "sleep" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "hibernate" in query:
            os.system("shutdown /h")

        elif "switch window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "close the browser" in query:
            os.system("taskkill /f /im msedge.exe")

        

       

        elif "shutdown" in query:
            speak("Are you sure you want to shut down?")
            ans = takeCommand().lower()
            if 'yes' in ans:
                os.system("shutdown /s /t 5")
            else:
                break

        elif "restart" in query:
            speak("Are you sure you want to restart?")
            ans = takeCommand().lower()
            if 'yes' in ans:
                os.system("shutdown /r /t 5")
            else:
                break

        elif "log out" in query:
            speak("Are you sure you want to log out?")
            ans = takeCommand().lower()
            if 'yes' in ans:
                os.system("shutdown -l")
            else:
                break

        elif "goodbye" in query:
            speak("Goodbye! Have a nice day.")
            sys.exit()

        elif 'open whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com")
        
        elif 'open spotify' in query:
            webbrowser.open("https://open.spotify.com")
        
        elif 'open linkedin' in query:
            webbrowser.open("https://www.linkedin.com")
        
        elif 'open gmail' in query:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        
        elif 'write mail' in query:
            speak("Opening Gmail to compose a new mail.")
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")
            time.sleep(5) 
            speak("Who is the recipient?")
            recipient = takeCommand().lower()
            pyautogui.typewrite(recipient)
            pyautogui.press("tab")
            speak("What should be the subject?")
            subject = takeCommand().lower()
            pyautogui.typewrite(subject)
            pyautogui.press("tab")
            speak("What should be the body of the email?")
            body = takeCommand().lower()
            pyautogui.typewrite(body)
            pyautogui.hotkey("ctrl", "enter")
            speak("Email has been sent.")
