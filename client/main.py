import customtkinter as ctk
from keylogger import Keylogger
import requests
import json
import threading

class App:
    keylogger = None
    userId = None
    userSessionId = None
    
    def __init__(self, master:ctk.CTk):
        self.master = master
        self.master.geometry('400x350')
        self.master.resizable(False,False)
        self.master.wm_title('Keydo')
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        
        self.mainlabel = ctk.CTkLabel(self.master, text='Keydo')
        self.mainlabel.pack(pady=20)
        
        self.frame = ctk.CTkFrame(master=master)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        self.label = ctk.CTkLabel(master=self.frame, text='Sign in')
        self.label.pack(pady=12,padx=10)
        
        self.user_email = ctk.CTkEntry(master=self.frame, placeholder_text = "Email")
        self.user_email.pack(pady=12,padx=10)
        
        self.user_pass = ctk.CTkEntry(master=self.frame, placeholder_text = "Password", show="*")
        self.user_pass.pack(pady=12,padx=10)
        
        self.button = ctk.CTkButton(master=self.frame, text = "Login", command = self.login)
        self.button.pack(pady=12,padx=10)
    
    def exit(self):
        print("Exiting...")
        if self.keylogger is not None:
            if self.keylogger.running:
                self.keylogger.stop()
        self.master.quit()
        
    
    def login(self):
        url = 'http://localhost:8000/api/user/login/'
        headers = {
            "Content-Type": "application/json"
        }
        credentials = {
            "email": str(self.user_email.get()),
            "password":str(self.user_pass.get())
        }
        
        self.session = requests.Session()
        App.userSessionId = self.session
        response = self.session.post(url, data=json.dumps(credentials), headers=headers)
        
        if response.status_code != 200 :
            self.label = ctk.CTkLabel(master=self.frame, text='Something went wrong', text_color='red')
            self.label.pack(pady=0,padx=10)
        else:
            self.frame.destroy()
            self.mainlabel.configure(text='Welcome to Keydo')
            self.__authToken = response.json().get('jwt token', '')  # Safely get the token, default to empty string if not found
            self.initiate()
    
    def initiate(self):
        self.master.geometry('750x600')
        
        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        terms_text = (
            "Terms and Conditions:\n\n\n"
            "1. This is a keylogger service that once enabled will track every key that you type.\n\n"
            "2. Please be careful about the sensitive data that you type. \n\n  We recommend avoiding entering very confidential information if you are not comfortable.\n\n"
            "3. You have the right to delete your data at any time.\n\n  To request data deletion, please send an email to up1066442@upnet.gr.\n\n"
            "4. Your data is encrypted and kept safe on a fully secure server and database.\n\n  We take every measure to ensure the security and privacy of your information.\n\n"
            "5. Regardless of your request in data deletion, all your data will be erased after 6 months."
            "\n\n\n By clicking ON button you are accepting the above"
        )
        
        self.termsLabel = ctk.CTkLabel(master=self.frame, 
                                    text=terms_text,
                                    justify=ctk.LEFT)
        self.termsLabel.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.stopButton = ctk.CTkButton(master=self.frame, 
                                        text='OFF',
                                        width=50,
                                        height=50,
                                        corner_radius=5, 
                                        fg_color='transparent', 
                                        border_width=2,
                                        border_color='#ffffff',
                                        hover_color='#e81202', 
                                        command=self.stop)
        self.stopButton.pack(pady=12, padx=10, side=ctk.LEFT)
        
        self.startButton = ctk.CTkButton(master=self.frame, 
                                        text='ON',
                                        width=50,
                                        height=50,
                                        corner_radius=5, 
                                        fg_color='transparent',
                                        border_width=2,
                                        border_color='#ffffff', 
                                        hover_color='#02cf5b',
                                        command=self.start)
        self.startButton.pack(pady=12, padx=10, side=ctk.RIGHT)
    
    def start(self):
        self.startButton.configure(fg_color='#02cf5b')
        self.stopButton.configure(fg_color='transparent')
        url = 'http://localhost:8000/api/user/'
        # headers = {
        #     "Content-Type": "application/json",
        #     "Authorization": f"Bearer {self.__authToken}"
        # }
        response = self.session.get(url)
        if response.status_code != 200 :
            return
        App.userId = response.json().get('id')
        if not keylogger_thread.is_alive():
            keylogger_thread.start()
        
        # if self.keylogger:
        #     self.keylogger.start(userId=self.userId, userSessionId = self.session)
    
    def stop(self):
        self.startButton.configure(fg_color='transparent')
        self.stopButton.configure(fg_color='#e81202')
        if self.keylogger:
            self.keylogger.stop()

def start_gui():
    app = ctk.CTk()
    gui = App(master=app)
    app.mainloop()

def start_keylogger():
    App.keylogger = Keylogger("http://localhost:8000/api/v1/keystrokes/add/")
    App.keylogger.start(App.userId,App.userSessionId)

if __name__ == '__main__':
    gui_thread = threading.Thread(target=start_gui)
    keylogger_thread = threading.Thread(target=start_keylogger)
    
    gui_thread.start()
    gui_thread.join()
    
    if keylogger_thread.is_alive():
        keylogger_thread.join()
