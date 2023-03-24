from . import db


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
