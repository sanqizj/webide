from exts import db


class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return fields


class User(db.Model, EntityBase):
    __tablename__ = 'users'
    userid = db.Column(db.String(10), primary_key=True, unique=True)
    password = db.Column(db.String(20))

    def __init__(self, id, password):
        self.userid = id
        self.password = password
        db.session.add(self)
        db.session.commit()
