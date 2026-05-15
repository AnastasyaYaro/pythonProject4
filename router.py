from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .models import FormData      # ← тоже относительный импорт

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Главная страница – форма
@router.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Обработчик отправки формы
@router.post("/submit")
async def submit_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    comment: str = Form(None),
    file: UploadFile = File(None),
):
    # 1️⃣ Валидация через pydantic
    try:
        data = FormData(name=name, email=email, comment=comment)
    except Exception as exc:
        # Вернём форму с сообщением об ошибке
        return templates.TemplateResponse(
            "form.html",
            {
                "request": request,
                "message": f"Ошибка валидации: {exc}",
                "message_type": "error",
            },
        )

    # 2️⃣ Обработка файла (если пришёл)
    file_info = None
    if file:
        content = await file.read()
        file_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        }
        # здесь можно сохранить файл на диск:
        # with open(f"uploads/{file.filename}", "wb") as f:
        #     f.write(content)

    # 3️⃣ Логика «тестирования» – просто выводим данные в консоль
    print("\n--- Получены данные формы ---")
    print(data.json())
    if file_info:
        print("Файл:", file_info)

    # 4️⃣ Перенаправляем обратно к форме с success‑сообщением
    response = templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "message": "Форма успешно отправлена!",
            "message_type": "success",
        },
    )
    return response