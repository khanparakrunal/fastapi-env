from fastapi import FastAPI,Depends,status,Response,HTTPException
from matplotlib.pyplot import show, title
from requests import Session
from schemas import Blog,User,ShowUser,ShowBlog
import models
from database import engine,get_db
from hashing import Hash
from routers import blog


app= FastAPI()




models.Base.metadata.create_all(engine)




def get_db():
    db= SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get('/blog',tags=['blogs'])
def all(db:Session =Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs
    

@app.get('/blog/{id}',status_code=200,tags=['blogs'],response_model=ShowBlog)
def getblog(id,response: Response,db:Session =Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with id {id} is not available"}
    return blog



@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request: Blog,db:Session =Depends(get_db)):
    new_blog= models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def deleteBlog(id,db:Session =Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted!'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id,request : Blog,db:Session =Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with id {id} not found.")
    blog.update(request)
    db.commit()
    return 'updated!'


@app.post('/User',response_model=ShowUser,tags=['Users'])
def create_user(request: User,db:Session =Depends(get_db)):
    
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user

@app.get('/User/{user_id}',response_model=ShowUser,tags=['Users'])
def get_user(user_id:int,db:Session =Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with Id{user_id} NOT FOUND!")
    
    return user