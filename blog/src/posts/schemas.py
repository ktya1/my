from pydantic import BaseModel

class PostCreate(BaseModel):
    title:str
    content:str

class PostRead(BaseModel):
    title:str
    content:str
    id:int

class PostUpdatePatch(BaseModel):
    title:str | None = None 
    content:str | None = None
    
#put более жесткий 
class PostPut(BaseModel):
    title:str
    content:str