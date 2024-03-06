import warnings
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from main import answer_question  # Import from your main.py
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import chain as pgchain
warnings.simplefilter("ignore")
app = FastAPI()  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    
    
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# add_routes(app, pgchain, path="/pipeline")
@app.post("/pipeline")
async def ask_question(data: Query):
    answer, source_docs = answer_question(data.question)

    # Prepare the response with source documents (adjust formatting as needed)
    response_data = {
        "answer": answer,
        "sources": [{"content": doc.page_content} for doc in source_docs] 
    }

    return response_data 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
