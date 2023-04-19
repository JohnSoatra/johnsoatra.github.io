from datetime import datetime

def now():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def find(lamb, items):
    return next((item for item in items if lamb(item)), None)

