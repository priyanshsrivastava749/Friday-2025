import eel
import time
from multiprocessing import Process
import Backend.main as main

def trigger_ui_update_listen_text(command):
    eel.updateListenText("🎤 Friday is listening...")

def friday_main():
    main.speak("INITIALIZING FRIDAY")
    while True:
        print("🕵️ Listening for wake word...")
        command = main.listen(2,1)
        if 'friday' in command.lower():
            main.speak("Yes Boss")
            command = main.listen(6,3)
            main.processCommand(command)
        time.sleep(1)

def start_ui():
    eel.init('Frontend')
    eel.start('index.html', size=(500, 400), block=False)



if __name__ == '__main__':
    # Step 1: Start UI first
    start_ui()

    # Step 2: Run Friday in separate process
    p = Process(target=friday_main, daemon=True)
    p.start()

    # Step 3: Keep app running
    while True:
        eel.sleep(1)
