import json
import re
import requests
from io import BytesIO
from pypdf import PdfReader
from duckduckgo_search import DDGS
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = "deepseek-r1:8b"

def extract_text_from_pdf(pdf_file: BytesIO) -> str:
    """Mengekstrak teks mentah dari file PDF."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def summarize_cv_with_ollama(cv_text: str) -> dict:
    """Mengirim teks CV ke DeepSeek-R1 via Ollama dan mengekstrak JSON."""
    prompt = f"""
    You are an expert HR AI assistant. Analyze the following CV/Resume text and extract:
    1. Name
    2. Location
    3. Work experience summary

    Return ONLY a valid JSON object with the exact keys: "name", "location", "work_experience_summary".
    Do not include markdown codeblocks or extra conversational text.

    CV Text:
    {cv_text[:3000]}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    
    raw_response = response.json().get("response", "{}")
    
    # Membersihkan tag <think>...</think> bawaan DeepSeek-R1 jika ada
    cleaned_response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()
    
    # Menghapus formatting markdown ```json ... ``` jika ada
    if cleaned_response.startswith("```"):
        cleaned_response = re.sub(r'^```(?:json)?\n|\n```$', '', cleaned_response, flags=re.MULTILINE).strip()

    return json.loads(cleaned_response)

def search_news_duckduckgo(query: str, max_results: int = 5) -> list:
    """Mencari berita terkini menggunakan DuckDuckGo dengan SSL bypass."""
    results = []
    
    # Menyiapkan instansiasi DDGS dengan verify=False
    ddgs = DDGS(verify=False)
    
    try:
        # Menggunakan generator .text() yang paling stabil
        search_results = list(ddgs.text(query, max_results=max_results))
        
        for item in search_results:
            results.append({
                "title": item.get("title", ""),
                "summary": item.get("body", ""),
                "url": item.get("href", ""),
                "published_date": "Recent"
            })
    except Exception as e:
        # Cetak error ke console terminal Docker agar bisa kita debug jika ada masalah
        print(f"[DEBUG SEARCH ERROR]: {str(e)}")
        # Lempar ulang exception agar Swagger memunculkan detail error daripada sekadar []
        raise Exception(f"Gagal melakukan scraping: {str(e)}")

    return results