from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app= FastAPI()

@app.get('/blog')
def index(limit=10,published:bool =True,sort: Optional[str]=None):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}

@app.get('/blog/{id}')
def blog(id:int):
    return {'data':id}

@app.get('/blog/{id}/comments')
def blogcomments(id:int):
    return {'Comments':id}
@app.get('/about')
def about():
    return {'data':{'about page'}}

class Blog(BaseModel):
    title: str
    body:str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request:Blog):
    return {'data':f"Blog is create with Title:{request.title}"}
    