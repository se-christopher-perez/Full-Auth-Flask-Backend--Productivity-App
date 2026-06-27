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
    
class Logout(Resource):

    def delete(self):

        if session.get("user_id"):
            session["user_id"] = None

            return {}, 204
        
        return {}, 401
    
class JournalEntryIndex(Resource):

    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        paginated = JournalEntry.query.filter(JournalEntry.user_id == session["user_id"]).paginate(page=page, per_page=per_page, error_out=False)

        return {
            "page": paginated.page,
            "per_page": paginated.per_page,
            "total": paginated.total,
            "total_pages": paginated.pages,
            "items": [JournalEntrySchema().dump(entry) for entry in paginated.items]
        }, 200
    
    def post(self):
        data = request.get_json()

        entry = JournalEntry(
            
            title = data.get("title"),
            content = data.get("content"),
            user_id = session["user_id"]

        )

        try:
            db.session.add(entry)
            db.session.commit()
            
            return JournalEntrySchema().dump(entry), 201

        except IntegrityError:
            return {"error": "422 Unprocessable Entity"}, 422

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")


if __name__ == '__main__':
    app.run(port=5555, debug=True)