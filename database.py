from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String
import threading
from config import database_url


def start() -> scoped_session:
    engine = create_engine(database_url, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

class Channels(BASE):

    __tablename__ = "channels"
    username = Column(String, primary_key=True)


    def __init__(self, username):
        self.username = username


class ProfilePics(BASE):

    __tablename__ = "profilepics"
    username = Column(String, primary_key=True)
    url = Column(String, primary_key=False)

    def __init__(self, username, url):
        self.username = username
        self.url = url


Channels.__table__.create(checkfirst=True)
ProfilePics.__table__.create(checkfirst=True)

APPROVE_INSERTION_LOCK = threading.RLock()


def add_user(username):
    if username == None:
        return
    with APPROVE_INSERTION_LOCK:
        add_user = SESSION.query(Channels).get(username)
        if add_user is not None:
            return
        user = Channels(username)
        SESSION.add(user)
        SESSION.commit()


def remove_user(username):
    with APPROVE_INSERTION_LOCK:
        disapprove_user = SESSION.query(Channels).get(username)
        print(disapprove_user)
        if disapprove_user:
            SESSION.delete(disapprove_user)
            SESSION.commit()
        else:
            SESSION.close()


def search():
    with APPROVE_INSERTION_LOCK:
        stuff = SESSION.query(Channels.username).all()
        SESSION.close()
        return stuff


def searchpfp(username):
    with APPROVE_INSERTION_LOCK:
        stuff = SESSION.query(ProfilePics).get(username)
        SESSION.close()

    if stuff == None:
        return None

    return stuff.url
        
def add_pfp(username, url):
    with APPROVE_INSERTION_LOCK:
        add_user = SESSION.query(ProfilePics).get(username)
        if add_user is not None:
            return
        user = ProfilePics(username, url)
        SESSION.add(user)
        SESSION.commit()
