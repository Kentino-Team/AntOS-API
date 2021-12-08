from flask import Flask, render_template, Response
from flask_restful import Api
from flask_cors import CORS
import security.jwt as jwt

from resources.APIWorker import APIWorker
from resources.command import Command
from resources.farm import Farm
from resources.stat import Stat
from resources.worker import Worker
from resources.user_login import UserLogin
from resources.security import Security
from resources.wallet import Wallet
from resources.flight_sheet import FlightSheet
from resources.user_profile import UserProfile
from resources.configres import Config
from resources.pools import Pools
from resources.miner import Miner

app = Flask(__name__, static_url_path='', static_folder='web/static', template_folder='web/templates')

app.config['MONGO_URI'] = "mongodb://admin:Xolider500_%40@vicart.ovh/antos?authSource=admin"

api = Api(app)

cors = CORS(app)

jwt.init_jwt(app)

api.add_resource(APIWorker, '/worker/api')
api.add_resource(Command, '/command/<rig>')
api.add_resource(Farm, '/farm/<id>/<rig>', '/farm/<id>', '/farm/')
api.add_resource(Stat, '/stat/<rig_id>')
api.add_resource(Worker, '/worker/<rig_id>', '/worker')
api.add_resource(UserLogin, '/user/register')
api.add_resource(Security, '/security')
api.add_resource(Wallet, '/wallet/<id>', '/wallet')
api.add_resource(FlightSheet, '/flightsheet/<id>', '/flightsheet', '/flightsheet/')
api.add_resource(UserProfile, '/user/profile')
api.add_resource(Config, '/config/<rig_id>')
api.add_resource(Pools, '/pools')
api.add_resource(Miner, '/miners')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
