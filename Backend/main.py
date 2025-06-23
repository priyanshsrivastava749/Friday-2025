import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import subprocess
import time
import re

music = {
  "kela":"https://youtu.be/S0Ty4T5vXz4?si=ODixYUj_kg_m9P71",
  "sleepwalker":"https://youtu.be/ABDwY3ush_Y?si=SIAt6LXJWPa22YlT",
  "skins":"https://youtu.be/Hs8rhoaixU4?si=phXSWS_M7kGWSfbI",
  "government":"https://youtu.be/yBwYaXHhuNg?si=KliEaOo9z96IljmY",
  "sorry":"https://youtu.be/skaKitbOxrA?si=hpp1VK_1oFGMgnXK"
}


question = ["what","how","when","where","tell me","can you","why","who"]
engine = pyttsx3.init()
newsapi = "44c6abf73f304d4c9e8297817de4834c"
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(text):
  engine.say(text) 
  engine.runAndWait()

def listen(timeout,timelimit):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=timelimit)
            command = r.recognize_google(audio, language='en-US')
            print(f"User said: {command}")
            return command
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase.")
        return "Timeout"
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "Unrecognized"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "Error"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error"
    
def clear_response(statement):
     return re.sub(r"[*_`]+", "", statement)

def ask_local_llm(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.2:latest",  # change this if you installed another model like deepseek
        "prompt": prompt,
        "stream": False     # stream False means full response in one go
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return "Sorry bhai, model se response nahi aaya."
    except Exception as e:
        return f"LLM error: {e}"
    

def close_process_with_grace(process_name, wait_seconds=5):
    # Step 1: Gracefully close (taskkill without /F)
    subprocess.run(["taskkill", "/IM", process_name], shell=True)
    print(f"Sent close signal to {process_name}, waiting {wait_seconds} seconds...")

    # Step 2: Wait for process to close
    time.sleep(wait_seconds)

    # Step 3: Force kill (taskkill with /F)
    # This will ensure process is terminated if still running
    subprocess.run(["taskkill", "/F", "/IM", process_name], shell=True)
    print(f"Force kill command sent to {process_name} (if still running).")



def processCommand(command):
    print(command)
    if("open google"in command.lower()):
        webbrowser.open("https://google.com")
        return f"opening {command.split(' ')[1]}"
    elif("open facebook" in command.lower()):
        webbrowser.open("https://facebook.com")
        return f"opening {command.split(' ')[1]}"
    elif("open chat gpt" in command.lower()):
        webbrowser.open("https://chatgpt.com/")
        return f"opening {command.split(' ')[1]}" 
    elif("open github"  in command.lower()):
        webbrowser.open("https://github.com")
        return f"opening {command.split(' ')[1]}"
    elif("open linkedin"in command.lower()):
        webbrowser.open("https://linkedin.com")
        return f"opening {command.split(' ')[1]}"
    elif("open youtube"in command.lower()):
        webbrowser.open("https://youtube.com")
        return f"opening {command.split(' ')[1]}"
    elif("open portfolio"in command.lower()):
        webbrowser.open_new_tab("https://helpful-elf-967c0f.netlify.app/")
        return f"opening your {command.split(' ')[1]}"
    elif("open whatsapp"in command.lower()):
        subprocess.run(["start", "whatsapp:"], shell=True)
        return f"opening your {command.split(' ')[1]}"
    elif("close browser"in command.lower()):
        close_process_with_grace("brave.exe", wait_seconds=5)
        return f"closing {command.split(' ')[1]}"
    elif("close whatsapp"in command.lower()):
        close_process_with_grace("WhatsApp.exe", wait_seconds=5)
        return f"closing {command.split(' ')[1]}"
    elif command.lower().startswith("play"):
         try:
            song = command.lower().split(' ')[1]
            link = music[song]
            webbrowser.open(link)
            return f"playing {song}"
         except KeyError:
             return "Sorry sir,I Dont have this song in my library"
    elif "news" in command.lower():
        r =  requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                speak(article['title']) 
    else:
        command_lower = command.lower()
        for word in question:
            if word in command_lower:
                print("control is in the else block of the process command")
                answer = ask_local_llm(command)
                speak(clear_response(answer))
      
        