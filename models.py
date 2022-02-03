import os

from sqlalchemy import String, Column, Integer, Text
from flask_sqlalchemy import SQLAlchemy


database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    if database_path.startswith("postgres://"):
        database_path = database_path.replace(
            "postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


def sample_data():
    db.drop_all()
    db.create_all()
    cocktail1 = Cocktail(name="test cocktail1",
                         ingredients=[],
                         directions="test directions1",
                         glassware="test glassware",
                         tags=[])
    beer1 = Beer(name="test beer1",
                 style="test style1",
                 draft_or_bottle="draft",
                 tags=[])
    wine1 = Wine(name="test wine1",
                 classification="red",
                 varietal="test varietal",
                 appellation="test appellation",
                 vintage=2022,
                 tags=[])

    cocktail1.create()
    beer1.create()
    wine1.create()


# Beverage tags and association tables

cocktail_tags = db.Table('cocktail_tags',
                         db.Column('cocktail_id', db.Integer, db.ForeignKey('cocktails.id')),
                         db.Column('bev_tag_id', db.Integer, db.ForeignKey('bev_tags.id')))

beer_tags = db.Table('beer_tags',
                     db.Column('beer_id', db.Integer, db.ForeignKey('beer.id')),
                     db.Column('bev_tag_id', db.Integer, db.ForeignKey('bev_tags.id')))

wine_tags = db.Table('wine_tags',
                     db.Column('wine_id', db.Integer, db.ForeignKey('wine.id')),
                     db.Column('bev_tag_id', db.Integer, db.ForeignKey('bev_tags.id')))


class BevTag(db.Model):
    __tablename__ = 'bev_tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def detailed(self):
        return {
            'id': self.id,
            'name': self.name
        }


# Cocktails, ingredients, and association table

cocktail_ingredients = db.Table('cocktail_ingredients',
                                db.Column('cocktail_id', db.Integer, db.ForeignKey('cocktails.id')),
                                db.Column('cocktail_ingredient_id', db.Integer, db.ForeignKey('ingredients.id')))


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def detailed(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Cocktail(db.Model):
    __tablename__ = "cocktails"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ingredients = db.relationship('Ingredient',
                                  secondary=cocktail_ingredients,
                                  backref=db.backref('cocktails', lazy='dynamic'))
    directions = Column(Text, nullable=True)
    glassware = Column(String, nullable=True)
    tags = db.relationship('BevTag',
                           secondary=cocktail_tags,
                           backref=db.backref('cocktails', lazy='dynamic'))

    def __init__(self, name, ingredients, directions, glassware, tags):
        self.name = name
        self.ingredients = ingredients
        self.directions = directions
        self.glassware = glassware
        self.tags = tags

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def detailed(self):
        return {
            'id': self.id,
            'name': self.name,
            'directions': self.name,
            'glasswear': self.glassware,
            'ingredients': [ingredient.name for ingredient in self.ingredients],
            'tags': [tag.name for tag in self.tags]
        }

    def basic(self):
        return {
            'id': self.id,
            'name': self.name
        }


# Beer table

class Beer(db.Model):
    __tablename__ = 'beer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    style = Column(String)
    draft_or_bottle = Column(String)
    tags = db.relationship('BevTag', secondary=beer_tags, backref=db.backref('beer', lazy=True))

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def detailed(self):
        return {
            'id': self.id,
            'name': self.name,
            'style': self.style,
            'draft_or_bottle': self.draft_or_bottle,
            'tags': [tag.name for tag in self.tags]
        }

    def basic(self):
        return {
            'id': self.id,
            'name': self.name
        }


# Wine Table

class Wine(db.Model):
    __tablename__ = 'wine'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    classification = Column(String)
    varietal = Column(String)
    vintage = Column(Integer)
    appellation = Column(String)
    tags = db.relationship('BevTag', secondary=wine_tags, backref=db.backref('wine', lazy=True))

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def detailed(self):
        return {
            'id': self.id,
            'name': self.name,
            'classification': self.classification,
            'varietal': self.varietal,
            'vintage': self.vintage,
            'appellation': self.appellation,
            'tags': [tag.name for tag in self.tags]
        }

    def basic(self):
        return {
            'id': self.id,
            'name': self.name
        }







