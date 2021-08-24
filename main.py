
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI,Depends,HTTPException
from passlib.context import CryptContext
from fastapi.security import  OAuth2PasswordBearer,OAuth2PasswordRequestForm
#from mongoengine import Document,StringField
from enum import unique
from pymongo.errors import DuplicateKeyError

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
async def sign_up(new_user:New_user):
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
    user=mycoll.find_one({"username":username})

    if user:
         veri=pwd_context.verify(password,**(mycoll.find_one(password)))
         return veri
    # user=json.loads(User.objects.get(username=username).to_json())
    else:
        return False
