from fastapi import FastAPI,UploadFile,File,Header
from typing import List,Annotated
import shutil,os
from werkzeug.utils import secure_filename
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import jwt
from jose import jwe


class Settings(BaseSettings):
    SECRET_KEY:str = '8a27dc7b112ed8e70ca02fa3778e04b6'
    AES_SECRET_KEY :bytes = b'1!\x14\xd8?\x03\xefm\xa0*1\xaf\xd8\xe7\x9b\xdcb\xed\xeek\xf8?\\:@\xed,\x06*\xcbYL'

settings = Settings()
app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_files/{tablename}")
async def index(tablename:str,files:List[UploadFile] = File(...),Authorization:Annotated[str | None,Header()] = None ):
    authorization_token = Authorization.split(" ")[1].encode('ascii')
    try:
        token = jwe.decrypt(authorization_token,settings.AES_SECRET_KEY)
        token = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"message":"Invalid Token"}
    except Exception as e:
         return {"message":"cant decrypt"}
    userid = token['userid']
    try:
        for _file in files:
        
            filename = secure_filename(_file.filename)
            path = os.path.join("UPLOADED_FILES",userid,tablename)
            os.makedirs(path,exist_ok=True)
            print(path)
            with open(os.path.join(path,filename),'wb') as f:
                shutil.copyfileobj(_file.file,f)
    except  Exception as e:
            return {"message":str(e)}
    finally:
            _file.file.close()
    
    return {"message":"Files Uploaded Successfully"}
            
    