from typing import Union

from fastapi import FastAPI, Depends, Request, Form
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory ="templates")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})

@app.post("/add")
def add(request:Request,title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code = status.HTTP_303_SEE_OTHER)

#질문1 : 2분 12초 쯤에 jinja2 코드가 갑자기 나타나는데 이 유튜버는 어떻게 한건지?? 아마 복붙인듯