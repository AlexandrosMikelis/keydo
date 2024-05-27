import faust

class Keystroke(faust.Record, serializer="json"):
    user: str
    keystroke_id: str
    key_code: str
    event:str
    timestamp:str