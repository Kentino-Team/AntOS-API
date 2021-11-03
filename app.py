from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

from resources.APIWorker import APIWorker
from resources.command import Command
from resources.farm import Farm
from resources.stat import Stat
from resources.worker import Worker
from resources.user_login import UserLogin

app = Flask(__name__, static_url_path='', static_folder='web/static', template_folder='web/templates')

app.config['MONGO_URI'] = "mongodb://admin:Xolider500_%40@vicart.ovh/antos?authSource=admin"

api = Api(app)

cors = CORS(app)

api.add_resource(APIWorker, '/worker/api')
api.add_resource(Command, '/command')
api.add_resource(Farm, '/farm/<id>/<rig>', '/farm/<id>', '/farm/')
api.add_resource(Stat, '/stat/<rig_id>')
api.add_resource(Worker, '/worker')
api.add_resource(UserLogin, '/user/login')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
