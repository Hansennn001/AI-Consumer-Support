from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.customer_agent import customer_agent
from app.api.error_handler import global_exception_handler
from app.database.db import (
    get_logs,
    get_pending_reviews
)

import uuid
import time



app = FastAPI(
    title="AI Customer Support Agent",
    version="1.0"
)



app.add_exception_handler(
    Exception,
    global_exception_handler
)



class SupportRequest(BaseModel):

    email: str



@app.get("/")
def home():

    return {

        "status": "running",

        "message": "AI Customer Support Agent API"

    }



@app.post("/chat")
def chat(request: SupportRequest):


    request_id = str(uuid.uuid4())


    conversation_id = request_id



    start_time = time.time()



    state = {


    "request_id": request_id,


    "conversation_id": conversation_id,


    "customer_id": request_id,


    "email": request.email,


    "conversation_history": [],


    "category": "",


    "risk_level": "",


    "risk_reason": "",


    "contact_count": 0,


    "use_tool": False,


    "tool_name": "",


    "tool_query": "",


    "tool_result": "",


    "response": "",


    "requires_human": False,


    "status": "",


    "processing_time": 0.0

    }  



    result = customer_agent.invoke(state)



    result["processing_time"] = round(

        time.time() - start_time,

        3

    )



    if result["requires_human"]:


        result["status"] = "pending_review"


    else:


        result["status"] = "completed"



    return result





@app.get("/logs")
def logs():

    return get_logs()

@app.get("/review/pending")
def pending_reviews():

    return get_pending_reviews()