from flask import Blueprint ,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from api.schema import Income_schema,Search
from pydantic import ValidationError
from api.models import Income,User
from api.extensions import db
from api import http_status_codes


income_bp = Blueprint('income',__name__,url_prefix='/api/income')

@income_bp.post('/')
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        income_data = Income_schema(
            income=data['income'],
            details=data['details']
        )
    except ValidationError as e:
        return jsonify({'message':str(e)})
    
    income =Income(income=income_data.income,
                details=income_data.details,
                user_id=user_id)
    
    db.session.add(income)
    db.session.commit()
    
    return jsonify(
        {"income amount":income.income,
                 "details":income.details,
                 "created":income.created,
                 "id":income.id
                 }
    ),http_status_codes.HTTP_201_CREATED

@income_bp.post('/search')
@jwt_required()
def search_income():
    try:
        query = request.args.get('query')
        #should have an id condition
        #print(search)
        search_query="%{}%".format(query)
        results = Income.query.filter(Income.details.like(search_query)|Income.income.like(search_query)).all()
        if results:
            for result in results:
                return jsonify(
                    {
                        "income":result.income,
                        "details":result.details,
                        "timestamp":result.created,
                        "id":result.id
                    }
                ),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message":"Not found"})

    except ValidationError as e:
        return jsonify({"message":str(e)})   

@income_bp.get('/')
@jwt_required()
def get_all():
    try:
        #identity = get_jwt_identity()

        # Query tasks with their associated user's username
        income = db.session.query(Income, User.username).join(User, Income.user_id == User.id).order_by(Income.created.desc()).all()
        
        if income:
            income_list = []
            for i, username in income:
                income_list.append({
                    "username": username,
                    "id": i.id,
                    "income": i.income,
                    "details": i.details,
                    "created": i.created.strftime('%Y-%m-%d %H:%M:%S') 
                })

            return jsonify(income_list),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message": "No income item added yet"}),http_status_codes.HTTP_200_OK

    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return jsonify({'message': 'Internal Server Error'}),http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    
@income_bp.get('/<int:id>')
@jwt_required()
def get_one(id):
    income=Income.query.filter_by(id=id).first()
    if income:
        return jsonify(
            {
                "income":income.income,
                "details":income.details,
                "create":income.created,
                "id":income.id
                
            }
        ),http_status_codes.HTTP_200_OK
    
    else:
        return jsonify({'message':'No such  income item exist'}),http_status_codes.HTTP_200_OK


@income_bp.put('/<int:id>')
@jwt_required()
def edit(id):
    income=Income.query.filter_by(id=id).first()
    data = request.get_json()
    if income:
        try:
            income_data = Income_schema(
                income=data['income'],
                details=data['details'],
            )
        except ValidationError as e:
            return jsonify({"message":str(e)})
        
        income = Income(id=id,income=income_data.income,
                    details=income_data.details,
                    )
        
        db.session.merge(income)
        db.session.commit()

        return jsonify({'id':income.id,
                        "income":income.income,
                        "details":income.details,
                        "created":income.created}),http_status_codes.HTTP_200_OK
    else:
        return jsonify({"message":"No such income item exists"}),http_status_codes.HTTP_200_OK


@income_bp.delete('/<int:id>')
@jwt_required()
def delete(id):
    income=Income.query.filter_by(id = id).first()
    if income is None:
        return jsonify({"message": "No such income exists"})
    else:
        db.session.delete(income)
        db.session.commit()
    return jsonify(),http_status_codes.HTTP_204_NO_CONTENT