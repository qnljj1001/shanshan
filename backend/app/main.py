from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.services import llm

app = FastAPI(title="AI Doc Assistant")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
async def home():
    return {"status":"ok"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = llm.chat(request.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="LLM request failed") from exc
    return ChatResponse(answer=answer)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)