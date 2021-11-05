from flask_restful import Resource
from flask_jwt import jwt_required


class Security(Resource):

    @jwt_required()
    def get(self):
        return {}, 200
