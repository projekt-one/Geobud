from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 📌 Upewniamy się, że folder statyczny istnieje
STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# 📌 Montujemy folder "static" jako serwer plików statycznych
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory="templates")

# 📌 Strona główna
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 📌 Obsługa obrazków, żeby się wyświetlały zamiast pobierać
@app.get("/static/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("static/images", image_name)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path, media_type="image/jpeg")  # Wymusza wyświetlanie zamiast pobierania

# 📌 Endpoint do zapisania nowego projektu
@app.post("/zapisz_projekt")
def zapisz_projekt(nazwa: str = Form(...), lokalizacja: str = Form(...), projekt_link: str = Form(...), obrazek: str = Form(...)):
    return JSONResponse(content={"message": "Projekt zapisany pomyślnie!", "obrazek": obrazek})

# 📌 Pobieranie listy projektów
@app.get("/projekty")
def pobierz_projekty():
    return [
        {"nazwa": "Projekt 100m²", "lokalizacja": "Lokalizacja A", "projekt_link": "https://przykladowylink1.com", "obrazek": "/static/images/projekt1.jpg"},
        {"nazwa": "Projekt 150m²", "lokalizacja": "Lokalizacja B", "projekt_link": "https://przykladowylink2.com", "obrazek": "/static/images/projekt2.jpg"}
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
