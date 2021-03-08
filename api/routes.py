from flask_restful import Api

from api.movie import MoviesApi, MovieApi


def create_route(api: Api):
    api.add_resource(MoviesApi, '/movies')
    api.add_resource(MovieApi, '/movies/<movie_id>')
