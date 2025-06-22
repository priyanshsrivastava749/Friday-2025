import eel
import time
from multiprocessing import Process, Queue
import Backend.main as main

def trigger_ui_update_listen_text(command):
    eel.updateListenText("🎤 Friday is listening...")

def friday_main(queue: Queue):
    main.speak("INITIALIZING FRIDAY")
    while True:
        print("🕵️ Listening for wake word...")
        command = main.listen(2,1)
        if 'friday' in command.lower():
            main.speak("Yes Boss")
            queue.put("show_listen")  # 💡 Send command to UI thread
            command = main.listen(6,3) 
            main.processCommand(command)
            queue.put("show_home")
        time.sleep(1)

def start_ui(queue: Queue):
    eel.init('Frontend')
    eel.start('index.html', size=(500, 400), block=False)
    # 👂 Listen to messages from backend
    while True:
        try:
            msg = queue.get_nowait()
            if msg == "show_listen":
                eel.showSection("Listen")
            elif msg == "show_home":
                eel.showSection("Home")  # ✅ Call exposed JS function
        except:
            pass
        eel.sleep(0.1)

if __name__ == '__main__':
    q = Queue()

    # Step 1: Start frontend UI (with queue listener)
    ui_process = Process(target=start_ui, args=(q,))
    ui_process.start()

    # Step 2: Run FRIDAY logic in another process
    backend_process = Process(target=friday_main, args=(q,))
    backend_process.start()

    # Optional: Join processes if needed
    ui_process.join()
    backend_process.join()
