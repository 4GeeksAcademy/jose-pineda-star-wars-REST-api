import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Character, Planet, User, Favorite


app = Flask(__name__)
CORS(app)

# Configure the database
engine = create_engine('sqlite:///starwars.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

# Routes

# Get a list of all people
@app.route('/people', methods=['GET'])
def get_people():
    people = session.query(Character).all()
    result = []
    for person in people:
        result.append({
            'id': person.id,
            'name': person.name,
            'gender': person.gender,
            'hair_color': person.hair_color,
            'eye_color': person.eye_color
        })
    return jsonify(result)

# Get a single person by ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = session.query(Character).filter_by(id=people_id).first()
    if person:
        result = {
            'id': person.id,
            'name': person.name,
            'gender': person.gender,
            'hair_color': person.hair_color,
            'eye_color': person.eye_color
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'Person not found'}), 404

# Get a list of all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = session.query(Planet).all()
    result = []
    for planet in planets:
        result.append({
            'id': planet.id,
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'population': planet.population
        })
    return jsonify(result)

# Get a single planet by ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = session.query(Planet).filter_by(id=planet_id).first()
    if planet:
        result = {
            'id': planet.id,
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'population': planet.population
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'Planet not found'}), 404

# Get a list of all users
@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'password': user.password
        })
    return jsonify(result)

# Get all favorites belonging to the current user
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  

    favorites = session.query(Favorite).filter_by(user_id=user_id).all()
    result = []
    for favorite in favorites:
        result.append({
            'id': favorite.id,
            'user_id': favorite.user_id,
            'character_id': favorite.character_id,
            'planet_id': favorite.planet_id
        })
    return jsonify(result)

# Add a new favorite planet to the current user
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  

    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    session.add(favorite)
    session.commit()

    return jsonify({'message': 'Favorite planet added successfully'})

# Add a new favorite character to the current user
@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = 1 

    favorite = Favorite(user_id=user_id, character_id=character_id)
    session.add(favorite)
    session.commit()

    return jsonify({'message': 'Favorite character added successfully'})

# Remove a favorite planet from the current user
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = 1  

    favorite = session.query(Favorite).filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        session.delete(favorite)
        session.commit()
        return jsonify({'message': 'Favorite planet removed successfully'})
    else:
        return jsonify({'error': 'Favorite planet not found'}), 404

# Remove a favorite character from the current user
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    user_id = 1  

    favorite = session.query(Favorite).filter_by(user_id=user_id, character_id=character_id).first()
    if favorite:
        session.delete(favorite)
        session.commit()
        return jsonify({'message': 'Favorite character removed successfully'})
    else:
        return jsonify({'error': 'Favorite character not found'}), 404
    
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
