from flask import Flask
from .extensions import db
import os
from api.auth import auth_bp
from api.task import task_bp
from api.meal import meal_bp
from api.income import income_bp
from api.expense import expense_bp
from flask_jwt_extended import JWTManager
from api.models import RevokedTokens
from flask_swagger_ui import get_swaggerui_blueprint
#from dotenv import load_dotenv
from flasgger import Swagger,swag_from
from api.config.swagger import template,swagger_config

#import psycopg2


def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    user=os.getenv("POSTGRES_USER")
    password=os.getenv("POSTGRES_PASSWORD")
    host=os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database=os.getenv("POSTGRES_DATABASE")
    

    DB_URL= 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=user,pw=password,host=host,port=port,db=database)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=DB_URL,
            JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
            SWAGGER={'title': "Personal Resource Manager API",
                'uiversion': 3}
        )
        

    else: 
        app.config.from_mapping(test_config)
    
    # swagger configurations
    SWAGGER_URL = '/swagger'   
    API_URL ='/static/swagger.json'
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'application_name':"Personal Resource Manager"}
    )

    #extension initializations
    db.app =app
    db.init_app(app)
    JWTManager(app)

    # Swagger(app,config=swagger_config,template=template )
    @app.post('/')
    @swag_from('./docs/auth/register.yml')
    def index():
        pass


    #blueprint registrations
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(meal_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(expense_bp)

    app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)

    #token block list
    @JWTManager().token_in_blocklist_loader
    def token_in_blockedlist_callback(jwt_header,jwt_data):
        jti=jwt_data['jti']
        token = RevokedTokens.query().filter_by(token=jti).first()
        return token is not None



    return app