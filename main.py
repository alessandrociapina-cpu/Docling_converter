from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from docling.document_converter import DocumentConverter
import tempfile
import os

app = FastAPI()

# Permite que o seu PWA acesse a API de qualquer lugar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Após testar, substitua "*" pela URL do seu GitHub Pages por segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o Docling
converter = DocumentConverter()

@app.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF.")
    
    # Salva o arquivo temporariamente para a leitura do Docling
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(await file.read())
        temp_pdf_path = temp_pdf.name

    try:
        # A IA processa o layout, tabelas e ordem de leitura
        result = converter.convert(temp_pdf_path)
        markdown_text = result.document.export_to_markdown()
        
        return {"filename": file.filename, "markdown": markdown_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no processamento: {str(e)}")
    finally:
        os.remove(temp_pdf_path)
