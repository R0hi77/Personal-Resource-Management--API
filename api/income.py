from flask import Blueprint ,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from api.schema import Income_schema,Search
from pydantic import ValidationError
from api.models import Income,User
from api.extensions import db
from api import http_status_codes


income_bp = Blueprint('income',__name__,url_prefix='/api/income')

@income_bp.post('/create')
@jwt_required()
def create():
    user_id = get_jwt_identity()
    try:
        income_data = Income_schema(
            income=request.form['income'],
            details=request.form['details']
        )
    except ValidationError as e:
        return jsonify({'message':str(e)})
    
    income =Income(income=income_data.income,
                details=income_data.details,
                user_id=user_id)
    
    db.session.add(income)
    db.session.commit()
    
    return jsonify(
        {"income added":{"income amount":income.income,
                 "description":income.details
                 }}
    ),http_status_codes.HTTP_201_CREATED

@income_bp.post('/search')
@jwt_required()
def search_income():
    try:
        search= Search(query=request.form['query'])
        #should have an id condition
        #print(search)
        search_query="%{}%".format(search.query)
        results = Income.query.filter(Income.details.like(search_query)).all()
        if results:
            for result in results:
                return jsonify(
                    {
                        "income":result.income,
                        "description":result.details,
                        "timestamp":result.created
                    }
                ),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message":"Not found"})

    except ValidationError as e:
        return jsonify({"message":str(e)})
    
    
    

@income_bp.get('/all')
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
                    "description": i.details,
                    "created": i.created.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as string
                })

            return jsonify(income_list),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message": "No income item added yet"}),http_status_codes.HTTP_200_OK

    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return jsonify({'message': 'Internal Server Error'}),http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    
@income_bp.get('/one/<int:id>')
@jwt_required()
def get_one(id):
    income=Income.query.filter_by(id=id).first()
    if income:
        return jsonify(
            {'income detials':{
                "income":income.income,
                "description":income.details,
                "create":income.created
                
            }}
        ),http_status_codes.HTTP_200_OK
    
    else:
        return jsonify({'message':'No such  income item exist'})


@income_bp.post('/edit/<int:id>')
@jwt_required()
def edit(id):
    income=Income.query.filter_by(id=id).first()
    if income:
        try:
            income_data = Income_schema(
                income=request.form['income'],
                details=request.form['details'],
            )
        except ValidationError as e:
            return jsonify({"message":str(e)})
        
        income = Income(id=id,income=income_data.income,
                    details=income_data.details,
                    )
        
        db.session.merge(income)
        db.session.commit()

        return jsonify({'message':'income item editted'}),http_status_codes.HTTP_200_OK
    else:
        return jsonify({"message":"No such income item exists"})


@income_bp.delete('/delete/<int:id>')
@jwt_required()
def delete(id):
    income=Income.query.filter_by(id = id).first()
    if income is None:
        return jsonify({"message": "No such income exists"})
    else:
        db.session.delete(income)
        db.session.commit()
    return jsonify({'message':'income item deleted'}),http_status_codes.HTTP_200_OK