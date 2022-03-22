import uvicorn
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/auth/redirect")
def post_auth_redirect(clientid: str = Form(...)):
    return RedirectResponse(f"https://dribbble.com/oauth/authorize?client_id={clientid}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/auth")
def post_auth(code: str, request: Request):
    return templates.TemplateResponse("auth.html", {"request": request, "code": code})

@app.post("/auth/generate")
def post_auth_generate(request: Request, code: str = Form(...), clientid: str = Form(...), clientsecret: str = Form(...)):
    r = requests.post(f"https://dribbble.com/oauth/token?client_id={clientid}&client_secret={clientsecret}&code={code}")
    token = json.loads(r.text)["access_token"]
    return templates.TemplateResponse("done.html", {"request": request, "token": token})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)