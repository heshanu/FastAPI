from typing import Union
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from model.PostModel import Post
from random import randrange

app = FastAPI()

myPosts=[
    {"id":1,"title":"Title of post 1","content":"Content of post 1"},
    {"id":2,"title":"Title of post 2","content":"Content of post 2"}
]

def findPost(id):
    for p in myPosts:
        if p['id']==id:
            return p

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
def getPost(id:int):
    post = findPost(id)
    return {"post detail":post}

@app.get("/posts/latest")
def getLatestPost():
    latestPost= myPosts[len(myPosts)-1]
    return {"details":latestPost}