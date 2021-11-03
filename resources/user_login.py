from flask_restful import Resource, request
from config.db import db


class UserLogin(Resource):

    def get(self):
        login = request.args.get('login')
        password = request.args.get('pwd')
        user = db.users.find_one({
            "$or": [{
                "email": login
            }, {
                "pseudo": login
            }],
            "pwd": password
        })
        if user is None:
            return {"error": "invalid user"}, 404


        return 200
