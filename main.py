from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF

app = FastAPI()

# Konfigurasi CORS agar Android bisa akses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan ["http://localhost:port"] kalau ingin lebih aman
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()

    try:
        # Buka PDF dari byte stream
        pdf_file = fitz.open(stream=contents, filetype="pdf")

        # Ekstrak teks per halaman
        extracted_lines = []
        for page in pdf_file:
            page_text = page.get_text().strip()
            lines = page_text.splitlines()
            extracted_lines.extend(lines)

        return {
            "filename": file.filename,
            "content": extracted_lines
        }

    except Exception as e:
        return {"error": str(e)}