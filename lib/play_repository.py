from lib.db import db
from lib.play import Play

class PlayRepository:

    def __init__(self):
        pass

    def create(self, play: Play) -> None:
        db.session.add(play)
        db.session.commit()
        return None