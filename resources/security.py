from flask_restful import Resource
from flask_jwt import jwt_required, current_identity


class Security(Resource):

    @jwt_required()
    def get(self):
        return current_identity.jsonify(), 200
