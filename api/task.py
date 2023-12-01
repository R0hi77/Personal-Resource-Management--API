from flask import Blueprint ,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from api.schema import Task_schema, Search
from pydantic import ValidationError
from api.models import Task,User
from api.extensions import db
from api import http_status_codes


task_bp = Blueprint('task',__name__,url_prefix='/api/task')

@task_bp.post('/')
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        task_data = Task_schema(
            task=data['task'],
            description=data['description'],
            duetime=data['duetime'],
        )
    except ValidationError as e:
        return jsonify({'message':str(e)})
    
    task = Task(task=task_data.task,
                description=task_data.description,
                duetime=task_data.duetime,
                user_id=user_id)
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(
        {"task":task.task,
                 "description":task.description,
                 "duetime":task.duetime,
                 "id":task.id}
    ),http_status_codes.HTTP_201_CREATED

@task_bp.get('/')
@jwt_required()
def search_for_a_task():
    
    query = request.args.get('query')
    results = Task.query.filter(Task.task.ilike(f'%{query}%')|Task.description.ilike(f'%{query}%')).all()
    if results:
        for result in results:
            return jsonify(
                {
                    "task":result.task,
                    "description":result.description,
                    "id":result.id,
                    "duetime":result.duetime,
                    "created":result.created
                }
            ),http_status_codes.HTTP_200_OK
    return jsonify({"message":"Not found"}),http_status_codes.HTTP_200_OK

@task_bp.get('/')
@jwt_required()
def get_all():
    try:
        tasks = db.session.query(Task, User.username).join(User, Task.user_id == User.id).order_by(Task.created.desc()).all()
        
        if tasks:
            task_list = []
            for task, username in tasks:
                task_list.append({
                    "username": username,
                    "id": task.id,
                    "task": task.task,
                    "description": task.description,
                    "duetime": task.duetime.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
                    "created": task.created.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as string
                })

            return jsonify(task_list),http_status_codes.HTTP_200_OK
        else:
            return jsonify({"message": "Nothing found"}),http_status_codes.HTTP_200_OK

    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return jsonify({'message': 'Internal Server Error'}),http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    
@task_bp.get('/<int:id>')
@jwt_required()
def get_one(id):
    task=Task.query.filter_by(id=id).first()
    if task:
        return jsonify(
            {
                "task":task.task,
                "description":task.description,
                "duetime":task.duetime,
                "duetime":task.created
            }
        ),http_status_codes.HTTP_200_OK
    
    else:
        return jsonify({'message':'No task such exist'}),http_status_codes.HTTP_200_OK


@task_bp.put('/<int:id>')
@jwt_required()
def edit(id):
    task=Task.query.filter_by(id=id).first()
    data = request.get_json()
    if task:
        try:
            task_data = Task_schema(
                task=data['task'],
                description=data['description'],
                duetime=data['duetime'],
            )
        except ValidationError as e:
            return jsonify({"message":str(e)})
        
        task = Task(id=id,task=task_data.task,
                    description=task_data.task,
                    duetime = task_data.duetime)
        
        db.session.merge(task)
        db.session.commit()

        return jsonify({"task":task.task,
                        "description":task.description,
                        "duetime":task.duetime,
                        "id":task.id}),http_status_codes.HTTP_200_OK
    else:
        return jsonify({"message":"no such task exists"}),http_status_codes.HTTP_200_OK


@task_bp.delete('/<int:id>')
@jwt_required()
def delete(id):
    task=Task.query.filter_by(id = id).first()
    if task is None:
        return jsonify({"message": "No such task item exists"})
    else:
        db.session.delete(task)
        db.session.commit()
    return jsonify(),http_status_codes.HTTP_204_NO_CONTENT

    
    
    


        


    

