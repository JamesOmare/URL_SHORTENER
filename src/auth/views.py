from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
import validators
from ..models.user import User, db
from ..models.bookmark import Bookmark
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': 'Password is too short'}), HTTPStatus.BAD_REQUEST
    
    if len(username) < 3:
        return jsonify({'error': 'Username is too short'}), HTTPStatus.BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':'Email is not valid'}), HTTPStatus.BAD_REQUEST

    if User.query.filter_by(email = email).first() is not None:
        return jsonify({'error':'Email is taken'}), HTTPStatus.CONFLICT

    if User.query.filter_by(username = username).first() is not None:
        return jsonify({'error':'That username is taken'}), HTTPStatus.CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(

        username = username,
        password = pwd_hash,
        email = email

    )

    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            'message': 'User created',
            'user': {
                'username': username,
                'email': email
            }
        }
    ), HTTPStatus.CREATED
   

@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email = email).first()

    if user:
        is_pass_valid = check_password_hash(user.password, password)

        if is_pass_valid:
            refresh = create_refresh_token(identity = user.id)
            access = create_access_token(identity = user.id)

            return jsonify({

                'user':{

                    'access_token': access,
                    'refresh_token': refresh,
                    'username': user.username,
                    'email': user.email
                }

            }), HTTPStatus.OK


    return jsonify({'error': 'Wrong credentials'}), HTTPStatus.UNAUTHORIZED

 


@auth.get('/me')
@jwt_required()
def me(): 
    #jwt_identity returns user identity
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).first()

    return jsonify(

        {
            'username': user.username,
            'email':user.email
        }

    ), HTTPStatus.OK

@auth.post('/token/refresh')
@jwt_required(refresh = True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity = identity)

    return jsonify({

        'access_token': access

    }), HTTPStatus.CREATED