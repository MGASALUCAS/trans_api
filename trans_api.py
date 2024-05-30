import threading
import time

transcription = ""
transcription_lock = threading.Lock()

def save_transcription_periodically(socketio):
    while True:
        time.sleep(30)  # Wait for 30 seconds
        with transcription_lock:
            if transcription:
                # Save transcription to a text file
                with open("transcription.txt", "a") as f:
                    f.write(transcription + "\n")
                
                # Emit the transcription to the student page
                socketio.emit('update_transcription', {'text': transcription}, broadcast=True)
                
                # Clear the current transcription
                transcription = ""

def start_background_thread(socketio):
    thread = threading.Thread(target=save_transcription_periodically, args=(socketio,))
    thread.daemon = True
    thread.start()
