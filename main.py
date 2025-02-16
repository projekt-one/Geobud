from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fpdf
import sqlite3
import os
import uvicorn

app = FastAPI()

# Tworzenie katalogów na pliki statyczne i szablony
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
DB_FILE = "projekty.db"

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Inicjalizacja bazy danych
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
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Zapis projektu do bazy
@app.post("/zapisz_projekt")
def zapisz_projekt(
    nazwa: str = Form(...),
    lokalizacja: str = Form(...),
    projekt_link: str = Form(...),
    obrazek: str = Form(...)
):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projekty (nazwa, lokalizacja, projekt_link, obrazek) VALUES (?, ?, ?, ?)", 
                   (nazwa, lokalizacja, projekt_link, obrazek))
    conn.commit()
    conn.close()
    return JSONResponse(content={"message": "Projekt zapisany pomyślnie!"})

# Pobieranie projektów z bazy
@app.get("/projekty")
def pobierz_projekty():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projekty")
    projekty = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "nazwa": p[1], "lokalizacja": p[2], "projekt_link": p[3], "obrazek": p[4]} for p in projekty]

# Generowanie wniosku PDF
@app.post("/generate_pdf")
def generate_pdf(dzialka: str = Form(...), urzad: str = Form(...)):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Wniosek o Warunki Zabudowy", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Adres działki: {dzialka}", ln=True)
    pdf.cell(200, 10, txt=f"Urzad: {urzad}", ln=True)

    filename = "wniosek.pdf"
    pdf.output(filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# NOWY KOD – Endpoint główny zwracający stronę HTML
