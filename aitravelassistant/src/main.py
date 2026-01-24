from fastapi import FastAPI, UploadFile
from contextlib import asynccontextmanager

#from openai import embeddings
from pydantic import BaseModel
from src.ingest import ingest_pdf
from src.vectorstores import init_qdrant
from src.retriever import retrieve_docs
from src.generator import generate_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources here (e.g., database connections, models)
    # Initialize Qdrant database
    print("Initializing Qdrant database...")
    init_qdrant()
    print("Database initialization complete.")   
    yield

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(req: QueryRequest):
    resp = generate_answer(req.query)
    #retrievedocs = await retrieve_docs(req.query)
    return {"response": resp}

@app.post("/upload")
async def upload_file(file: UploadFile = None):
    if not file:
        return {"message": "No file uploaded"}
        
    if not file.filename.endswith('.pdf'):
        return {"message": "Please upload a PDF file"}
    
    try:
        await ingest_pdf(file)
        return {"message": "File uploaded successfully"}
    except Exception as e:
        return {"message": f"Error processing file: {str(e)}"}

