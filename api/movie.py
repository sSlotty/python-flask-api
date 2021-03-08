from flask import request, Response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.movies import Movies


class MoviesApi(Resource):
    @jwt_required()
    def get(self) -> Response:
        movies = Movies.objects()
        if len(movies) > 0:
            response = jsonify(movies)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def post(self) -> Response:
        schema = Kanpai.Object({
            'name': Kanpai.String().required(),
            'casts': Kanpai.Array().required(),
            'genres': Kanpai.Array().required()
        })

        validate_result = schema.validate(request.get_json())
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            Movies(**body).save()
            return Response(status=201)
        except NotUniqueError:
            return Response("Name is already exist", status=400)

class MovieApi(Resource):
    def get(self, movie_id: str = None) -> Response:
        try:
            movie = Movies.objects.get(id=movie_id).to_json()
            return Response(movie, mimetype="application/json", status=200)
        except DoesNotExist:
            return Response(status=404)

    def patch(self, movie_id: str) -> Response:
        schema = Kanpai.Object({
            'casts': Kanpai.Array(),
            'genres': Kanpai.Array()
        })

        validate_result = schema.validate(request.get_json())
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            Movies.objects.get(id=movie_id).update(**body)
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)

    def delete(self, movie_id: str) -> Response:
        try:
            Movies.objects.get(id=movie_id).delete()
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)
