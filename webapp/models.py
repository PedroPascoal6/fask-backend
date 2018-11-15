from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import names, random
from random import randint

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
                            substitute_id=new_politician.get('substitute_id'))

    db.session.add(politician)
    db.session.commit()


def save_event(new_event):
    event = Event(date=new_event.get('date'),
                  politician_id=new_event.get('politician_id'),
                  event_type=new_event.get('event_type'),
                  text=new_event.get('text'))
    db.session.add(event)
    db.session.commit()


def setPoliticianInactive(politician_id, substitute_id):
    updateActiveStateOnPolitician(politician_id, substitute_id, False)


def setPoliticianActive(politician_id, substitute_id):
    updateActiveStateOnPolitician(politician_id, substitute_id, True)


def updateActiveStateOnPolitician(politician_id, substitute_id, state):
    politician = Politician.query.filter_by(id=politician_id).first()
    politician.active = state
    politician.substitute_id = substitute_id
    db.session.commit()


# Passagem de subordinados para outro politico
def updateSubordinates(superior_id, subordinate_list, on_top):
    politician = Politician.query.filter_by(id=superior_id).first()
    for subordinate_selected in subordinate_list:
        politician_id = subordinate_selected.get('attr').get('id')
        # caso não seja o mesmo
        if politician_id != politician:
            subordinate = Politician.query.filter_by(id=politician_id).first()
            subordinate.superior_id = superior_id
            subordinate.superior_name = politician.name
            if on_top:
                politician.superior_id = None
            db.session.commit()


# Reaver os seus subordinados
def resetSubordinates(superior_id, subordinate_Substitute):
    politician = Politician.query.filter_by(id=superior_id).first()
    subordinate_list = subordinate_Substitute.get('children')
    for subordinate_selected in subordinate_list:
        subordinate_id = subordinate_selected.get('attr').get('id')
        original_superior = subordinate_selected.get('attr').get('superiorid_original')
        print("subordinate_id->" + str(subordinate_id))
        print("original_superior->" + str(original_superior))
        print("superior_id->" + str(superior_id))
        print("if ->" + str(int(original_superior) == int(superior_id)))
        if int(original_superior) == int(superior_id):
            subordinate = Politician.query.filter_by(id=subordinate_id).first()
            subordinate.superior_id = superior_id
            subordinate.superior_name = politician.name

    # TODO rever se é necessario ou se basta apenas adicionar
    if int(subordinate_Substitute.get('attr').get('superiorid_original')) == int(superior_id):
        subordinate = Politician.query.filter_by(id=int(subordinate_Substitute.get('attr').get('id'))).first()
        subordinate.superior_id = superior_id
        subordinate.superior_name = politician.name
    db.session.commit()


def generate_data(amount):
    Politician.query.delete()
    choice = list(["yes", "no"])
    for n in range(0, amount):
        new_politician_name = names.get_full_name()
        superior_name = None
        superior_id = None
        if random.choice(choice) == "yes":
            if n > 0:
                superior_id = randint(0, n - 1)
                politician = Politician.query.filter_by(id=superior_id).first()
                superior_name = politician.name
                if politician.subordinate_id is None:
                    politician.subordinate_id = n
                    politician.subordinate_name = new_politician_name
        else:
            superior_id = None

        new_politician = {"id": n,
                          "name": new_politician_name,
                          "active": True,
                          "superior_id": superior_id,
                          "superior_id_original": superior_id,
                          "superior_name": superior_name,
                          "subordinate_id": None,
                          "subordinate_name": None
                          }
        save_politician(new_politician)