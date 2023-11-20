from pydantic import BaseModel,validator,ValidationError,Field
import re
from datetime import date
class Register(BaseModel):
    username:str
    email:str
    password:str =Field(min_length=8,max_length=32)
    confirm_password:str

    # @validator('password')
    # def validate_password_string(cls,v):
    #     if not re.search(r'[^A-Za-z0-9]',v):
    #         raise ValidationError("Password must contain at least one special character")
    #     return v

    # @validator('confirm_password')
    # def validate_password_match(cls,v,values, **kwargs):
    #     if 'password' in values and v!=values['password']:
    #         raise ValidationError('passwords do not match')
    #     return v

class Login(BaseModel):
    email:str
    password:str

# for text type data
class Search(BaseModel):
    query:str

# class Search_nums(BaseModel):
#     query:float
    
class Task_schema(BaseModel):
    task:str
    description:str
    duetime:date

class Meal_schema(BaseModel):
    meal:str
    description:str

class Income_schema(BaseModel):
    income:float
    details:str

class Expense_schema(BaseModel):
    expense:float
    details:str



    
    




    
    

