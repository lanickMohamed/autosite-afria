from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import anthropic, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    msg = body.get("message", "")
    system = body.get("system", "Tu es AfrIA Assistant. Réponds en français.")
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=system,
        messages=[{"role": "user", "content": msg}]
    )
    return JSONResponse({"response": response.content[0].text})

@app.post("/commander")
async def commander(request: Request):
    data = await request.json()
    print(f"COMMANDE: {data}")
    return JSONResponse({"status": "ok"})
