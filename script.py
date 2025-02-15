from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import fpdf
import sqlite3
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Obsługa plików statycznych (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Plik bazy danych SQLite
DB_FILE = "projekty.db"

def init_db():
    """ Inicjalizacja bazy danych SQLite """
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
    """ Uruchamiane przy starcie aplikacji """
    init_db()

@app.post("/zapisz_projekt")
def zapisz_projekt(nazwa: str = Form(...), lokalizacja: str = Form(...), projekt_link: str = Form(...)):
    """ Zapisanie projektu do bazy danych """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projekty (nazwa, lokalizacja, projekt_link) VALUES (?, ?, ?)", 
                       (nazwa, lokalizacja, projekt_link))
        conn.commit()
        conn.close()
        return JSONResponse(content={"message": "Projekt zapisany pomyślnie!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projekty")
def pobierz_projekty():
    """ Pobranie wszystkich zapisanych projektów """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projekty")
    projekty = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "nazwa": p[1], "lokalizacja": p[2], "projekt_link": p[3]} for p in projekty]

@app.get("/mpzp")
def get_mpzp(lokalizacja: str = Query(..., title="Lokalizacja działki")):
    """ Pobieranie przykładowych warunków zabudowy """
    return {
        "lokalizacja": lokalizacja,
        "maks_wysokosc": "9m",
        "minimalna_odleglosc_od_granicy": "4m",
        "dach": "skośny lub płaski"
    }

@app.get("/analiza_slonca")
def analiza_slonca(lokalizacja: str = Query(..., title="Lokalizacja działki")):
    """ Analiza optymalnej orientacji budynku względem słońca """
    return {
        "lokalizacja": lokalizacja,
        "optymalny_kat": "30° względem południa",
        "zalecana_orientacja": "Południowa"
    }

@app.post("/generate_pdf")
def generate_pdf(dzialka: str = Form(...), urzad: str = Form(...)):
    """ Generowanie pliku PDF z wnioskiem o warunki zabudowy """
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
    uvicorn.run(app, host="0.0.0.0", port=10000)
