from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import AnalyticsAgent
import uvicorn

app = FastAPI()
agent = AnalyticsAgent()

class QuestionRequest(BaseModel):
    store_id: str
    question: str
    access_token: str = None

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        response = agent.process(request.store_id, request.question, request.access_token)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
