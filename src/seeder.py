from app import app, db
from models import User, Person, Planet, FavoritePerson, FavoritePlanet

def seed_users():
    if User.query.count() == 0:
        users = [
            User(email='luke@rebellion.org', password='force123', is_active=True),
            User(email='leia@rebellion.org', password='alderaan123', is_active=True),
            User(email='han@falcon.com', password='chewie123', is_active=True)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Users seeded!")
    else:
        print("Users already exist, skipping...")

def seed_planets():
    if Planet.query.count() == 0:
        planets = [
            Planet(
                name='Tatooine',
                rotation_period='23',
                orbital_period='304',
                diameter='10465',
                climate='arid',
                gravity='1 standard',
                terrain='desert',
                surface_water='1',
                population='200000'
            ),
            Planet(
                name='Alderaan',
                rotation_period='24',
                orbital_period='364',
                diameter='12500',
                climate='temperate',
                gravity='1 standard',
                terrain='grasslands, mountains',
                surface_water='40',
                population='2000000000'
            ),
            Planet(
                name='Yavin IV',
                rotation_period='24',
                orbital_period='4818',
                diameter='10200',
                climate='temperate, tropical',
                gravity='1 standard',
                terrain='jungle, rainforests',
                surface_water='8',
                population='1000'
            )
        ]
        db.session.bulk_save_objects(planets)
        db.session.commit()
        print("Planets seeded!")
    else:
        print("Planets already exist, skipping...")

def seed_people():
    if Person.query.count() == 0:
        people = [
            Person(
                name='Luke Skywalker',
                height='172',
                mass='77',
                hair_color='blond',
                skin_color='fair',
                eye_color='blue',
                birth_year='19BBY',
                gender='male',
                home_world=1  
            ),
            Person(
                name='Leia Organa',
                height='150',
                mass='49',
                hair_color='brown',
                skin_color='fair',
                eye_color='brown',
                birth_year='19BBY',
                gender='female',
                home_world=2  
            ),
            Person(
                name='Han Solo',
                height='180',
                mass='80',
                hair_color='brown',
                skin_color='fair',
                eye_color='brown',
                birth_year='29BBY',
                gender='male',
                home_world=1  
            )
        ]
        db.session.bulk_save_objects(people)
        db.session.commit()
        print("People seeded!")
    else:
        print("People already exist, skipping...")

def seed_favorites():
    if FavoritePerson.query.count() == 0 and FavoritePlanet.query.count() == 0:
        favorites_people = [
            FavoritePerson(user_id=1, people_id=2),  
            FavoritePerson(user_id=1, people_id=3)   
        ]
        favorites_planets = [
            FavoritePlanet(user_id=1, planet_id=1), 
            FavoritePlanet(user_id=1, planet_id=2)  
        ]
        
        db.session.bulk_save_objects(favorites_people)
        db.session.bulk_save_objects(favorites_planets)
        db.session.commit()
        print("Favorites seeded!")
    else:
        print("Favorites already exist, skipping...")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_users()
        seed_planets()
        seed_people()
        seed_favorites()
        print("Database seeding completed!")