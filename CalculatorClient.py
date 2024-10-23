from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import calculator_agent

app = FastAPI(
    title="Calculator Agent API",
    description="An API to interact with the Calculator Agent.",
    version="1.0.0",
)
# ENSURE ALL METHODS ARE MULTI THREAD SAFE
# IF METHODS ARE NOT THREAD DEPENDENT THEN OKAY AS IS

class QueryRequest(BaseModel):
    user_id: str
    input_text: str

class QueryResponse(BaseModel):
    response: str

class ActivateRequest(BaseModel):
    user_id: str


@app.post("/execute", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    """
    Endpoint to process a user query and return the agent's response.
    """
    
    try:
        response = calculator_agent(request.input_text)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/activate")
def activate(request: ActivateRequest):
    user_id = request.user_id
    # COMPLETE ANY ACTIVATION THAT NEEDS TO BE DONE PER USER
    # THIS EXAMPLE SIMPLY ALERTS THAT THE AGENT IS READY FOR EXECUTION

    return {
        "message":f"Ready to handle traffic for User: {user_id}"
    }