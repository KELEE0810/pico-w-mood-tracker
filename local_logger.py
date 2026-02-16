import os

class LocalLogger:
    def __init__(self, filename="mood_log.csv"):
        self.filename = filename
    
    def save(self, data_str):
        with open(self.filename, "a") as f:
            f.write(data_str + "\n")
            
    def read_all(self):
        if self.filename in os.listdir():
            with open(self.filename, "r") as f:
                return f.readlines()
        return []
    
    def clear(self):
        if self.filename in os.listdir():
            os.remove(self.filename)