from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, JournalEntry, UserSchema, JournalEntrySchema

@app.before_request
def check_if_logged_in():

    open_access_list = ["signup", "login", "check_sesion"]

    if request.endpoint not in open_access_list and not session.get("user_id"):
        return {"error": "401 Unauthorized Entry"}, 401


class Signup(Resource):

    def post(self):

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User(

            username = username

        )

        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id

            return UserSchema().dump(user), 201
        
        except IntegrityError:
            return {"error": "422 Inprocessable Entity"}, 422
        
class CheckSession(Resource):

    def get(self):

        user = User.query.filter(User.id == session.get("user_id")).first()

        return UserSchema().dump(user), 200
    
class Login(Resource):
    
    def post(self):

        username = request.get_json()["username"]
        password = request.get_json()["password"]

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id
            return UserSchema().dump(user), 200
        
        return {"error": "401 Unauthorized"}, 401


if __name__ == '__main__':
    app.run(port=5555, debug=True)