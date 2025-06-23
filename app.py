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
            queue.put("show_listen")
            queue.put({ "type": "text_update", "text": "🎤 Friday is listening...", "hold": 4000 })# 💡 Send command to UI thread
            command = main.listen(6,3)
            word_count = len(command.split())
            estimated_time = word_count / 1.5
            print(f"estimated time  to the given command is {estimated_time} seconds")
            print(f"📝 Sending to JS: {command}")
            queue.put({ "type": "text_update", "text": command, "hold": estimated_time })
            result = main.processCommand(command)
            if not result:
               result = "Sorry, no response received."
            word_count = len(result.split())
            estimated_time = word_count / 1.5
            print(f"estimated time is {estimated_time} seconds")
            queue.put({ "type": "text_update", "text": result, "hold": estimated_time })
            time.sleep(estimated_time+1)
            if(result != "Sorry, no response received."):
                main.speak(result)
            queue.put("show_home")
        time.sleep(1)

def start_ui(queue: Queue):
    eel.init('Frontend')
    eel.start('index.html', size=(500, 400), block=False)

    # ✅ Wait for JS to be ready
    time.sleep(2)  # JS needs time to load eel.expose()

    print("✅ UI Loop Started - Waiting for Messages...")

    while True:
        try:
            msg = queue.get_nowait()
            if msg == "show_listen":
                eel.showSection("Listen")
            elif msg == "show_home":
                eel.showSection("Home")
            # elif isinstance(msg, str):
            #     print(f"📨 UI got text to update: {msg}")
            #     eel.updateListenText(msg)
            elif isinstance(msg, dict) and msg.get("type") == "text_update":
                text = msg.get("text", "")
                hold = msg.get("hold", 5000)
                print(f"📨 Dict message: {text} | Hold: {hold}")
                eel.updateListenText(text, hold)
            elif isinstance(msg, str):
                print(f"📨 String message: {msg}")
                eel.updateListenText(msg)  # fallback default 5 sec

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

