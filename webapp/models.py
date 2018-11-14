from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class Politician(db.Model):
    __tablename__ = "politicians"
    id = db.Column('id', db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    name = db.Column('name', db.String(255))
    superior_id_original = db.Column('superior_id_original', db.Integer())
    superior_id = db.Column('superior_id', db.Integer())
    superior_name = db.Column('superior_name', db.String(255))
    subordinate_id = db.Column('subordinate_id', db.Integer())
    subordinate_name = db.Column('subordinate_name', db.String(255))
    substitute_id = db.Column('substitute_id', db.Integer())

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
                            superior_id_original=new_politician.get('superior_id_original'),
                            superior_id=new_politician.get('superior_id'),
                            superior_name=new_politician.get('superior_name'),
                            subordinate_id=new_politician.get('subordinate_id'),
                            subordinate_name=new_politician.get('subordinate_name'),
                            substitute_id = new_politician.get('substitute_id'))

    db.session.add(politician)
    db.session.commit()


def save_event(new_event):
    event = Event(date=new_event.get('date'),
                  politician_id=new_event.get('politician_id'),
                  event_type=new_event.get('event_type'),
                  text=new_event.get('text'))
    db.session.add(event)
    db.session.commit()


def setPoliticianInactive(politician_id,substitute_id):
    updateActiveStateOnPolitician(politician_id,substitute_id, False)


def setPoliticianActive(politician_id,substitute_id):
    updateActiveStateOnPolitician(politician_id,substitute_id, True)


def updateActiveStateOnPolitician(politician_id,substitute_id, state):
    politician = Politician.query.filter_by(id=politician_id).first()
    politician.active = state
    politician.substitute_id = substitute_id
    db.session.commit()

#Passagem de subordinados para outro politico
def updateSubordinates(superior_id, subordinate_list, on_top):
    politician = Politician.query.filter_by(id=superior_id).first()
    for subordinate_selected in subordinate_list:
        politician_id = subordinate_selected.get('attr').get('id')
        #caso não seja o mesmo
        if politician_id != politician:
            subordinate = Politician.query.filter_by(id=politician_id).first()
            subordinate.superior_id = superior_id
            subordinate.superior_name = politician.name
            if on_top:
                politician.superior_id = None
            db.session.commit()

#Reaver os seus subordinados
def resetSubordinates(superior_id, subordinate_list):
    politician = Politician.query.filter_by(id=superior_id).first()
    for n in subordinate_list:
        subordinate_id = subordinate_list[n].get('attr').get('id')
        original_superior = subordinate_list[n].get('attr').get('superiorid_original')
        if original_superior == superior_id:
            subordinate = Politician.query.filter_by(id=subordinate_id).first()
            subordinate.superior_id = superior_id
            subordinate.superior_name = politician.get('attr').get('name')
            db.session.commit()