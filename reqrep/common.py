from datetime import datetime

encoding = 'ascii'
STATUS_OK = 'OK'
STATUS_ERROR = 'ERROR'

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")