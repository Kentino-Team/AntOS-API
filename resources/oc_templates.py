from flask_restful import Resource, request
from config.db import db
from flask_jwt import jwt_required, current_identity
import json
from bson import json_util


class OCTemplates(Resource):

    @jwt_required()
    def get(self, id="", rig_id=""):
        templates = db.oc_templates.find({
            "user_id": current_identity.id,
            "farm_id": {
                "$in": ["", id]
            },
            "rig_id": {
                "$in": ["", rig_id]
            }
        })
        templates = json.loads(json_util.dumps(templates))
        return templates, 200

    @jwt_required()
    def post(self, id="", rig_id=""):
        template = request.json['template']
        db.oc_templates.insert_one({
            "farm_id": id,
            "user_id": current_identity.id,
            "config": template,
            "rig_id": rig_id
        })
        return {}, 201
