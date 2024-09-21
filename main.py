from typing import Union
from fastapi import FastAPI,status,Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from model.PostModel import Post
from random import randrange

app = FastAPI()

myPosts=[
    {"id":1,"title":"Title of post 1","content":"Content of post 1"},
    {"id":2,"title":"Title of post 2","content":"Content of post 2"}
]

def findPost(id:int):
    for p in myPosts:
        if p['id']==id:
            return p

def findIndexPost(id:int):
    for i,p in enumerate(myPosts):
        if p['id']==id:
            return i

@app.get("/posts")
def getPosts():
    return {"data":myPosts}

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