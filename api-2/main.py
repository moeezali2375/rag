from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_query import rag_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/query")
async def query_document(request: QueryRequest):
    try:
        answer = rag_query(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing the query: {str(e)}"
        )
