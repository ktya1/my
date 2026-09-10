import os
import secrets
import string

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


load_dotenv()

MAX_PASSWORD_LENGTH = int(os.getenv("MAX_PASSWORD_LENGTH", "64"))
DEFAULT_PASSWORD_LENGTH = int(os.getenv("DEFAULT_PASSWORD_LENGTH", "16"))

app = FastAPI(title="Password Generator")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "password": "",
            "length": DEFAULT_PASSWORD_LENGTH,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": True,
            "error": None,
            "max_length": MAX_PASSWORD_LENGTH,
        },
    )


@app.post("/generate")
def generate_password(
    request: Request,
    length: int = Form(DEFAULT_PASSWORD_LENGTH),
    use_upper: bool = Form(False),
    use_lower: bool = Form(False),
    use_digits: bool = Form(False),
    use_special: bool = Form(False),
):
    character_sets = []

    if use_upper:
        character_sets.append(string.ascii_uppercase) # заглавные буквы аски

    if use_lower:
        character_sets.append(string.ascii_lowercase)# маленькие буквы аскт

    if use_digits:
        character_sets.append(string.digits)# все цифры

    if use_special:
        character_sets.append(string.punctuation)# доп символы

    error = None
    password = ""

    if length < 1 or length > MAX_PASSWORD_LENGTH:
        error = f"Длина пароля должна быть от 1 до {MAX_PASSWORD_LENGTH}."

    elif not character_sets:
        error = "Выберите хотя бы один набор символов."

    elif length < len(character_sets):
        error = "Длина пароля слишком мала для выбранных наборов символов."

    else:
        characters = "".join(character_sets)

        # Гарантируем хотя бы один символ
        # из каждого выбранного набора.
        password_characters = [
            secrets.choice(character_set)
            for character_set in character_sets
        ]

        # Остальные символы выбираем из общего набора.
        password_characters.extend( #  добавляет все элементы из итерируемого объекта (например, другого списка, строки или кортежа) в конец существующего списка
            secrets.choice(characters)
            for _ in range(length - len(password_characters))
        )

        # Перемешиваем символы.
        secrets.SystemRandom().shuffle(password_characters)

        password = "".join(password_characters)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "password": password,
            "length": length,
            "use_upper": use_upper,
            "use_lower": use_lower,
            "use_digits": use_digits,
            "use_special": use_special,
            "error": error,
            "max_length": MAX_PASSWORD_LENGTH,
        },
    )
