"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    results = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
        }
        results.append(user_data)
    return jsonify(results)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    results = []
    for person in people:
        person_data = {
            'id': person.id,
            'name': person.name,
            'gender': person.gender,
            'lastname': person.lastname
        }
        results.append(person_data)
    return jsonify(results)

@app.route('/people', methods=['POST'])
def add_person():
    data = request.get_json()
    new_person = People(name=data['name'], gender=data['gender'], lastname=data['lastname'])
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'Person created successfully'}),200

@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    person = People.query.get(id)
    return jsonify({'data':person.serialize()}),200


@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
    new_planet = Planets(name=data['name'], size=data['size'], population=data['population'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'message': 'Planet created successfully'}),200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planets.query.get(id)
    return jsonify({'data':planet.serialize()}),200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    results = []
    for planet in planet:
        planet_data = {
            'id': planet.id,
            'name': planet.name,
            'size': planet.size,
            'population': planet.population
        }
        results.append(planet_data)
    return jsonify(results)

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = favorites.query.all()
    results = []
    for favorite in favorites:
        favorite_data = {
            'id': favorite.id,
            'people': favorite.people_id,
            'planets': favorite.planets_id,
            'users': favorite.user_id
        }
        results.append(favorite_data)
    return jsonify(results)

@app.route('/favorites', methods=['POST'])
def add_planets_favorites():
    data = request.get_json()
    new_favorites = Favorites(people_id=data['people_id'], planets_id=data['planets_id'], user_id=data['user_id'])
    db.session.add(new_favorites)
    db.session.commit()
    return jsonify({'message': 'added to favorites'}),200

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite_to_delete = Favorites.query.filter_by(id=favorite_id).first()

    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()
        return jsonify({'message': 'Favorite deleted successfully'}), 200
    else:
        return jsonify({'error': 'Favorite not found'}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
