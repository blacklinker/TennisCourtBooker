from datetime import datetime, timedelta
import json
import os
import sys
from threading import Timer

from Model.view_model import ViewModel
from Services.book_service import book

class Controller:
    def __init__(self, model: ViewModel, view):
        self.model = model
        self.view = view
        data = self.load_data()
        self.timer: Timer = None
        if(data != None):
            self.model.bciti_id = str(data.get("id", ""))
            self.model.dob = str(data.get("birth", ""))
            self.model.time = str(data.get("time", ""))
            self.model.email = str(data.get("email", ""))
            
    def callBookService(self, targetTime: str, dob: str, bciti_id: str, email: str):
        link = self.load_link()
        return book(link, targetTime, dob, bciti_id, email)

    def get_bciti_id(self):
        return self.model.get_bciti_id()
    
    def get_dob(self):
        return self.model.get_dob()
    
    def get_email(self):
        return self.model.get_email()
    
    def get_time(self):
        return self.model.get_time()

    def load_data(self):
        if os.path.exists("user_input.json"):
            with open("user_input.json", "r") as file:
                for line in file:
                    try:
                        data = json.loads(line)
                        id = data.get("id", "")
                        birth = data.get("birth", "")
                        time = data.get("time", "")
                        email = data.get("email", "")
                        return {"id": id, "birth": birth, "time": time, "email": email}
                    except json.JSONDecodeError:
                        continue
        else:
            return None
        
    def load_link(self):
        if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
            configPath = os.path.join(sys._MEIPASS, 'config.json')
        else:
            configPath = 'config.json'
        if os.path.exists(configPath):
            with open(configPath, "r") as file:
                for line in file:
                    try:
                        data = json.loads(line)
                        link = data.get("link", "")
                        return link
                    except json.JSONDecodeError:
                        continue
        else:
            return None
        
    def calculateTime(self, start_time: str):
        next_day = datetime.now() + timedelta(days=1)
        booking_time = datetime(next_day.year, next_day.month, next_day.day, int(start_time[:2]), 0, 0)
        wanted_time = booking_time - timedelta(hours=36)
        time = wanted_time - datetime.now()
        if(time.total_seconds() > 0):
            return time.total_seconds()
        else:
            return 0