from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class Politician(db.Model):
    __tablename__ = "politicians"
    id = db.Column('id', db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    name = db.Column('name', db.String(255))
    superior_id = db.Column('superior_id', db.Integer())
    superior_name = db.Column('superior_name', db.String(255))
    subordinate_id = db.Column('subordinate_id', db.Integer())
    subordinate_name = db.Column('subordinate_name', db.String(255))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('date', db.DateTime)
    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'))
    # politician = db.relationship("politicians", uselist=False, backref=backref('events'))
    event_type = db.Column('event_type', db.Integer)
    text = db.Column('text', db.String)


def save_politician(new_politician):
    print(new_politician.get('id'))
    politician = Politician(id=new_politician.get('id'),
                            active=new_politician.get('active'),
                            name=new_politician.get('name'),
                            superior_id=new_politician.get('superior_id'),
                            superior_name=new_politician.get('superior_name'),
                            subordinate_id=new_politician.get('subordinate_id'),
                            subordinate_name=new_politician.get('subordinate_name'))

    db.session.add(politician)
    db.session.commit()


def save_event(new_event):
    event = Event(id=new_event.get('id'),
                  date=new_event.get('date'),
                  politician_id=new_event.get('politician_id'),
                  event_type=new_event.get('event_type'),
                  text=new_event.get('text'))
    db.session.add(event)
    db.session.commit()
