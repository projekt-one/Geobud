from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import fpdf
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Aplikacja działa!"}

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
