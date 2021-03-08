from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine

from api.routes import create_route

config = {
    'JSON_SORT_KEYS': False,
    'MONGODB_SETTINGS': {
        'host': 'mongodb://localhost/movie-bag'
    }
}

# init flask
app = Flask(__name__)

# configure app
app.config.update(config)

# init api and routes
api = Api(app)
create_route(api=api)

# init mongoengine
db = MongoEngine(app=app)

# setup CORS
CORS(app, resources={r"/*": {"origin": "*"}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
