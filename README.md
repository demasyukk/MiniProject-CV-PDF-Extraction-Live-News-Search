# 🚀 FastAPI Multi-Feature Engine (CV Processing & Agentic News Search)

Backend API berbasis **FastAPI** dan **Docker** yang mengintegrasikan pemrosesan dokumen menggunakan **Local LLM (DeepSeek-R1 via Ollama)** serta pencarian berita *real-time* berbasis **Agentic Web Search**.

---

## 📌 Features

1. **Feature 1: Resume / CV Processing (Local LLM)**
   - Upload file PDF CV.
   - Ekstraksi teks secara *in-memory* tanpa menyimpan file ke disk (`pypdf`).
   - Ekstraksi informasi terstruktur (Nama, Lokasi, Ringkasan Pengalaman) menggunakan model **DeepSeek-R1:8b** via **Ollama**.
   - Cleaning output otomatis (menghapus tag `<think>` dan markdown wrapper).

2. **Feature 2: Agentic Live News Search**
   - Pencarian berita terkini secara *real-time* menggunakan **DuckDuckGo Search**.
   - Penanganan khusus SSL Certificate Interception pada jaringan lokal/ISP.
   - Validasi skema output terstruktur menggunakan **Pydantic**.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **Data Validation:** Pydantic (v2)
- **AI / LLM:** DeepSeek-R1:8b (Ollama local instance)
- **Data Scraping / Retrieval:** DuckDuckGo Search, Requests, PyPDF
- **Containerization:** Docker & Docker Compose

---

## 🚀 How to Run

### Prerequisites
- Docker & Docker Compose sudah terinstall.
- Ollama lokal sudah berjalan di host machine dengan model `deepseek-r1:8b`.

### Steps
1. **Clone repository ini:**
   ```bash
   git clone [https://github.com/USERNAME_KAMU/NAMA_REPO.git](https://github.com/USERNAME_KAMU/NAMA_REPO.git)
   cd NAMA_REPO
2. **Jalankan aplikasi via Docker Compose**
   docker-compose up --build
3. **Akses Swagger UI Documentation:**
   GET / - Health check status.
   POST /api/v1/process-cv - Upload PDF CV untuk dianalisis oleh DeepSeek-R1.
   GET /api/v1/news-search?query={keywords} - Pencarian berita terkini secara real-time.