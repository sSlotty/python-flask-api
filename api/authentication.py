from flask import request, Response, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    jwt_required,
    get_jwt_identity
)

from mongoengine import DoesNotExist

from models.oauth.error import OAuthErrorResponse
from models.oauth.token import TokenResponse
from models.users import Users


class SignUpApi(Resource):
    def post(self) -> Response:
        body = request.get_json()
        user = Users(**body)
        user.save()
        response = Response()
        response.status_code = 201
        return response


class TokenApi(Resource):
    def post(self) -> Response:
        body = request.form.to_dict()
        if body.get('username') is None or body.get('password') is None:
            response = jsonify(
                OAuthErrorResponse(
                    "invalid_request", "The request is missing a required parameter."
                ).__dict__
            )
            response.status_code = 400
            return response

        try:
            user: Users = Users.objects.get(username=body.get('username'))
            auth_success = user.check_pw_hash(body.get('password'))
            if not auth_success:
                response = jsonify(
                    OAuthErrorResponse(
                        "invalid_grant", "The username or password is incorrect."
                    ).__dict__
                )
                response.status_code = 400
                return response
            else:
                return generate_token_response(str(user.id))
        except DoesNotExist:
            response = jsonify(
                OAuthErrorResponse(
                    "invalid_grant", "The username or password is incorrect."
                ).__dict__
            )
        response.status_code = 400
        return response


class RefreshTokenApi(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt_identity()
        return generate_token_response(user)


def generate_token_response(user: str) -> Response:
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    response = jsonify(
        TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            refresh_token=refresh_token
        ).__dict__
    )
    response.status_code = 200
    # set_access_cookies(response, access_token)
    return response
