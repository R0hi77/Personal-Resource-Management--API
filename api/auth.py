from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from api.schema import Register,Login
from api import http_status_codes
from api.models import User,RevokedTokens
from api.extensions import db
from pydantic import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity,get_jwt

auth_bp = Blueprint('auth',__name__,url_prefix='/api/auth')

@auth_bp.post('/register')
def signup():
    try:
        user_data= Register(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password'],
            confirm_password=request.form['confirm password']
                            )
        
    except ValidationError as e:
        return jsonify({'error':str(e)}),http_status_codes.HTTP_400_BAD_REQUEST
    
    user = User.query.filter_by(email=user_data.email).first()
    if user is not None:
        return jsonify({"message":"Email already exists"}),http_status_codes.HTTP_400_BAD_REQUEST
    
    else:
        user = User(
            username = user_data.username,
            email = user_data.email,
            password = generate_password_hash(user_data.password)
        )

        created_user={"name":user.username,"email":user.email}

        db.session.add(user)
        db.session.commit()
        print(user)
        return jsonify(
            {
                'messasge':'user created',
                'user data':created_user
                    
            }
        ),http_status_codes.HTTP_201_CREATED
    

@auth_bp.post('/login')
def login():
    try:
        user_data =Login(email=request.form['email'],password=request.form['password'])
    except ValidationError as e:
        return jsonify({"error":str(e)}),http_status_codes.HTTP_400_BAD_REQUEST
    
    user  = User.query.filter_by(email=user_data.email).first()
    if user and check_password_hash(user.password,user_data.password):
        refresh=create_refresh_token(identity=user.id)
        access=create_access_token(identity=user.id)

        return jsonify({'user':{
            "access taken":access,
            "refresh token":refresh,
            "username":user.username,
            "email":user.email
        }

        }),http_status_codes.HTTP_200_OK
    
    else:
        return jsonify({"error":"wrong credentials"}),http_status_codes.HTTP_401_UNAUTHORIZED

    
@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh():
    identity=get_jwt_identity()
    new_token= create_access_token(identity=identity)
    return jsonify({'new access token':new_token}),http_status_codes.HTTP_200_OK


@auth_bp.post('/logout')
@jwt_required()
def logout():
    jwt= get_jwt()

    jti = jwt['jti']

    token = RevokedTokens(token=jti)
    db.session.add(token)
    db.session.commit()

    return jsonify({'message':"User logged out succesfully"}),http_status_codes.HTTP_200_OK