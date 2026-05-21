from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, get_db, Base
from models import UserForm

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse))))

async def home(request: Request, db: Session = Depends(get_db)):
    rows = db.query(UserForm).order_by(UserForm.id.desc()).all()
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "rows": rows},
    )

ryrthfhjfgjtjrtjrthr

@app.post("/submit")
async def submit_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    age: int = Form(None),
    message: str = Form(None),
    db: Session = Depends(get_db),
):
    # 1️⃣ Сохраняем в БД
    db_user = UserForm(
        username=username,
        email=email,
        age=age,
        message=message,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 2️⃣ Перенаправляем обратно на GET /
    # 303 See Other – лучший статус для POST‑REDIRECT‑GET
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Создаём таблицы при запуске
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True
    )