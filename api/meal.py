from flask import Blueprint ,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from api.schema import Meal_schema, Search
from pydantic import ValidationError
from api.models import Meal,User
from api.extensions import db
from api import http_status_codes


meal_bp = Blueprint('meal',__name__,url_prefix='/api/meal')

@meal_bp.post('/create')
@jwt_required()
def create():
    user_id = get_jwt_identity()
    try:
        meal_data = Meal_schema(
            meal=request.form['meal'],
            description=request.form['meal_description']
        )
    except ValidationError as e:
        return jsonify({'message':str(e)})
    
    meal = Meal(meal=meal_data.meal,
                meal_description=meal_data.description,
                user_id=user_id)
    
    db.session.add(meal)
    db.session.commit()
    
    return jsonify(
        {"meal added":{"taask":meal.meal,
                 "description":meal.meal_description,
                 }}
    ),http_status_codes.HTTP_201_CREATED

@meal_bp.post('/search')
@jwt_required()
def search_meal():
    try:
        search= Search(query=request.form['query'])
        #should have an id condition
        #print(search)
        search_query="%{}%".format(search.query)
        results = Meal.query.filter(Meal.meal.like(search_query)).all()
        if results:
            for result in results:
                return jsonify(
                    {
                        "meal":result.meal,
                        "description":result.meal_description
                    }
                ),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message":"Not found"})

    except ValidationError as e:
        return jsonify({"message":str(e)})
    
    
    

@meal_bp.get('/all')
@jwt_required()
def get_all():
    try:
        #identity = get_jwt_identity()

        # Query tasks with their associated user's username
        meals = db.session.query(Meal, User.username).join(User, Meal.user_id == User.id).order_by(Meal.created.desc()).all()
        
        if meals:
            meal_list = []
            for meal, username in meals:
                meal_list.append({
                    "username": username,
                    "id": meal.id,
                    "meal": meal.meal,
                    "description": meal.meal_description,
                    "created": meal.created.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as string
                })

            return jsonify(meal_list),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message": "No meal item added yet"}),http_status_codes.HTTP_200_OK

    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return jsonify({'message': 'Internal Server Error'}),http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

@meal_bp.post('/edit/<int:id>')
@jwt_required()
def edit(id):
    meal=Meal.query.filter_by(id=id).first()
    if meal:
        try:
            meal_data = Meal_schema(
                meal=request.form['meal'],
                description=request.form['meal_description'],
            )
        except ValidationError as e:
            return jsonify({"message":str(e)})
        
        meal = Meal(id=id,meal=meal_data.meal,
                    meal_description=meal_data.description,
                    )
        
        db.session.merge(meal)
        db.session.commit()

        return jsonify({'message':'meal editted'}),http_status_codes.HTTP_200_OK
    else:
        return jsonify({"message":"No such meal item exists"})


@meal_bp.delete('/delete/<int:id>')
@jwt_required()
def delete(id):
    meal=Meal.query.filter_by(id = id).first()
    if meal is None:
        return jsonify({"message": "No such meal exists"})
    else:
        db.session.delete(meal)
        db.session.commit()
    return jsonify({'message':'meal item deleted'}),http_status_codes.HTTP_200_OK
