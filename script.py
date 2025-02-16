from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 📌 Tworzymy folder na pliki statyczne, jeśli nie istnieje
STATIC_DIR = "static"
IMAGES_DIR = "static/images"

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# 📌 Montujemy folder "static" do obsługi plików statycznych
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory="templates")

# 📌 Strona główna
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 📌 Obsługa obrazków, aby były wyświetlane zamiast pobierane
@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(IMAGES_DIR, image_name)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Obraz nie znaleziony")

    with open(image_path, "rb") as image_file:
        return Response(content=image_file.read(), media_type="image/jpeg")  # Wymusza wyświetlanie zamiast pobierania

# 📌 Endpoint do zapisywania nowego projektu
@app.post("/zapisz_projekt")
def zapisz_projekt(
    nazwa: str = Form(...), 
    lokalizacja: str = Form(...), 
    projekt_link: str = Form(...), 
    obrazek: str = Form(...)
):
    return JSONResponse(content={"message": "Projekt zapisany pomyślnie!", "obrazek": obrazek})

# 📌 Pobieranie listy projektów
@app.get("/projekty")
def pobierz_projekty():
    return [
        {
            "nazwa": "Projekt 100m²",
            "lokalizacja": "Lokalizacja A",
            "projekt_link": "https://przykladowylink1.com",
            "obrazek": "/images/projekt1.jpg"  # Ścieżka do obrazu w API
        },
        {
            "nazwa": "Projekt 150m²",
            "lokalizacja": "Lokalizacja B",
            "projekt_link": "https://przykladowylink2.com",
            "obrazek": "/images/projekt2.jpg"  # Ścieżka do obrazu w API
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
