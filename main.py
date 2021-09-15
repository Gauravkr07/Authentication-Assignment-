#Assignment to create login and sign_up function in fast api
import secrets
from pydantic import BaseModel,EmailStr
from pymongo import MongoClient
from fastapi import FastAPI,Depends,HTTPException,status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasicCredentials, HTTPBasic
from pymongo.errors import DuplicateKeyError
import config
from datetime import timedelta,datetime
from jose import jwt



"""In this project,we created two type of authentication system 
            1. by using module of HTTPBasicCredenticls from Fastapi.security library
            2. by creating token after verifing username and password                       
"""
SECRET_KEY=config.tokenkey
ALGORITHM =config.algorithm
security = HTTPBasic()
app=FastAPI()
client=MongoClient(config.database_server)
db=client[config.database]
mycoll=db["proo"]
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth_scheme=OAuth2PasswordBearer(tokenUrl="token")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class New_user(BaseModel):
    """here this model take username(Email only) and password """
    username:EmailStr
    password:str


#==================================================================================================================================


@app.post("/sign_up",tags=["Authentication"])
async def sign_up(new_user:New_user):
    """At this endpoint, we are using fastapi authentication system to store username and password in database"""
        try
            """Enter username """
            mycoll.insert({"username":new_user.username ,"password":hasshing(new_user.password)})
            return {"Successfully Registered"}
        except DuplicateKeyError:
            """It show when username already present in database"""
            print("Username is already present.Try another")
            return {"DuplicateKeyError"}

def hasshing(password):
    """"This hashing function convert plain password to hashed format password and return to sign_up function"""
    return pwd_context.hash(password)


#=============================================================================================================================
@app.get("/",tags=["welcome"])
def welcome(token:str=Depends(oauth_scheme)):
    """At this endpoints welcome function return token tokens"""
    return{"token":token}

def create_access_token(data:dict,expires_delta=timedelta):
    to_encode=data.copy()
    expire=datetime.utcnow()+ expires_delta
    to_encode.update({"exp":expire})
    encod_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encod_jwt


@app.post("/token",tags=["Authentication"])
async def sign_in(form_data:OAuth2PasswordRequestForm=Depends()):
    """At this endpoint, token generated if credentials are correct"""
    username=form_data.username
    password=form_data.password
    user = mycoll.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username ")

    l=mycoll.find_one({"username":username},{"password":1,"_id":0})
    j=list(*l.items())
    k=j[1]
    check=verify_password(password,k )

    if check==True:
        access_token=create_access_token(data={ "sub":username},expires_delta=timedelta(minutes=30))
        return {"access_token":access_token, "token_type": "bearer"}
    else:
        raise  HTTPException(status_code=404,detail="Password in misstyped,Retype again!")

def verify_password(plain_password,hashed_password):
     return pwd_context.verify(plain_password, hashed_password)
