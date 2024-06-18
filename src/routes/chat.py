from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from ..socket.connection import ConnectionManager
from ..model import LLMModel
from langchain_community.vectorstores import DocArrayInMemorySearch,Chroma
from langchain_community.embeddings import OllamaEmbeddings

chat = APIRouter()
manager = ConnectionManager()

# Initialise LLM
model = LLMModel()
vectordb = Chroma(persist_directory="./chromadb")
embedding_function  = OllamaEmbeddings(model=model.model_name)
vectordb._embedding_function = embedding_function
model.retriever = vectordb.as_retriever()

@chat.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try: 
        while True: 
            user_message = await websocket.receive_text()
            print(user_message)
            reply = model.answer_question(user_message)
            print(reply)
            await manager.send_message(reply, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)