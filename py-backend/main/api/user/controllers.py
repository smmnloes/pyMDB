from flask import request
from flask_restful import Resource

from services.user import user_service


class Login(Resource):
    def post(self):
        return user_service.login_user(request.json['email'], request.json['password'])


class Register(Resource):
    def post(self):
        return user_service.register_user(request.json['email'], request.json['password'], request.json['username'])
