from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from __init__ import app

# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along
# Define variable to define type of database (sqlite), and name and location of myDB.db
dbURI = 'sqlite:///model/myDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
# Create SQLAlchemy engine to support SQLite dialect (sqlite:)
db = SQLAlchemy(app)
Migrate(app, db)



# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Users(db.Model):
    # define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, password="", phone=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.password = password
        if len(phone) > 0:
            self.phone = phone
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing section"""


def model_tester():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    # Drops Table: users if it already exists
    db.session.execute('DROP TABLE IF EXISTS users')
    db.create_all()

    """Tester data for table"""
    u1 = Users(name='Nicolaus Copernicus', email='He was the first modern European scientist to propose that Earth and other planets revolve around the sun, or the Heliocentric Theory of the universe.', password='123nic', phone="1111111111")
    u2 = Users(name='Galileo Galilei', email='He made revolutionary telescopic discoveries, including the four largest moons of Jupiter.', password='123gali', phone="1111112222")
    u3 = Users(name='Johannes Kepler', email='He was a German mathematician and astronomer who discovered that the Earth and planets travel about the sun in elliptical orbits.', password='123johan', phone="1111113333")
    u4 = Users(name='Isaac Newton', email='He was a physicist and mathematician who developed the principles of modern physics, including the laws of motion and is credited as one of the great minds of the 17th-century Scientific Revolution.', password='123isaa', phone="1111114444")
    u5 = Users(name='Neil DeGrasse Tyson', email='He, (born October 5, 1958, New York, New York, U.S.), is an American astronomer who popularized science with his books and frequent appearances on radio and television.', password='123neil', phone="1111115555")
    u6 = Users(name='Aristotle', email='He made pioneering contributions to all fields of philosophy and science, he invented the field of formal logic, and he identified the various scientific disciplines and explored their relationships to each other.', password='123aris', phone="1111116666")
    # U7 intended to fail as duplicate key

    table = [u1, u2, u3, u4, u5, u6]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")


def model_printer():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from users')
    print(result.keys())
    for row in result:
        print(row)


if __name__ == "__main__":
    model_tester()  # builds model of Users
    model_printer()