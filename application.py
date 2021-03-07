from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from database.db import initialize_db

from controllers.movie import MovieController

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag',
}

initialize_db(app)

CORS(app, resources={r"/*": {"origin": "*"}})

api.add_resource(MovieController,
                 '/movies',
                 '/movies/<movie_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
