import secrets
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI,Depends,HTTPException,status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasicCredentials, HTTPBasic
#from mongoengine import Document,StringField
from enum import unique
from pymongo.errors import DuplicateKeyError


security = HTTPBasic()
app=FastAPI()
client=MongoClient("mongodb://localhost:27017/")
db=client["Userinfo"]
mycoll=db["proo"]
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth_scheme=OAuth2PasswordBearer(tokenUrl="token")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class New_user(BaseModel):
    username:str
    password:str

#==================================================================================================================================
@app.get("/",tags=["welcome"])
def welcome(token:str=Depends(oauth_scheme)):
    return{"token":token}
#==================================================================================================================================
@app.post("/sign_up",tags=["Authentication"])

async def sign_up(new_user:New_user,credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "hel")
    correct_password = secrets.compare_digest(credentials.password, "say")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password",headers={"WWW-Authenticate": "Basic"},)
    else:
        try:
            mycoll.insert({"username":new_user.username ,"password":hasshing(new_user.password)})
            return {"Successfully Registered"}
        except DuplicateKeyError:
            print("Username is already present.Try another")
            return {"DuplicateKeyError"}

def hasshing(password):
    return pwd_context.hash(password)

@app.post("/token",tags=["Authentication"])
async def sign_in(form_data:OAuth2PasswordRequestForm=Depends()):
    username=form_data.username
    password=form_data.password
    if authenticate(username,password):
        return {"Access token":username,"token_type":"bearer"}
    else:
        raise HTTPException(status_code=400,detail="incorrect username or password")

async def authenticate(username,password):
    import ipdb;
    ipdb.set_trace()
    user=  mycoll.find_one({"username":username})
    if user:
        #mycoll.aggregate()
        veri=pwd_context.verify(password,**(mycoll.find_one(username,password)))
        print(veri)
        return  veri
    else:
        return False
