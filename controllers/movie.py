from flask import request, Response, jsonify
from flask_restful import Resource
from flask_mongoengine import DoesNotExist
from mongoengine import NotUniqueError
from kanpai import Kanpai

from database.models import Movie


class MovieController(Resource):
    def get(self, movie_id: str = None):
        if movie_id is not None:
            try:
                movie = Movie.objects.get(id=movie_id).to_json()
                return Response(movie, mimetype="application/json", status=200)
            except DoesNotExist:
                return Response(status=404)
        else:
            movies = Movie.objects()
            if len(movies) > 0:
                return Response(movies.to_json(), mimetype="application/json", status=200)
            else:
                return Response(status=204)

    def post(self):
        schema = Kanpai.Object({
            'name': Kanpai.String().required(),
            'casts': Kanpai.Array().required(),
            'genres': Kanpai.Array().required()
        })

        validate_result = schema.validate(request.json)
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            movie = Movie(**body).save()
            return Response(status=201)
        except NotUniqueError:
            return Response("Name is already exist", status=400)

    def patch(self, movie_id: str):
        schema = Kanpai.Object({
            'name': Kanpai.String(),
            'casts': Kanpai.Array(),
            'genres': Kanpai.Array()
        })

        validate_result = schema.validate(request.json)
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            Movie.objects.get(id=movie_id).update(**body)
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)

    def delete(self, movie_id: str):
        try:
            Movie.objects.get(id=movie_id).delete()
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)
