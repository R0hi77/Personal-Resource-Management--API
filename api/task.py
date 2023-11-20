from flask import Blueprint ,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from api.schema import Task_schema, Search
from pydantic import ValidationError
from api.models import Task,User
from api.extensions import db
from api import http_status_codes


task_bp = Blueprint('task',__name__,url_prefix='/api/task')

@task_bp.post('/create')
@jwt_required()
def create():
    user_id = get_jwt_identity()
    try:
        task_data = Task_schema(
            task=request.form['task'],
            description=request.form['description'],
            duetime=request.form['duetime'],
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
        {"task added":{"taask":task.task,
                 "description":task.description,
                 "duetime":task.duetime}}
    ),http_status_codes.HTTP_201_CREATED

@task_bp.post('/search')
@jwt_required()
def search_task():
    try:
        search_query = Search(query=request.form['query'])
    except ValidationError as e:
        return jsonify({"message":str(e)})
    
    results = Task.query.filter(Task.task.ilike(f'%{search_query.query}%')|Task.description.ilike(f'%{search_query}%')).all()
    if results:
        for result in results:
            return jsonify(
                {
                    "task":result.task,
                    "description":result.description
                }
            ),http_status_codes.HTTP_200_OK
    return jsonify({"message":"Not found"}),http_status_codes.HTTP_204_NO_CONTENT

@task_bp.get('/all')
@jwt_required()
def get_all():
    try:
        #identity = get_jwt_identity()

        # Query tasks with their associated user's username
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
            return jsonify({"message": "No tasks added yet"}),http_status_codes.HTTP_200_OK

    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return jsonify({'message': 'Internal Server Error'}),http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR

    
@task_bp.get('/one/<int:id>')
@jwt_required()
def get_one(id):
    task=Task.query.filter_by(id=id).first()
    if task:
        return jsonify(
            {'task':{
                "task":task.task,
                "description":task.description,
                "duetime":task.duetime,
                "duetime":task.created
            }}
        ),http_status_codes.HTTP_200_OK
    
    else:
        return jsonify({'message':'No task such exist'}),http_status_codes.HTTP_204_NO_CONTENT


@task_bp.post('/edit/<int:id>')
@jwt_required()
def edit(id):
    task=Task.query.filter_by(id=id).first()
    if task:
        try:
            task_data = Task_schema(
                task=request.form['task'],
                description=request.form['description'],
                duetime=request.form['duetime'],
            )
        except ValidationError as e:
            return jsonify({"message":str(e)})
        
        task = Task(id=id,task=task_data.task,
                    description=task_data.task,
                    duetime = task_data.duetime)
        
        db.session.merge(task)
        db.session.commit()

        return jsonify({'message':'task editted'}),http_status_codes.HTTP_200_OK
    else:
        return jsonify({"message":"no such task exists"}),http_status_codes.HTTP_204_NO_CONTENT


@task_bp.delete('/delete/<int:id>')
@jwt_required()
def delete(id):
    task=Task.query.filter_by(id = id).first()
    if task is None:
        return jsonify({"message": "No such task item exists"})
    else:
        db.session.delete(task)
        db.session.commit()
    return jsonify({'message':'Task deleted'}),http_status_codes.HTTP_200_OK

    
    
    


        


    

