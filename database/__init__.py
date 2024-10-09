from datetime import datetime
from .models import Session, Log


def log_request(user_id, command, response):
    session = Session()
    log_entry = Log(user_id=user_id, command=command, timestamp=datetime.now(), response=response)
    session.add(log_entry)
    session.commit()
