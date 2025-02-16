from fastapi import FastAPI, Form, Query, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fpdf
import sqlite3
import os
import uvicorn

app = FastAPI()

# Konfiguracja katalogów statycznych i szablonów
STATIC_DIR = "static"
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory="templates")

# Baza danych SQLite
DB_FILE = "projekty.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projekty (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nazwa TEXT,
                        lokalizacja TEXT,
                        projekt_link TEXT,
                        obrazek TEXT
                    )''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

# Strona główna
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/zapisz_projekt")
def zapisz_projekt(
    nazwa: str = Form(...), 
    lokalizacja: str = Form(...), 
    projekt_link: str = Form(...), 
    obrazek: str = Form(...)  # Dodanie pola obrazka
):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projekty (nazwa, lokalizacja, projekt_link, obrazek) VALUES (?, ?, ?, ?)", 
                   (nazwa, lokalizacja, projekt_link, obrazek))
    conn.commit()
    conn.close()
    return JSONResponse(content={"message": "Projekt zapisany pomyślnie!"})

@app.get("/projekty")
def pobierz_projekty():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projekty")
    projekty = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "nazwa": p[1], "lokalizacja": p[2], "projekt_link": p[3], "obrazek": p[4]} for p in projekty]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
