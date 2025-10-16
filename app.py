import uvicorn
import webbrowser
import threading
import time

def open_docs():
    time.sleep(1.5)
    webbrowser.open_new("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    threading.Thread(target=open_docs).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
