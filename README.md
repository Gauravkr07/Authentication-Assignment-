### Authentication-Assignment-
   
  
## Aim: 
      in this , we created authentication system on endpoint of FastAPI .
      
# Requirements:

-   python3
-   pip
-   FastAPI
-   Uvicorn server
-   python libraries:
    +   Pydantic
    +   pymongo
    +   passlib.context
    +   fastapi.security
    +   config module(containing environment variable) 
-   MongoDB
-   git
   
### To run the application on your local machine:
  
  # 1. Clone the repository:
        git clone "https://github.com/Gauravkr02/Authentication-Assignment-"
    
  # 2. Change the directory into the repository:
        'cd ./`Authentication-Assignment-'
       
  # 3. Create python virtual environment
        "python3 -m venv ./ver_env"
   
  # 4. Install python requirements:
        `pip install -r requirements.txt`
        
  # 5. To execute, Open the  pycharm application
     
+  Run the main.py 
          (We need uvicorn server to run Fastapi and  need to use localhost ip with portnumber.)
         
   + To run this we have two mathod:-
        + 1. configure run by importing module uvicorn)
        + 2. use uvicorn comman (uvicorn main:app --reaload)
       
+  Check 127.0.0.1/docs by using any system browser
  
+  when you visit this address then you find padlock sign in corner(represent that it's locked).
   
# 6. Sign_UP  At this endpint
       + where we can store data(username and passwoerd for sign_in) into MongoDB.
       + username and password received in plain form but password stored in hash format.
       + you need api authentication username and password to store these data in database.
    
        
# 7. sign_in At this endpoint
       + at first you have to enter username 
       + if username found then you have to enter password
       + Then authenticate fun match username with password
       + if matched then it generate token otherwise return error.
