class ChatSession:
    def __init__(self, session_id, timestamp):
        self.session_id = session_id
        self.timestamp = timestamp
        self.messages = []

    def add_message(self, sender, content, timestamp):
        self.messages.append({
            "sender": sender,
            "content": content,
            "timestamp": timestamp
        })

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "messages": self.messages
        }

    @classmethod
    def from_dict(cls, data):
        session = cls(data["session_id"], data["timestamp"])
        session.messages = data["messages"]
        return session
