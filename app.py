from fastapi import FastAPI, Request
import uvicorn
from text_processor import process_text

app = FastAPI()

@app.post("/process_text")
async def process_text_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("text", "")
    persona = data.get("persona", "friendly_mentor")  # Default persona
    
    # Get AI response
    ai_response = process_text(user_input, persona)
    
    return {"response": ai_response}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
