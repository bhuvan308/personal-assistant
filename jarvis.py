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
from typing import Optional

class VoiceAssistant:
    def __init__(self):
        # Initialize TTS engine
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Paths (update these according to your system)
        self.music_dir = 'E:\\Musics'
        self.movie_path = "E:\\ironman.mkv"
        
    def speak(self, audio: str) -> None:
        """Convert text to speech"""
        try:
            self.engine.say(audio)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech: {e}")
    
    def wish_me(self) -> None:
        """Greet user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("Ready To Comply. What can I do for you?")
    
    def take_command(self) -> str:
        """Listen to user voice and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.pause_threshold = 1
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except sr.WaitTimeoutError:
            print("Listening timeout")
            return "None"
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "None"
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return "None"
        except Exception as e:
            print(f"Error: {e}")
            return "None"
    
    def write_in_notepad(self, content: str) -> None:
        """Type content in notepad"""
        try:
            pyautogui.typewrite(content)
        except Exception as e:
            print(f"Error writing in notepad: {e}")
    
    def search_wikipedia(self, query: str) -> None:
        """Search Wikipedia and speak results"""
        try:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            print(results)
            self.speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"Multiple results found. Being more specific: {e.options[0]}")
            results = wikipedia.summary(e.options[0], sentences=2)
            print(results)
            self.speak(results)
        except wikipedia.exceptions.PageError:
            self.speak("No Wikipedia page found for this query")
        except Exception as e:
            self.speak("Sorry, I couldn't fetch information from Wikipedia")
            print(f"Wikipedia error: {e}")
    
    def open_camera(self) -> None:
        """Open camera with voice control"""
        try:
            camera_on = True
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                self.speak("Cannot open camera")
                return
                
            self.speak("Camera is now on. Say 'close camera' to stop.")
            
            while camera_on:
                ret, img = cap.read()
                if not ret:
                    break
                    
                cv2.imshow('webcam', img)
                
                # Check for 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # Non-blocking command check
                try:
                    with sr.Microphone() as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                        audio = self.recognizer.listen(source, timeout=0.1, phrase_time_limit=2)
                        query = self.recognizer.recognize_google(audio).lower()
                        if "close camera" in query:
                            camera_on = False
                            self.speak("Closing the camera.")
                except:
                    pass  # Continue if no voice command
            
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            self.speak("Error with camera")
            print(f"Camera error: {e}")
    
    def calculate(self) -> None:
        """Perform basic calculations"""
        try:
            with sr.Microphone() as source:
                self.speak("Say your calculation. For example: 5 plus 3")
                print("Listening for calculation...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            calculation = self.recognizer.recognize_google(audio).lower()
            print(f"Calculation: {calculation}")
            
            # Simple calculation parser
            calculation = calculation.replace("plus", "+").replace("add", "+")
            calculation = calculation.replace("minus", "-").replace("subtract", "-")
            calculation = calculation.replace("times", "*").replace("multiply", "*")
            calculation = calculation.replace("divided by", "/").replace("divide", "/")
            
            try:
                result = eval(calculation)
                self.speak(f"The result is {result}")
                print(f"Result: {result}")
            except:
                self.speak("Sorry, I couldn't calculate that. Please use simple operations.")
        except Exception as e:
            self.speak("Error in calculation")
            print(f"Calculation error: {e}")
    
    def get_ip_address(self) -> None:
        """Get public IP address"""
        try:
            self.speak("Checking your IP address")
            response = requests.get('https://api.ipify.org', timeout=5)
            ip_address = response.text
            print(f"IP Address: {ip_address}")
            self.speak(f"Your IP address is {ip_address}")
        except requests.RequestException:
            self.speak("Network error. Please check your internet connection.")
        except Exception as e:
            self.speak("Error getting IP address")
            print(f"IP error: {e}")
    
    def take_screenshot(self) -> None:
        """Take screenshot with custom name"""
        try:
            self.speak('Tell me a name for the screenshot')
            name = self.take_command().lower()
            if name != "None":
                time.sleep(2)
                screenshot = pyautogui.screenshot()
                filename = f"{name}.png"
                screenshot.save(filename)
                self.speak(f"Screenshot saved as {filename}")
            else:
                self.speak("No name provided. Screenshot not taken.")
        except Exception as e:
            self.speak("Error taking screenshot")
            print(f"Screenshot error: {e}")
    
    def run(self) -> None:
        """Main loop for voice assistant"""
        self.wish_me()
        
        while True:
            query = self.take_command().lower()
            
            if query == "none":
                continue
            
            try:
                if 'wikipedia' in query:
                    self.search_wikipedia(query)
                
                elif "channel analytics" in query:
                    webbrowser.open("https://studio.youtube.com/channel/UCxeYbp9rU_HuIwVcuHvK0pw/analytics/tab-overview/period-default")
                
                elif 'search on youtube' in query:
                    self.speak("What should I search on YouTube?")
                    search_query = self.take_command()
                    if search_query != "None":
                        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                
                elif 'open youtube' in query:
                    self.speak("What would you like to watch?")
                    video_query = self.take_command()
                    if video_query != "None":
                        kit.playonyt(video_query)
                
                elif 'open google' in query:
                    self.speak("What should I search?")
                    search_query = self.take_command()
                    if search_query != "None":
                        webbrowser.open(f"https://www.google.com/search?q={search_query}")
                
                elif 'play music' in query:
                    if os.path.exists(self.music_dir):
                        songs = os.listdir(self.music_dir)
                        if songs:
                            random_song = random.choice(songs)
                            os.startfile(os.path.join(self.music_dir, random_song))
                            self.speak("Playing music")
                        else:
                            self.speak("No songs found in music directory")
                    else:
                        self.speak("Music directory not found")
                
                elif 'play iron man movie' in query:
                    if os.path.exists(self.movie_path):
                        os.startfile(self.movie_path)
                        self.speak("Playing Iron Man movie")
                    else:
                        self.speak("Movie file not found")
                
                elif 'time' in query:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    self.speak(f"The time is {current_time}")
                
                elif "open notepad" in query:
                    os.startfile("notepad.exe")
                    time.sleep(2)
                    self.speak("Notepad opened. You can start typing.")
                
                elif "open command prompt" in query:
                    os.system("start cmd")
                    self.speak("Command prompt opened")
                
                elif "open camera" in query:
                    self.open_camera()
                
                elif "take screenshot" in query:
                    self.take_screenshot()
                
                elif "calculate" in query:
                    self.calculate()
                
                elif "ip address" in query:
                    self.get_ip_address()
                
                elif "volume up" in query:
                    for _ in range(5):
                        pyautogui.press("volumeup")
                    self.speak("Volume increased")
                
                elif "volume down" in query:
                    for _ in range(5):
                        pyautogui.press("volumedown")
                    self.speak("Volume decreased")
                
                elif "mute" in query:
                    pyautogui.press("volumemute")
                    self.speak("Volume muted")
                
                elif 'open whatsapp' in query:
                    webbrowser.open("https://web.whatsapp.com")
                    self.speak("Opening WhatsApp")
                
                elif 'open spotify' in query:
                    webbrowser.open("https://open.spotify.com")
                    self.speak("Opening Spotify")
                
                elif 'open linkedin' in query:
                    webbrowser.open("https://www.linkedin.com")
                    self.speak("Opening LinkedIn")
                
                elif 'open gmail' in query:
                    webbrowser.open("https://mail.google.com")
                    self.speak("Opening Gmail")
                
                elif "shutdown" in query:
                    self.speak("Are you sure you want to shutdown?")
                    confirm = self.take_command().lower()
                    if 'yes' in confirm:
                        os.system("shutdown /s /t 5")
                    else:
                        self.speak("Shutdown cancelled")
                
                elif "restart" in query:
                    self.speak("Are you sure you want to restart?")
                    confirm = self.take_command().lower()
                    if 'yes' in confirm:
                        os.system("shutdown /r /t 5")
                    else:
                        self.speak("Restart cancelled")
                
                elif "sleep" in query:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    self.speak("System going to sleep")
                
                elif any(word in query for word in ["goodbye", "exit", "quit", "go to sleep"]):
                    self.speak("Goodbye! Have a nice day.")
                    break
                
                else:
                    self.speak("I didn't understand that command. Please try again.")
            
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                self.speak("An error occurred. Please try again.")
                print(f"Error: {e}")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()