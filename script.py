from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fpdf
import sqlite3
import os
import uvicorn

app = FastAPI()

# Tworzenie katalogu na pliki statyczne, jeśli nie istnieje
STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

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
                        projekt_link TEXT
                    )''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/zapisz_projekt")
def zapisz_projekt(nazwa: str = Form(...), lokalizacja: str = Form(...), projekt_link: str = Form(...)):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projekty (nazwa, lokalizacja, projekt_link) VALUES (?, ?, ?)", 
                   (nazwa, lokalizacja, projekt_link))
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
    return [{"id": p[0], "nazwa": p[1], "lokalizacja": p[2], "projekt_link": p[3]} for p in projekty]

# Pobieranie warunków zabudowy z MPZP (symulacja API)
@app.get("/mpzp")
def get_mpzp(lokalizacja: str = Query(..., title="Lokalizacja działki")):
    return {
        "lokalizacja": lokalizacja,
        "maks_wysokosc": "9m",
        "minimalna_odleglosc_od_granicy": "4m",
        "dach": "skośny lub płaski"
    }

# Analiza nasłonecznienia
@app.get("/analiza_slonca")
def analiza_slonca(lokalizacja: str = Query(..., title="Lokalizacja działki")):
    return {
        "lokalizacja": lokalizacja,
        "optymalny_kat": "30° względem południa",
        "zalecana_orientacja": "Południowa"
    }

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
