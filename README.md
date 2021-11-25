# To start the project using docker (recommended)
- `docker-compose up` 

# To start the project using docker
1. create virtual env `python -m venv .venv`
2. activate `source .venv/bin/activate`
3. `python manage.py runserver`
# Overview
- This have POSTMAN collection
- This project is in Django
- Django admin can be accessed on http://localhost:8000/api/admin/ with username: admin & password: password.
- API Docs can be viewed on http://localhost:8000/api/swagger/ or http://localhost:8000/api/redoc/
- There is some data already populated. because I am using SQLlite, and the db is also commited in git.

# Features
- user can login and get token
- Get all expensed added by him
- Create expense
- create group
- get all groups
- create friends
- get friend
- update friend
- get expense for type: friend
- Get overall expense in splitwise
- settleup payment with a friend

 
# Authorization
- Token Based Authentication

# API Endpoints
## Unauthenticated APIs
- POST - `localhost:8000/api/users/token/` - create or get token
    - payload 
    {
        "username": "admin",
        "password": "password"
    }

## Token
- `Token 5121c747ea3ee0dff961cafcf812ac567800efb7`
## Authenticated API - send (Authorization: <Token> in header)
- GET - `localhost:8000/api/expense/` - to get all Expenses added by you
- GET - `localhost:8000/api/expense/` - Get all expensed
- POST - `localhost:8000/api/expense/` - Create Expense
    - payload
    {
        "amount": 200,
        "payer": 1,
        "payee": 2 
    }
- POST - `localhost:8000/api/group/` - create group
    - payload
    {
        "name": "Family",
        "users": [
            1,2
        ]
    }
- GET - `localhost:8000/api/group/` - get all groups
- POST - `localhost:8000/api/friend/` - create friends
    - payload 
        {
        "friends": [
            "vikram@gmail.com"
            ]
        }
- GET - `localhost:8000/api/friend/` - get friends
- PUT - `localhost:8000/api/friend/1/` - update friend
- GET - `localhost:8000/api/expense/friend/` - get expense for type: friend
- GET - `localhost:8000/api/expense/overall/` - your overall expense in splitwise
- POST - `localhost:8000/api/expense/settleup/` - to settleup payment with a friend
    - payload
        {
            "friend_email": "vikram@gmail.com"
        }

 # Some Screenshots!!
![image](https://user-images.githubusercontent.com/22349420/143372152-3dac2131-6b24-44ee-bd1c-5611c1d4616f.png)
    
![image](https://user-images.githubusercontent.com/22349420/143372228-4dd15d36-418d-4a72-8cd7-31c75386e7c0.png)
    
    
![image](https://user-images.githubusercontent.com/22349420/143372268-dbf6cae5-6f56-4510-ab16-8201ad2a5172.png)
    
    
![image](https://user-images.githubusercontent.com/22349420/143372304-29f94a95-c104-45bf-8c61-a6d20ff3c10c.png)
    
## From POSTMAN
 ![image](https://user-images.githubusercontent.com/22349420/143372839-05470d9c-365c-4209-944e-1991bfa5949e.png)
 ![image](https://user-images.githubusercontent.com/22349420/143372876-26b013df-0542-4303-9dac-ba36efa1f89e.png)
 ![image](https://user-images.githubusercontent.com/22349420/143372912-fbeb0988-026e-43bf-9179-2ade0a74aa9b.png)
 ![image](https://user-images.githubusercontent.com/22349420/143372964-19da3550-15a8-4344-8271-b16b13c6516b.png)



