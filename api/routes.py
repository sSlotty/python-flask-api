from flask_restful import Api

from api.authentication import SignUpApi, TokenApi, RefreshTokenApi
from api.movie import MoviesApi, MovieApi


def create_route(api: Api):
    api.add_resource(MoviesApi, '/movies')
    api.add_resource(MovieApi, '/movies/<movie_id>')

    api.add_resource(SignUpApi, '/authentication/signup')
    api.add_resource(TokenApi, '/authentication/token')
    api.add_resource(RefreshTokenApi, '/authentication/token/refresh')
