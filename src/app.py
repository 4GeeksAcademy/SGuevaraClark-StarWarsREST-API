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
from models import db, User, Person, Planet, FavoritePerson, FavoritePlanet


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


@app.route('/people', methods=['GET'])
def get_all_people():
    people = Person.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Person.query.get(people_id)
    if person is None:
        raise APIException('Person not found', status_code=404)
    return jsonify(person.serialize()), 200

# Planet endpoints
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

# User endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # For demo purposes, using user_id=1. In a real app, this would come from authentication
    user = User.query.get(1)
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize()), 200

# Favorite endpoints
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # For demo purposes, using user_id=1
    user = User.query.get(1)
    planet = Planet.query.get(planet_id)
    
    if user is None or planet is None:
        raise APIException('User or Planet not found', status_code=404)
        
    favorite = FavoritePlanet(user_id=user.id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    # For demo purposes, using user_id=1
    user = User.query.get(1)
    person = Person.query.get(people_id)
    
    if user is None or person is None:
        raise APIException('User or Person not found', status_code=404)
        
    favorite = FavoritePerson(user_id=user.id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite person added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # For demo purposes, using user_id=1
    favorite = FavoritePlanet.query.filter_by(user_id=1, planet_id=planet_id).first()
    
    if favorite is None:
        raise APIException('Favorite planet not found', status_code=404)
        
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet deleted successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    # For demo purposes, using user_id=1
    favorite = FavoritePerson.query.filter_by(user_id=1, people_id=people_id).first()
    
    if favorite is None:
        raise APIException('Favorite person not found', status_code=404)
        
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite person deleted successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)