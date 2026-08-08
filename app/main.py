from fastapi import FastAPI, Request, Form, Depends 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .database import SessionLocal, engine, Base
from . import models, auth, chatbot


Base.metadata.create_all(bind=engine) #for automatic table creation

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static") #get static files
templates = Jinja2Templates(directory="app/templates") #get template html files

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse("/login")

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(username: str = Form(...),
           email: str = Form(...),
           password: str = Form(...),
           db: Session = Depends(get_db)):
    
    auth.create_user(db, username, email, password)
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...),
          password: str = Form(...),
          db: Session = Depends(get_db)):
    
    user = auth.authenticate_user(db, username, password)
    if user:
        response = RedirectResponse("/chat", status_code=303)
        return response
    return {"error": "Invalid credentials"}

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
def chat(user_input: str = Form(...)):
    reply = chatbot.medical_response(user_input)
    return {"reply": reply}
