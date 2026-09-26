from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from io import BytesIO
from app.schemas import CVSummaryResponse, NewsSearchResponse
from app.services import extract_text_from_pdf, summarize_cv_with_ollama, search_news_duckduckgo

app = FastAPI(
    title="Multi-Feature API",
    description="Backend API untuk CV Extraction (DeepSeek-R1) & Live News Search (DuckDuckGo)",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "online", "message": "AI Engine Server is Running"}

@app.post("/api/v1/process-cv", response_model=CVSummaryResponse)
async def process_cv(file: UploadFile = File(...)):
    """Feature 1: Upload PDF CV, ekstraksi teks, dan ringkas via DeepSeek-R1."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File harus berformat PDF")
    
    try:
        contents = await file.read()
        pdf_file = BytesIO(contents)
        text = extract_text_from_pdf(pdf_file)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Tidak dapat mengekstrak teks dari PDF ini")
            
        summary = summarize_cv_with_ollama(text)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses CV: {str(e)}")

@app.get("/api/v1/news-search", response_model=NewsSearchResponse)
def news_search(query: str = Query(..., description="Topik berita yang ingin dicari, contoh: Artificial Intelligence")):
    """Feature 2: Mencari berita terkini berbasis topik dari web."""
    try:
        articles = search_news_duckduckgo(query)
        return {
            "query": query,
            "articles": articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mencari berita: {str(e)}")