from fastapi import FastAPI
import uvicorn
from src.routes import chat


app = FastAPI()
app.include_router(chat.chat)



@app.get('/')
def root(): 
    return {"message": 'Homepage reached!'}

if __name__ == '__main__':
    uvicorn.run('main:app', port=5000)