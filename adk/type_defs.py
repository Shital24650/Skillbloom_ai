from typing import Dict

class Message:
    def __init__(self, payload: Dict, sender: str, receiver: str):
        self.payload = payload
        self.sender = sender
        self.receiver = receiver