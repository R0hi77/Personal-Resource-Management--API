from flask import Blueprint ,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from api.schema import Expense_schema,Search
from pydantic import ValidationError
from api.models import Expense,User
from api.extensions import db
from api import http_status_codes


expense_bp = Blueprint('expense',__name__,url_prefix='/api/expense')

@expense_bp.post('/')
@jwt_required()
def create():
    user_id = get_jwt_identity()
    try:
        expense_data = Expense_schema(
            expense=request.form['expense'],
            details=request.form['details']
        )
    except ValidationError as e:
        return jsonify({'message':str(e)})
    
    expense =Expense(expense=expense_data.expense,
                expense_details=expense_data.details,
                user_id=user_id)
    
    db.session.add(expense)
    db.session.commit()
    
    return jsonify(
        {"expense amount":expense.expense,
                 "details":expense.expense_details,
                 "id":expense.id,
                 "created":expense.created
                 }
    ),http_status_codes.HTTP_201_CREATED

@expense_bp.get('/')
@jwt_required()
def search_expense():
    
    
        query = request.args.get('query')
        search_query="%{}%".format(query)
        results = Expense.query.filter(Expense.expense_details.like(search_query)|Expense.expense.like(search_query)).all()
        if results:
            for result in results:
                return jsonify(
                    {
                        "expense":result.expense,
                        "description":result.expense_details,
                        "timestamp":result.created
                    }
                ),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message":"Not found"}),http_status_codes.HTTP_200_OK

@expense_bp.get('/')
@jwt_required()
def get_all():
    try:
        #identity = get_jwt_identity()

        # Query tasks with their associated user's username
        expenses = db.session.query(Expense, User.username).join(User, Expense.user_id == User.id).order_by(Expense.created.desc()).all()
        
        if expenses:
            expense_list = []
            for expense, username in expenses:
                expense_list.append({
                    "username": username,
                    "id": expense.id,
                    "expense": expense.expense,
                    "description": expense.expense_details,
                    "created": expense.created.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as string
                })

            return jsonify(expense_list),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message": "No expense item added yet"}),http_status_codes.HTTP_200_OK

    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return jsonify({'message': 'Internal Server Error'}),http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    
@expense_bp.get('/<int:id>')
@jwt_required()
def get_one(id):
    expense=Expense.query.filter_by(id=id).first()
    if expense:
        return jsonify(
            {   "id":expense.id,
                "expense":expense.expense,
                "details":expense.expense_details,
                "create":expense.created
                
            }
        ),http_status_codes.HTTP_200_OK
    
    else:
        return jsonify({'message':'No such  expense item exist'}),http_status_codes.HTTP_200_OK


@expense_bp.put('/<int:id>')
@jwt_required()
def edit(id):
    expense=Expense.query.filter_by(id=id).first()
    data = request.get_json()
    if expense:
        try:
            expense_data = Expense_schema(
                expense=data['expense'],
                details=data['details'],
            )
        except ValidationError as e:
            return jsonify({"message":str(e)})
        
        expense = Expense(id=id,expense=expense_data.expense,
                    expense_details=expense_data.details,
                    )
        
        db.session.merge(expense)
        db.session.commit()

        return jsonify({"expense":expense.expense,
                        "details":expense.expense_details,
                        "created":expense.created,
                        "id":expense.id}),http_status_codes.HTTP_200_OK
    else:
        return jsonify({"message":"No such expense item exists"})


@expense_bp.delete('/<int:id>')
@jwt_required()
def delete(id):
    expense=Expense.query.filter_by(id = id).first()
    if expense is None:
        return jsonify({"message": "No such expense exists"})
    else:
        db.session.delete(expense)
        db.session.commit()
    return jsonify(),http_status_codes.HTTP_204_NO_CONTENT