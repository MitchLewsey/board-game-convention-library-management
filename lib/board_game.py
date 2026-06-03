from lib.db import db


class BoardGame(db.Model):
    __tablename__ = 'board_game'

    id           = db.Column(db.Integer,     primary_key=True)
    name         = db.Column(db.String(255), nullable=False)
    bgg_id       = db.Column(db.Integer)
    factory_upc  = db.Column(db.String(20),  unique=True)
    min_players  = db.Column(db.SmallInteger)
    max_players  = db.Column(db.SmallInteger)
    min_time     = db.Column(db.SmallInteger)
    max_time     = db.Column(db.SmallInteger)
    publisher    = db.Column(db.String(255))
    designer     = db.Column(db.String(255))
    artist       = db.Column(db.String(255))
    is_expansion = db.Column(db.Boolean,     nullable=False, default=False)
    base_game_id = db.Column(db.Integer,     db.ForeignKey('board_game.id', ondelete='SET NULL'))

    def __eq__(self, other):
        game1 = {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state'}
        game2 = {k: v for k, v in other.__dict__.items() if k != '_sa_instance_state'}
        return game1 == game2
    
    def __repr__(self):
        return f"BoardGame({self.id}, {self.name}, {self.bgg_id}, {self.factory_upc}, {self.min_players}, {self.max_players}, {self.min_time}, {self.max_time}, {self.publisher}, {self.designer}, {self.artist}, {self.is_expansion}, {self.base_game_id})"