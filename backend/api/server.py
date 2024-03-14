import os
import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from constants import UPLOAD_DIR
from database import get_db, Document, Session, print_documents_table_length

# Uncomment this if you wish to use hugging face
from hugging_face_provider import AgentProvider

# Uncomment this if you wish to use hugging face
# from openai_provider import AgentProvider

app = FastAPI()
agent_provider = AgentProvider()


class Query(BaseModel):
    question: str

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.post('/upload-pdf')
async def upload_pdf(file: UploadFile, db: Session = Depends(get_db)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as buffer:
        buffer.write(file.file.read())

    file_size = os.path.getsize(os.path.join(UPLOAD_DIR, file.filename))

    # Save Meta Data
    document = Document(filename=file.filename, file_size=file_size)
    db.add(document)
    db.commit()

    print_documents_table_length()

    # Extract Text
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        await agent_provider.process_pdf(file_path) 

        return {"filename": file.filename, "message": "File uploaded successfully"}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error uploading PDF: {str(e)}")
        
@app.post('/handle-query')
async def handle_query(query: Query):
    try:
        answer = agent_provider.get_answer(query.question)
        print(answer)
        return {"answer": answer}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
