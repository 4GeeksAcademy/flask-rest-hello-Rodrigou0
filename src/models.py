from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
            return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<people %r>' %self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "lastname": self.lastname
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    population = db.Column(db.String(120), unique=False, nullable=False)
    size = db.Column(db.String(120), unique=False, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return '<planets %r>' %self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "size": self.size,
            "population": self.population,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    people = db.relationship("People")
    user = db.relationship("User")
    planets = db.relationship("Planets")

    def __repr__(self):
        return '<favorites %r>' %self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "people":self.people_id,
            "planets": self.planets_id,
            "user": self.user_id,
        }


    