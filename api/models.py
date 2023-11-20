from api.extensions import db 
from datetime import datetime



# class Base(db.Model):
#     id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
#     created = db.Column(db.DateTime(),default=datetime.utcnow())

class User (db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime(),default=datetime.utcnow())
    username = db.Column(db.String(),nullable=False,unique =True)
    email = db.Column(db.String(),nullable=False, unique=True)
    password = db.Column(db.String(),nullable=False)

    task=db.relationship('Task',backref='user',lazy=True)
    meal=db.relationship('Meal',backref='user',lazy=True)
    income=db.relationship('Income',backref='user',lazy=True)
    expense=db.relationship('Expense',backref='user',lazy=True)
    

    def __repr__(self):
        return f"{self.id},{self.username},{self.email},{self.created},{self.id}"

class Task(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime(),default=datetime.utcnow())
    task = db.Column(db.String(),nullable =False)
    description=db.Column(db.Text(),nullable=True)
    duetime =db.Column(db.DateTime(),nullable=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=True)

    def __repr__(self):
        return f"{self.id},{self.task},{self.description},{self.duetime},{self.created},{self.user_id}"

class Meal(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime(),default=datetime.utcnow())
    meal=db.Column(db.String(),nullable=False)
    meal_description=db.Column(db.Text(),nullable=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=True)

    def __repr__(self):
        return f"{self.id},{self.meal},{self.description},{self.created},{self.user_id}"

class Income(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime(),default=datetime.utcnow())
    income = db.Column(db.Float(),nullable=False)
    details = db.Column(db.Text(),nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=True)

    def __repr__(self):
        return f"{self.id},{self.income},{self.details},{self.created},{self.user_id}"


class Expense(db.Model):
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime(),default=datetime.utcnow())
    expense =db.Column(db.Float(), nullable= False)
    expense_details = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=True)

    def __repr__(self):
       return f"{self.id},{self.expense},{self.details},{self.created},{self.user_id}"
    

class RevokedTokens(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    token = db.Column(db.String(),nullable=False)
    # user_id=db.Column(db.Integer(),nullable=False)
    created =db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self):
          return f'{self.token}'

      