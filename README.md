# Personal-Resource-Management--API
## API Overview
This a CRUD API with search functionality implemented in REST.It allows users to first of all perform account related operations like sign up sign in logout.
Users can also create edit delete search and view all personal resources.The API handles tasks,income,expenditure and meals. 
JSON Web Tokens was is used to secure the following endpoints all, edit and search and delete to ensure the right user is accessing the right resource 

## DOCUMENTATION

The API uses HTTP Methods to interract with resources. It supports the following endpoints:
### Authentication Endpoints
1.Registration
- `POST api/auth/register` - Create an account
  
- Requires the data below
  ```json
  {
  "username":"string",
  "email":"email",
  "password":"string",
  "confirm password":"string"
  }
  
2. Login
-`POST api/auth/login`

```json
Requires the following data
{
"email":"string",
"password":"string"
}

Returns the following

{ "access tokens":"string",
  "refresh tokens":"string",
  "username":"string",
"email":"string"
}

```
3. Logout
- `POST api/auth/logout`
  this endpoint rervokes the JWTs issued upon login

## Task Endpoint
1. Create Task
   `POST api/task/create`

   -Requires the data below
  ```json
  {
  "task":"string",
  "description":"string",
  "duetime":"string",
  }
```
2. Search for an existing task
   `POST api/task/search`

   - Requires the data below
  ```json
  {
  "query":"string",
  }
```
3. Edit a task
   `POST api/task/edit/<int:id>`

   -Requires the data below
  ```json
  {
  "task":"string",
  "description":"string",
  "duetime":"string",
  }
```
4. Get all tasks
`GET api/task/all`
- Returns all existing tasks created by current user
  

5. Delete a task
`POST api/delete/<int:id>`



### Meal Endpoints
1. Create Meal item
   `POST api/meal/create`

   -Requires the data below
  ```json
  {
  "Meal":"string",
  "meal_description":"string",
  }
```
2. Search for an existing meal item
   `POST api/meal/search`

   - Requires the data below
  ```json
  {
  "query":"string",
  }
Returns all entries similar the search query
```
3. Edit a meal
   `POST api/meal/edit/<int:id>`
   - Requires the data below
  ```json
  {
  "meal":"string",
  "meal_description":"string",
  }
```
4. Get all item
`GET api/meal/all`
   - Returns all existing meal items created by current user
  

5. Delete a item
`POST api/meal/delete/<int:id>`

### Income Enpoints

1. Create income item
   `POST api/income/create`

   -Requires the data below
  ```json
  {
  "income":"string",
  "details":"email",
  
  }
```
2. Search for an existing income
   `POST api/income/search`

   - Requires the data below
  ```json
  {
  "query":"string",
  }
Returns all entries similar the search query
```
3. Edit a income item
   `POST api/income/edit/<int:id>`

   -Requires the data below
  ```json
  {
  "task":"string",
  "details":"string",
  }
```
4. Get all income items
`GET api/income/all`
- Returns all existing income items created by current user
  
5. Delete income item
`POST api/income/delete/<int:id>`

## Expenditure Enpoints

1. Create expense item
   `POST api/expense/create`

   -Requires the data below
  ```json
  {
  "income":"string",
  "details":"email",
  
  }
```
2. Search for an existing expenditure
   `POST api/expense/search`

   - Requires the data below
  ```json
  {
  "query":"string",
  }
Returns all entries similar the search query
```
3. Edit expenditure
   `POST api/expense/edit/<int:id>`

   -Requires the data below
  ```json
  {
  "task":"string",
  "details":"string",
  }
```
4. Get all expenditure
`GET api/expense/all`
- Returns all existing expenditure created by current user
  
5. Delete an expenditure item
`POST api/expense/delete/<int:id>`

## Pydantic is used to validate user entries and Flask SqlAlchmy to interract with the database
