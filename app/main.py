from typing import Union
from fastapi import FastAPI,status,Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from model.PostModel import Post
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_CONFIG

app = FastAPI()

def get_db_connection():
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# myPosts=[
#     {"id":1,"title":"Title of post 1","content":"Content of post 1"},
#     {"id":2,"title":"Title of post 2","content":"Content of post 2"}
# ]

def findPost(id:int):
    for p in myPosts:
        if p['id']==id:
            return p

def findIndexPost(id:int):
    for i,p in enumerate(myPosts):
        if p['id']==id:
            return i

@app.get("/items/")
def read_items():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM products")
        items = cursor.fetchall()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.post("/post")
def createPost(payLoad:Post):
    postDict =payLoad.dict() 
    postDict['id']=randrange(0,100)
    myPosts.append(postDict) 
   # print(myPosts)   
    return {"data":payLoad}

@app.get("/post/{id}")
def getPost(id:int,response:Response):
    post = findPost(id)
    if post==None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
        #return Response(status_code=status.HTTP_404_NOT_FOUND)
    return {"post detail":post}

@app.get("/posts/latest")
def getLatestPost():
    latestPost= myPosts[len(myPosts)-1]
    return {"details":latestPost}

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id:int):
    index=findIndexPost(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not exists")
    myPosts.pop(index)

    return {"message":"post was successfully deleted"}

@app.put("/post/{id}")
def updatePost(id:int,post:Post):
    index=findIndexPost(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not exists")
    postDict=post.dict()
    postDict['id']=id
    myPosts[index]=postDict
    return {"message":postDict}    