from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import anthropic, os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY",""))
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=body.get("system","Tu es AfrIA Assistant. Réponds en français."),
        messages=[{"role":"user","content":body.get("message","")}]
    )
    return JSONResponse({"response": response.content[0].text})

@app.post("/commander")
async def commander(request: Request):
    data = await request.json()
    print(f"COMMANDE: {data}")
    return JSONResponse({"status":"ok"})
