import os
basedir =os.path.abspath(os.path.dirname(__file__))

def load_private_key():
    key_path = os.path.join(basedir, ".ssh", "private-key.pem")
    with open(key_path, 'r') as f:
        return f.read()

class Config:
    SECRET_KEY = load_private_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CANCELLATION_DEADLINE_DAYS = int(os.environ.get('CANCELLATION_DEADLINE_DAYS', 2))
    UNAVAILABLE_ROOM_STATUS_NAMES = [
        name.strip()
        for name in os.environ.get(
            'UNAVAILABLE_ROOM_STATUS_NAMES',
            'Karbantartás,Karbantartás alatt,Nem elérhető',
        ).split(',')
        if name.strip()
    ]
