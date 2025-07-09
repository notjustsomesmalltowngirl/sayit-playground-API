from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin

db = SQLAlchemy()


class MasterClass(db.Model):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String, nullable=False)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name != 'playground_id' and column.name != 'id'
        }

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


class Playground(db.Model):
    __tablename__ = 'playground'
    id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False, unique=True)
    did_you_knows = db.relationship('DidYouKnow', backref='playground', lazy='dynamic')
    hypotheticals = db.relationship('Hypotheticals', backref='playground', lazy='dynamic')
    hot_takes = db.relationship('HotTakes', backref='playground', lazy='dynamic')
    never_have_i_evers = db.relationship('NeverHaveIEver', backref='playground', lazy='dynamic')
    would_you_rather_questions = db.relationship('WouldYouRather', backref='playground', lazy='dynamic')
    story_builders = db.relationship('StoryBuilder', backref='playground', lazy='dynamic')
    riddles = db.relationship('Riddle', backref='playground', lazy='dynamic')
    two_truths_and_a_lie = db.relationship('TwoTruthsAndALie', backref='playground', lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, type={self.type}>'


class DidYouKnow(MasterClass):
    __tablename__ = 'did_you_know'
    fact = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class Hypotheticals(MasterClass):
    __tablename__ = 'hypotheticals'
    scenario = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class HotTakes(MasterClass):
    __tablename__ = 'hot_takes'
    opinion = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class NeverHaveIEver(MasterClass):
    __tablename__ = 'never_have_i_ever'
    question = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class WouldYouRather(MasterClass):
    __tablename__ = 'would_you_rather'
    scenario = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class StoryBuilder(MasterClass):
    __tablename__ = 'story_builder'
    starter = mapped_column(String, nullable=False, unique=True)
    difficulty = mapped_column(String, nullable=False, default='easy')
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class Riddle(MasterClass):
    __tablename__ = 'riddle'
    question = mapped_column(String, nullable=False, unique=True)
    answer = mapped_column(String, nullable=False)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))


class TwoTruthsAndALie(MasterClass):
    __tablename__ = 'two_truths_and_a_lie'
    true_statement_1 = mapped_column(String, nullable=False, unique=True)
    true_statement_2 = mapped_column(String, nullable=False, unique=True)
    false_statement = mapped_column(String, nullable=False, unique=True)
    playground_id = mapped_column(Integer, db.ForeignKey('playground.id'))

    __table_args__ = (
        db.UniqueConstraint('true_statement_1', 'true_statement_2', 'false_statement', name='unique_statements_combo'),
    )


# class for users to suggest stuff like new games and riddles categories and stuff

# class PendingSuggestions(MasterClass):
#     category = None
#     suggestor_id = mapped_column(db.ForeignKey('users.id'))
#     suggestor = db.relationship('User', back_populates='suggestions')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    role = mapped_column(String, default='user', nullable=False)
    api_key = mapped_column(String, unique=True, nullable=True)
    # suggestions = db.relationship('PendingSuggestions', back_populates='suggestor')
